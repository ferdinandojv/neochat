import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ConversationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if not self.scope.get("user") or not self.scope["user"].is_authenticated:
            await self.close(code=4401)
            return

        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]
        self.group_name = f"conversation_{self.conversation_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, _close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        # O envio de mensagens acontece pela API REST; o socket aqui fica focado em eventos real-time.
        return

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "type": "chat.message",
            "message": event["message"],
        }))
