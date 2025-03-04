from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render

from .models import CustomUser


class UserManager:
    """Класс-контроллер для управления пользователями."""

    def __init__(self, user):
        print(user)
        if not user.has_perm("mailing.can_list_users"):
            raise PermissionDenied(
                "У вас недостаточно прав для просмотра списка пользователей."
            )
        if not user.has_perm("mailing.can_block_user"):
            raise PermissionDenied(
                "У вас недостаточно прав для блокировки пользователей."
            )

    def list_users(self):
        """Возвращает список всех пользователей."""
        return CustomUser.objects.all()

    def block_user(self, user_id):
        """Блокирует пользователя."""
        try:
            user = get_object_or_404(CustomUser, id=user_id)
            user.is_active = False
            user.save()
            return user
        except CustomUser.DoesNotExist:
            raise ValueError("Пользователь не найден.")
