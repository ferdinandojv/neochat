from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied

from conversations.models import Conversation
from conversations.permissions import can_access_conversation, can_edit_conversation, filter_conversations_for_user
from whatsapp.services import WhatsAppService

from .models import Message
from .realtime import broadcast_message
from .serializers import MessageSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.select_related("conversation", "sender_user")
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        allowed_conversations = filter_conversations_for_user(
            Conversation.objects.all(),
            self.request.user,
        )
        queryset = queryset.filter(conversation__in=allowed_conversations)
        conversation_id = self.request.query_params.get("conversation")
        if conversation_id:
            queryset = queryset.filter(conversation_id=conversation_id)
        return queryset

    def perform_create(self, serializer):
        conversation = serializer.validated_data["conversation"]
        if not can_access_conversation(self.request.user, conversation):
            raise PermissionDenied("Voce nao tem permissao para enviar mensagens nesta conversa.")
        if serializer.validated_data.get("sender_type") == Message.SENDER_AGENT and not can_edit_conversation(
            self.request.user,
            conversation,
        ):
            raise PermissionDenied("Voce nao pode responder uma conversa que nao esteja atribuida a voce.")

        message = serializer.save(sender_user=self.request.user)

        if message.sender_type == Message.SENDER_AGENT and message.conversation.channel == Conversation.CHANNEL_WHATSAPP:
            service = WhatsAppService()
            if service.enabled and message.conversation.customer_phone:
                try:
                    response_data = service.send_text_message(
                        message.conversation.customer_phone,
                        message.content,
                    )
                    wa_messages = response_data.get("messages", [])
                    if wa_messages:
                        message.external_id = wa_messages[0].get("id", "")
                        message.external_status = "sent"
                    metadata = message.metadata or {}
                    metadata["whatsapp_response"] = response_data
                    if message.external_id:
                        metadata["whatsapp_message_id"] = message.external_id
                    message.metadata = metadata
                except Exception as exc:
                    message.external_status = "failed"
                    metadata = message.metadata or {}
                    metadata["whatsapp_error"] = str(exc)
                    message.metadata = metadata

                message.save(update_fields=["external_id", "external_status", "metadata"])

        broadcast_message(message)
