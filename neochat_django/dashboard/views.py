from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
    View,
)

from conversations.models import Conversation
from conversations.permissions import (
    can_access_conversation,
    can_assign_target,
    can_edit_conversation,
    can_manage_users,
    can_transfer_conversation,
    filter_conversations_for_user,
)
from whatsapp.services import WhatsAppService

User = get_user_model()


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/index.html"


class AdminRoleRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return can_manage_users(self.request.user)

    def handle_no_permission(self):
        raise PermissionDenied("Voce nao tem permissao para acessar esta area.")


class UserListView(LoginRequiredMixin, AdminRoleRequiredMixin, ListView):
    model = User
    template_name = "dashboard/users.html"
    context_object_name = "users"
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get("search", "")
        if search:
            queryset = queryset.filter(
                username__icontains=search
            ) | queryset.filter(
                first_name__icontains=search
            ) | queryset.filter(
                last_name__icontains=search
            )
        return queryset.order_by("username")


class UserDetailView(LoginRequiredMixin, AdminRoleRequiredMixin, DetailView):
    model = User
    template_name = "dashboard/user_detail.html"
    context_object_name = "user_obj"


class UserCreateView(LoginRequiredMixin, AdminRoleRequiredMixin, CreateView):
    model = User
    template_name = "dashboard/user_form.html"
    fields = ["username", "first_name", "last_name", "email", "phone", "role", "is_active"]
    success_url = reverse_lazy("users")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(self.request.POST.get("password", "changeme123"))
        user.save()
        messages.success(self.request, f"Usuário {user.username} criado com sucesso!")
        return redirect(self.success_url)


class UserUpdateView(LoginRequiredMixin, AdminRoleRequiredMixin, UpdateView):
    model = User
    template_name = "dashboard/user_form.html"
    fields = ["first_name", "last_name", "email", "phone", "role", "status", "is_active"]
    success_url = reverse_lazy("users")

    def form_valid(self, form):
        messages.success(self.request, "Usuário atualizado com sucesso!")
        return super().form_valid(form)


class UserDeleteView(LoginRequiredMixin, AdminRoleRequiredMixin, DeleteView):
    model = User
    template_name = "dashboard/user_confirm_delete.html"
    success_url = reverse_lazy("users")

    def form_valid(self, form):
        messages.success(self.request, "Usuário removido com sucesso!")
        return super().form_valid(form)


class ConversationListView(LoginRequiredMixin, ListView):
    model = Conversation
    template_name = "dashboard/conversations.html"
    context_object_name = "conversations"
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset().select_related("assigned_to", "created_by")
        queryset = filter_conversations_for_user(queryset, self.request.user)
        
        status_filter = self.request.GET.get("status")
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        channel_filter = self.request.GET.get("channel")
        if channel_filter:
            queryset = queryset.filter(channel=channel_filter)

        assigned_filter = self.request.GET.get("assigned")
        if assigned_filter:
            queryset = queryset.filter(assigned_to_id=assigned_filter)
        
        search = self.request.GET.get("search", "")
        if search:
            queryset = queryset.filter(
                customer_name__icontains=search
            ) | queryset.filter(
                customer_phone__icontains=search
            ) | queryset.filter(
                pet_name__icontains=search
            )
        
        return queryset.order_by("-updated_at")


class ConversationDetailView(LoginRequiredMixin, DetailView):
    model = Conversation
    template_name = "dashboard/conversation_detail.html"
    context_object_name = "conversation"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not can_access_conversation(self.request.user, obj):
            raise PermissionDenied("Voce nao tem permissao para acessar esta conversa.")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users"] = User.objects.filter(is_active=True)
        context["can_transfer"] = can_transfer_conversation(self.request.user, self.object)
        context["transfer_history"] = (self.object.metadata or {}).get("transfer_history", [])
        context["messages"] = self.object.messages.select_related("sender_user").order_by("created_at")
        return context


class ConversationUpdateView(LoginRequiredMixin, UpdateView):
    model = Conversation
    template_name = "dashboard/conversation_form.html"
    fields = [
        "customer_name",
        "customer_phone",
        "customer_email",
        "pet_name",
        "channel",
        "status",
        "priority",
        "subject",
        "assigned_to",
    ]

    def get_success_url(self):
        return reverse_lazy("conversation-detail", kwargs={"pk": self.object.pk})

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not can_edit_conversation(self.request.user, obj):
            raise PermissionDenied("Voce nao tem permissao para editar esta conversa.")
        return obj

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not can_transfer_conversation(self.request.user, self.object):
            form.fields.pop("assigned_to", None)
        return form

    def form_valid(self, form):
        messages.success(self.request, "Conversa atualizada com sucesso!")
        return super().form_valid(form)


class ConversationTransferView(LoginRequiredMixin, View):
    def post(self, request, pk):
        conversation = get_object_or_404(Conversation, pk=pk)
        if not can_transfer_conversation(request.user, conversation):
            raise PermissionDenied("Voce nao tem permissao para transferir esta conversa.")

        assignee_id = request.POST.get("assigned_to")
        reason = (request.POST.get("reason") or "").strip()
        if not assignee_id:
            messages.error(request, "Selecione um usuario para transferencia.")
            return redirect("conversation-detail", pk=pk)

        target = get_object_or_404(User, pk=assignee_id)
        if not can_assign_target(target):
            messages.error(request, "Usuario de destino invalido para atribuicao.")
            return redirect("conversation-detail", pk=pk)

        previous_assignee = conversation.assigned_to
        conversation.assigned_to = target
        metadata = conversation.metadata or {}
        history = metadata.get("transfer_history", [])
        history.append(
            {
                "from": previous_assignee.username if previous_assignee else None,
                "to": target.username,
                "by": request.user.username,
                "reason": reason,
                "transferred_at": timezone.now().isoformat(),
            }
        )
        metadata["transfer_history"] = history
        conversation.metadata = metadata
        conversation.save(update_fields=["assigned_to", "metadata", "updated_at"])

        messages.success(request, f"Conversa transferida para {target.username}.")
        return redirect("conversation-detail", pk=pk)


class WhatsAppTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/whatsapp_template.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        conversations = Conversation.objects.filter(
            channel=Conversation.CHANNEL_WHATSAPP,
            status=Conversation.STATUS_OPEN,
        ).select_related("assigned_to")
        context["conversations"] = filter_conversations_for_user(conversations, self.request.user)
        context["whatsapp_enabled"] = WhatsAppService().enabled
        return context
