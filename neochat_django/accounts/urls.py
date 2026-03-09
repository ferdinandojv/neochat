from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    MeView,
    ProfileEditView,
    ProfileView,
    RegisterTemplateView,
    RegisterView,
    UserListView,
)

urlpatterns = [
    # API endpoints (REST Framework)
    path("api/register/", RegisterView.as_view(), name="api_register"),
    path("api/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/me/", MeView.as_view(), name="api_me"),
    path("api/users/", UserListView.as_view(), name="api_users"),
    
    # Template views (Django Templates)
    path("register/", RegisterTemplateView.as_view(), name="register_template"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/edit/", ProfileEditView.as_view(), name="profile_edit"),
]
