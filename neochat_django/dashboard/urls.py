from django.urls import path

from .views import (
    ConversationDetailView,
    ConversationListView,
    ConversationTransferView,
    ConversationUpdateView,
    DashboardView,
    UserCreateView,
    UserDeleteView,
    UserDetailView,
    UserListView,
    UserUpdateView,
    WhatsAppTemplateView,
)

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("users/", UserListView.as_view(), name="users"),
    path("users/new/", UserCreateView.as_view(), name="user-create"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("users/<int:pk>/edit/", UserUpdateView.as_view(), name="user-edit"),
    path("users/<int:pk>/delete/", UserDeleteView.as_view(), name="user-delete"),
    path("conversations/", ConversationListView.as_view(), name="conversations"),
    path("conversations/<int:pk>/", ConversationDetailView.as_view(), name="conversation-detail"),
    path("conversations/<int:pk>/edit/", ConversationUpdateView.as_view(), name="conversation-edit"),
    path("conversations/<int:pk>/transfer/", ConversationTransferView.as_view(), name="conversation-transfer"),
    path("whatsapp-templates/", WhatsAppTemplateView.as_view(), name="whatsapp-templates"),
]
