from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def build_message_payload(message):
    return {
        "id": message.id,
        "conversation": message.conversation_id,
        "sender_type": message.sender_type,
        "sender_user": message.sender_user_id,
        "sender_user_name": message.sender_user.username if message.sender_user else message.sender_type,
        "content": message.content,
        "is_read": message.is_read,
        "metadata": message.metadata,
        "created_at": message.created_at.isoformat(),
    }


def broadcast_message(message):
    payload = build_message_payload(message)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"conversation_{message.conversation_id}",
        {
            "type": "chat_message",
            "message": payload,
        },
    )
