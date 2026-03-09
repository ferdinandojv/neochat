from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
	ROLE_ADMIN = "admin"
	ROLE_VET = "veterinario"
	ROLE_AGENT = "atendente"
	ROLE_RECEPTION = "recepcao"

	STATUS_ONLINE = "online"
	STATUS_OFFLINE = "offline"
	STATUS_AWAY = "away"
	STATUS_BUSY = "busy"

	ROLE_CHOICES = [
		(ROLE_ADMIN, "Admin"),
		(ROLE_VET, "Veterinario"),
		(ROLE_AGENT, "Atendente"),
		(ROLE_RECEPTION, "Recepcao"),
	]

	STATUS_CHOICES = [
		(STATUS_ONLINE, "Online"),
		(STATUS_OFFLINE, "Offline"),
		(STATUS_AWAY, "Away"),
		(STATUS_BUSY, "Busy"),
	]

	role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_AGENT)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_OFFLINE)
	phone = models.CharField(max_length=20, blank=True)

	class Meta:
		ordering = ["first_name", "username"]

	def __str__(self) -> str:
		return f"{self.get_full_name() or self.username} ({self.role})"
