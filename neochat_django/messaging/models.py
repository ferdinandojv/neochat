from django.conf import settings
from django.db import models


class Message(models.Model):
    SENDER_AGENT = "agent"
    SENDER_CUSTOMER = "customer"
    SENDER_SYSTEM = "system"

    conversation = models.ForeignKey(
        "conversations.Conversation",
        on_delete=models.CASCADE,
        related_name="messages",
    )
    sender_type = models.CharField(
        max_length=20,
        choices=[
            (SENDER_AGENT, "Agent"),
            (SENDER_CUSTOMER, "Customer"),
            (SENDER_SYSTEM, "System"),
        ],
        default=SENDER_AGENT,
    )
    sender_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="messages_sent",
    )
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    metadata = models.JSONField(default=dict, blank=True)
    external_id = models.CharField(max_length=120, blank=True, db_index=True)
    external_status = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self) -> str:
        return f"{self.sender_type}: {self.content[:40]}"
