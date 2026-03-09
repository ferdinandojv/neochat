from rest_framework import serializers

from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    sender_user_name = serializers.CharField(source="sender_user.username", read_only=True)

    class Meta:
        model = Message
        fields = [
            "id",
            "conversation",
            "sender_type",
            "sender_user",
            "sender_user_name",
            "content",
            "is_read",
            "metadata",
            "external_id",
            "external_status",
            "created_at",
        ]
        read_only_fields = ["id", "sender_user", "external_id", "external_status", "created_at"]
