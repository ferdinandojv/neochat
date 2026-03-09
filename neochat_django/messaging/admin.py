from django.contrib import admin

from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
	list_display = ("id", "conversation", "sender_type", "sender_user", "is_read", "created_at")
	list_filter = ("sender_type", "is_read", "created_at")
	search_fields = ("content",)

# Register your models here.
