from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView
from rest_framework import generics, permissions

from .forms import ProfileEditForm, UserRegistrationForm
from .serializers import RegisterSerializer, UserSerializer


User = get_user_model()


# ========================================
# API VIEWS (REST Framework)
# ========================================

class RegisterView(generics.CreateAPIView):
    """API endpoint para registro de usuários"""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class MeView(generics.RetrieveAPIView):
    """API endpoint para dados do usuário logado"""
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UserListView(generics.ListAPIView):
    """API endpoint para listagem de usuários"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


# ========================================
# TEMPLATE VIEWS (Django Templates)
# ========================================

class RegisterTemplateView(CreateView):
    """View para registro de usuários via Django Template"""
    model = User
    form_class = UserRegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        # Redireciona usuários já autenticados
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Conta criada com sucesso! Faça login para continuar.')
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, TemplateView):
    """View para visualizar perfil do usuário logado"""
    template_name = 'registration/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """View para editar perfil do usuário logado"""
    model = User
    form_class = ProfileEditForm
    template_name = 'registration/profile_edit.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Perfil atualizado com sucesso!')
        return super().form_valid(form)
