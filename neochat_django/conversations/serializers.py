from rest_framework import serializers

from .models import Conversation


class ConversationSerializer(serializers.ModelSerializer):
    assigned_to_name = serializers.CharField(source="assigned_to.username", read_only=True)

    class Meta:
        model = Conversation
        fields = [
            "id",
            "channel",
            "status",
            "priority",
            "subject",
            "customer_name",
            "customer_phone",
            "customer_email",
            "pet_name",
            "assigned_to",
            "assigned_to_name",
            "created_by",
            "metadata",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_by", "created_at", "updated_at"]
