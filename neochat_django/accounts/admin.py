from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
	fieldsets = UserAdmin.fieldsets + (
		(
			"Atendimento",
			{
				"fields": ("role", "status", "phone"),
			},
		),
	)
	list_display = ("username", "email", "first_name", "role", "status", "is_active")

# Register your models here.
