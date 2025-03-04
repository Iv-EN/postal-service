from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


class UserIsNotAuthenticated(UserPassesTestMixin):

    def test_func(self):
        if self.request.user.is_authenticated:
            messages.info(self.request, "Вы уже авторизованы.")
            raise PermissionDenied
        return True

    def handle_no_permission(self):
        return redirect("home")


class ManageGroupMixin(LoginRequiredMixin):

    def is_manager_group(self):
        return self.request.user.groups.filter(name="Менеджеры").exists()
