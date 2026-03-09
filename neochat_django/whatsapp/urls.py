from django.urls import path

from .views import SendTemplateView, WhatsAppWebhookView

urlpatterns = [
    path("webhook/", WhatsAppWebhookView.as_view(), name="whatsapp-webhook"),
    path("send-template/", SendTemplateView.as_view(), name="whatsapp-send-template"),
]
