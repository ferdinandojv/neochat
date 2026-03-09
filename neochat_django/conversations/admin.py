from django.contrib import admin

from .models import Conversation


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
	list_display = ("id", "customer_name", "pet_name", "channel", "status", "priority", "assigned_to")
	list_filter = ("channel", "status", "priority")
	search_fields = ("customer_name", "customer_phone", "customer_email", "pet_name")

# Register your models here.
