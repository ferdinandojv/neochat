import json

from django.db import transaction
from django.http import HttpResponse
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from conversations.models import Conversation
from messaging.models import Message
from messaging.realtime import broadcast_message

from .serializers import SendTemplateSerializer
from .services import WhatsAppService


class WhatsAppWebhookView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        service = WhatsAppService()
        mode = request.query_params.get("hub.mode")
        verify_token = request.query_params.get("hub.verify_token")
        challenge = request.query_params.get("hub.challenge")

        if mode == "subscribe" and verify_token == service.webhook_verify_token:
            return HttpResponse(challenge or "", content_type="text/plain", status=200)

        return HttpResponse("forbidden", status=403)

    def post(self, request):
        service = WhatsAppService()
        signature = request.headers.get("X-Hub-Signature-256")
        if not service.verify_signature(request.body, signature):
            return Response({"detail": "invalid signature"}, status=status.HTTP_403_FORBIDDEN)

        payload = json.loads(request.body.decode("utf-8") or "{}")
        self._process_payload(payload)
        return Response({"status": "received"}, status=status.HTTP_200_OK)

    def _process_payload(self, payload):
        entries = payload.get("entry", [])
        for entry in entries:
            for change in entry.get("changes", []):
                value = change.get("value", {})
                self._handle_incoming_messages(value.get("messages", []), value.get("contacts", []))
                self._handle_status_updates(value.get("statuses", []))

    def _handle_incoming_messages(self, messages, contacts):
        contact_name = "Cliente"
        if contacts:
            contact_name = contacts[0].get("profile", {}).get("name") or contact_name

        for incoming in messages:
            from_phone = incoming.get("from", "")
            if not from_phone:
                continue

            body = self._extract_message_text(incoming)
            if body is None:
                body = "[mensagem nao suportada recebida]"

            with transaction.atomic():
                conversation, _created = Conversation.objects.get_or_create(
                    channel=Conversation.CHANNEL_WHATSAPP,
                    customer_phone=from_phone,
                    defaults={
                        "customer_name": contact_name,
                        "status": Conversation.STATUS_OPEN,
                        "priority": Conversation.PRIORITY_MEDIUM,
                        "subject": "Atendimento WhatsApp",
                    },
                )

                message = Message.objects.create(
                    conversation=conversation,
                    sender_type=Message.SENDER_CUSTOMER,
                    content=body,
                    metadata={"whatsapp_message_id": incoming.get("id", "")},
                    external_id=incoming.get("id", ""),
                    external_status="received",
                )

            broadcast_message(message)

    def _handle_status_updates(self, statuses):
        for item in statuses:
            message_id = item.get("id")
            status_value = item.get("status")
            if not message_id or not status_value:
                continue

            message = Message.objects.filter(external_id=message_id).first()
            if not message:
                continue

            message.external_status = status_value
            metadata = message.metadata or {}
            metadata["whatsapp_status"] = status_value
            message.metadata = metadata
            if status_value == "read":
                message.is_read = True
            message.save(update_fields=["external_status", "metadata", "is_read"])

    def _extract_message_text(self, incoming):
        msg_type = incoming.get("type")
        if msg_type == "text":
            return incoming.get("text", {}).get("body", "")

        if msg_type in {"image", "audio", "video", "document", "sticker"}:
            return f"[{msg_type}]"

        return None


class SendTemplateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = SendTemplateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        conversation_id = data["conversation_id"]
        template_name = data["template_name"]
        language_code = data.get("language_code", "pt_BR")
        components = data.get("components")

        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversa nao encontrada."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if conversation.channel != Conversation.CHANNEL_WHATSAPP:
            return Response(
                {"error": "Conversa nao eh do tipo WhatsApp."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not conversation.customer_phone:
            return Response(
                {"error": "Telefone do cliente nao configurado."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        service = WhatsAppService()
        if not service.enabled:
            return Response(
                {"error": "WhatsApp nao configurado no servidor."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        try:
            response_data = service.send_template_message(
                conversation.customer_phone,
                template_name,
                language_code,
                components,
            )

            message_content = f"[Template enviado: {template_name}]"
            wa_messages = response_data.get("messages", [])
            external_id = wa_messages[0].get("id", "") if wa_messages else ""

            message = Message.objects.create(
                conversation=conversation,
                sender_type=Message.SENDER_AGENT,
                sender_user=request.user,
                content=message_content,
                external_id=external_id,
                external_status="sent",
                metadata={
                    "whatsapp_template_name": template_name,
                    "whatsapp_language": language_code,
                    "whatsapp_response": response_data,
                },
            )

            broadcast_message(message)

            return Response(
                {
                    "success": True,
                    "message_id": message.id,
                    "external_id": external_id,
                    "whatsapp_response": response_data,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as exc:
            return Response(
                {"error": f"Erro ao enviar template: {str(exc)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
