from django.conf import settings
from django.db import models


class Conversation(models.Model):
	CHANNEL_WHATSAPP = "whatsapp"
	CHANNEL_TELEGRAM = "telegram"
	CHANNEL_EMAIL = "email"
	CHANNEL_SMS = "sms"
	CHANNEL_WEB = "web"
	CHANNEL_PHONE = "phone"

	STATUS_OPEN = "open"
	STATUS_PENDING = "pending"
	STATUS_CLOSED = "closed"

	PRIORITY_LOW = "low"
	PRIORITY_MEDIUM = "medium"
	PRIORITY_HIGH = "high"

	channel = models.CharField(
		max_length=20,
		choices=[
			(CHANNEL_WHATSAPP, "WhatsApp"),
			(CHANNEL_TELEGRAM, "Telegram"),
			(CHANNEL_EMAIL, "Email"),
			(CHANNEL_SMS, "SMS"),
			(CHANNEL_WEB, "Web"),
			(CHANNEL_PHONE, "Phone"),
		],
		default=CHANNEL_WHATSAPP,
	)
	status = models.CharField(
		max_length=20,
		choices=[
			(STATUS_OPEN, "Open"),
			(STATUS_PENDING, "Pending"),
			(STATUS_CLOSED, "Closed"),
		],
		default=STATUS_OPEN,
	)
	priority = models.CharField(
		max_length=20,
		choices=[
			(PRIORITY_LOW, "Low"),
			(PRIORITY_MEDIUM, "Medium"),
			(PRIORITY_HIGH, "High"),
		],
		default=PRIORITY_MEDIUM,
	)
	subject = models.CharField(max_length=200, blank=True)
	customer_name = models.CharField(max_length=120)
	customer_phone = models.CharField(max_length=20, blank=True)
	customer_email = models.EmailField(blank=True)
	pet_name = models.CharField(max_length=120, blank=True)
	assigned_to = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name="assigned_conversations",
	)
	created_by = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name="created_conversations",
	)
	metadata = models.JSONField(default=dict, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["-updated_at"]

	def __str__(self) -> str:
		return f"{self.customer_name} - {self.channel} ({self.status})"
