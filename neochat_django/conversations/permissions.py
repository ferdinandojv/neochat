from django.db.models import Q

from .models import Conversation


def is_admin(user) -> bool:
    return bool(user and user.is_authenticated and (user.is_superuser or getattr(user, "role", "") == "admin"))


def is_reception(user) -> bool:
    return bool(user and user.is_authenticated and getattr(user, "role", "") == "recepcao")


def can_manage_users(user) -> bool:
    return is_admin(user)


def can_access_all_conversations(user) -> bool:
    return is_admin(user) or is_reception(user)


def filter_conversations_for_user(queryset, user):
    if can_access_all_conversations(user):
        return queryset
    return queryset.filter(Q(assigned_to=user) | Q(created_by=user))


def can_access_conversation(user, conversation: Conversation) -> bool:
    if can_access_all_conversations(user):
        return True
    return conversation.assigned_to_id == user.id or conversation.created_by_id == user.id


def can_edit_conversation(user, conversation: Conversation) -> bool:
    if can_access_all_conversations(user):
        return True
    return conversation.assigned_to_id == user.id


def can_transfer_conversation(user, conversation: Conversation) -> bool:
    if can_access_all_conversations(user):
        return True
    return conversation.assigned_to_id == user.id


def can_assign_target(user_obj) -> bool:
    if not user_obj or not user_obj.is_active:
        return False
    return getattr(user_obj, "role", "") in {"admin", "veterinario", "atendente", "recepcao"}
