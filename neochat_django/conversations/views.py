from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import permissions, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from .models import Conversation
from .permissions import (
    can_assign_target,
    can_edit_conversation,
    can_transfer_conversation,
    filter_conversations_for_user,
)
from .serializers import ConversationSerializer


User = get_user_model()


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.select_related("assigned_to", "created_by")
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        return filter_conversations_for_user(queryset, self.request.user)

    def perform_create(self, serializer):
        assignee = serializer.validated_data.get("assigned_to")
        if assignee and assignee != self.request.user and not self.request.user.role in {"admin", "recepcao"}:
            raise PermissionDenied("Voce nao tem permissao para atribuir conversa a outro usuario.")
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        conversation = self.get_object()
        if not can_edit_conversation(self.request.user, conversation):
            raise PermissionDenied("Voce nao tem permissao para editar esta conversa.")

        previous_assignee = conversation.assigned_to
        new_assignee = serializer.validated_data.get("assigned_to", previous_assignee)
        is_transfer = "assigned_to" in serializer.validated_data and new_assignee != previous_assignee

        if is_transfer:
            if not can_transfer_conversation(self.request.user, conversation):
                raise PermissionDenied("Voce nao tem permissao para transferir esta conversa.")
            if new_assignee and not can_assign_target(new_assignee):
                raise serializers.ValidationError({"assigned_to": "Usuario de destino invalido para atribuicao."})

        updated = serializer.save()

        if is_transfer:
            metadata = updated.metadata or {}
            history = metadata.get("transfer_history", [])
            history.append(
                {
                    "from": previous_assignee.username if previous_assignee else None,
                    "to": new_assignee.username if new_assignee else None,
                    "by": self.request.user.username,
                    "reason": "transferencia via update",
                    "transferred_at": timezone.now().isoformat(),
                }
            )
            metadata["transfer_history"] = history
            updated.metadata = metadata
            updated.save(update_fields=["metadata", "updated_at"])

    @action(detail=True, methods=["post"], url_path="transfer")
    def transfer(self, request, pk=None):
        conversation = self.get_object()
        if not can_transfer_conversation(request.user, conversation):
            raise PermissionDenied("Voce nao tem permissao para transferir esta conversa.")

        assignee_id = request.data.get("assigned_to")
        reason = (request.data.get("reason") or "").strip()
        if not assignee_id:
            raise serializers.ValidationError({"assigned_to": "Campo obrigatorio."})

        try:
            target = User.objects.get(pk=assignee_id)
        except User.DoesNotExist as exc:
            raise serializers.ValidationError({"assigned_to": "Usuario de destino nao encontrado."}) from exc

        if not can_assign_target(target):
            raise serializers.ValidationError({"assigned_to": "Usuario de destino invalido para atribuicao."})

        previous_assignee = conversation.assigned_to
        conversation.assigned_to = target
        metadata = conversation.metadata or {}
        history = metadata.get("transfer_history", [])
        history.append(
            {
                "from": previous_assignee.username if previous_assignee else None,
                "to": target.username,
                "by": request.user.username,
                "reason": reason,
                "transferred_at": timezone.now().isoformat(),
            }
        )
        metadata["transfer_history"] = history
        conversation.metadata = metadata
        conversation.save(update_fields=["assigned_to", "metadata", "updated_at"])

        payload = self.get_serializer(conversation).data
        return Response(payload, status=status.HTTP_200_OK)
