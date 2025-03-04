from abc import abstractmethod
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.core.management import call_command
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, ListView
from django.views.generic.edit import DeleteView

from services.mixins import ManageGroupMixin
from .forms import MailingForm, MailingRecipientForm, MessageForm
from .models import AttemptToSend, Mailing, MailingRecipient, Message


class BaseCreateView(LoginRequiredMixin, View):
    """Базовое представление для создания объектов."""

    model = None
    form_class = None
    template_name = "mailing/mailing_form.html"

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("users:login")
        form = self.form_class()
        title = self.get_title()
        return render(
            request, self.template_name, {"form": form, "title": title}
        )

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect("users:login")
        form = self.form_class(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            self.set_owner(instance, request.user)
            instance.save()
            return redirect(self.get_success_url(instance))
        return render(request, self.template_name, {"form": form})

    @abstractmethod
    def set_owner(self, instance, user):
        """Устанавливает владельца объекта."""

    @abstractmethod
    def get_title(self):
        """Получает заголовок страницы."""

    @abstractmethod
    def get_success_url(self, instance):
        """Получает URL для перенаправления после успешного создания."""


class BaseListView(ManageGroupMixin, ListView):
    """Базовое представление для отображения списка объектов."""

    template_name = "mailing/mailing_list.html"
    context_object_name = "context"
    cache_timeout = 60 * 15

    @method_decorator(cache_page(cache_timeout), name="dispatch")
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        context["is_manager_group"] = self.is_manager_group()
        return context

    def get_queryset(self):
        if self.request.user.has_perm(self.permission_codename):
            return self.model.objects.all()
        return self.model.objects.filter(owner=self.request.user)


class MailingRecipientListView(BaseListView):
    """Представление для отображения списка получателей рассылок."""

    model = MailingRecipient
    title = "Получатели рассылок"
    permission_codename = "mailing.can_view_mailingrecipient"


class MailingRecipientCreateView(BaseCreateView):
    """Представление для создания получателя рассылок."""

    model = MailingRecipient
    form_class = MailingRecipientForm

    def set_owner(self, instance, user):
        instance.owner = user

    def get_title(self):
        return "Создание получателя рассылки"

    def get_success_url(self, instance):
        return reverse_lazy(
            "mailing:mailing_recipient_detail", args=[instance.pk]
        )


class MailingRecipientDetailsView(LoginRequiredMixin, DetailView):
    """
    Представление для отображения детальной информации о получателе рассылки.
    """

    model = MailingRecipient


class MailingRecipientUpdateView(LoginRequiredMixin, View):
    """Представление для редактирования получателя рассылки."""

    model = MailingRecipient
    template_name = "mailing/mailing_form.html"

    def get(self, request, pk):
        recipient = get_object_or_404(MailingRecipient, pk=pk)
        form = MailingRecipientForm(instance=recipient)
        return render(request, self.template_name, {"form": form})

    def post(self, request, pk):
        recipient = get_object_or_404(MailingRecipient, pk=pk)
        form = MailingRecipientForm(request.POST, instance=recipient)
        if form.is_valid():
            form.save()
            return redirect("mailing:mailing_recipient_list")
        return render(request, self.template_name, {"form": form})


class MailingRecipientDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        recipient = get_object_or_404(MailingRecipient, pk=pk)
        recipient.delete()
        return redirect("mailing:mailing_recipient_list")


# Message Views


class MessageListView(BaseListView):
    """Представление для отображения списка сообщений."""

    model = Message
    title = "Сообщения"
    permission_codename = "mailing.can_view_message"


class MessageDetailsView(LoginRequiredMixin, DetailView):
    """Представление для отображения детальной информации о сообщении."""

    model = Message


class MessageCreateView(BaseCreateView):
    """Представление для создания сообщения."""

    model = Message
    form_class = MessageForm

    def set_owner(self, instance, user):
        instance.owner = user

    def get_title(self):
        return "Создание сообщения"

    def get_success_url(self, instance):
        return "mailing:message_list"


class MessageUpdateView(LoginRequiredMixin, View):
    """Представление для редактирования сообщения."""

    model = Message
    template_name = "mailing/mailing_form.html"

    def get(self, request, pk):
        message = get_object_or_404(Message, pk=pk)
        form = MessageForm(instance=message)
        title = "Изменить сообщение"
        return render(
            request, self.template_name, {"form": form, "title": title}
        )

    def post(self, request, pk):
        message = get_object_or_404(Message, pk=pk)
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect("mailing:message_list")
        return render(request, self.template_name, {"form": form})


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    """Представление для удаления сообщения."""

    model = Message
    template_name = "mailing/message_confirm_delete.html"
    success_url = reverse_lazy("mailing:message_list")

    def delete(self, request, *args, **kwargs):
        """Удаляет продукт."""
        messages.success(request, "Рассылка успешно удалена.")
        return super().delete(request, *args, **kwargs)


class MailingListView(BaseListView, ManageGroupMixin):
    """Представление для отображения списка рассылок."""

    model = Mailing
    title = "Рассылки"
    permission_codename = "mailing.can_view_mailing"


class MailingDetailsView(DetailView, ManageGroupMixin):
    """Представление для отображения детальной информации о рассылке."""

    model = Mailing

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_manager_group"] = self.is_manager_group()
        context["username"] = self.request.user.username
        return context


class MailingCreateView(BaseCreateView):
    """Представление для создания новой рассылки."""

    model = Mailing
    form_class = MailingForm

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect("users:login")
        form = self.form_class(request.POST, user=request.user)
        if form.is_valid():
            instance = form.save(commit=False)
            self.set_owner(instance, request.user)
            instance.save()
            form.save_m2m()
            return redirect("mailing:mailing_list")
        else:
            return render(request, "mailing/mailing_form.html", {"form": form})

    def set_owner(self, instance, user):
        instance.owner = user

    def get_title(self):
        return "Создание рассылки"

    def get_success_url(self, instance):
        return "mailing:mailing_list"


class MailingUpdateView(LoginRequiredMixin, View):
    """Представление для редактирования рассылки."""

    model = Mailing
    template_name = "mailing/mailing_form.html"

    def get(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        form = MailingForm(instance=mailing)
        title = "Редактировать рассылку"
        return render(
            request, self.template_name, {"form": form, "title": title}
        )

    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        form = MailingForm(request.POST, instance=mailing)
        if form.is_valid():
            mailing = form.save(commit=False)
            mailing.owner = request.user
            mailing.save()
            form.save_m2m()
            return redirect("mailing:mailing_list")
        return render(
            request,
            self.template_name,
            {"form": form, "title": "Редактировать рассылку"},
        )


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    """Представление для удаления рассылки."""

    model = Mailing
    template_name = "mailing/mailing_confirm_delete.html"
    success_url = reverse_lazy("mailing:mailing_list")

    def delete(self, request, *args, **kwargs):
        """Удаляет продукт."""
        messages.success(request, "Рассылка успешно удалена.")
        return super().delete(request, *args, **kwargs)


class HomeView(ManageGroupMixin, View):
    """Представление для отображения главной страницы."""

    def get_context_data(self):
        return {
            "is_manager_group": self.is_manager_group(),
            "title": "Домашняя страница",
            "mailings_count": Mailing.objects.count(),
            "mailing_active_count": Mailing.objects.filter(
                status=Mailing.Status.STARTED
            ).count(),
            "recipients_count": MailingRecipient.objects.count(),
        }

    def get(self, request):
        context = self.get_context_data()
        return render(request, "mailing/home.html", context)


class MailingSendView(LoginRequiredMixin, View):
    """Представление для отправки рассылки."""

    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk, owner=request.user)
        if mailing.status in [Mailing.Status.CREATED, Mailing.Status.STARTED]:
            call_command("send_mailing", id=pk)
            messages.success(
                request, f"Рассылка '{mailing.message.topic}' успешно запущена"
            )
        else:
            messages.warning(
                request,
                f"Рассылка '{mailing.message.topic}' не может быть запущена",
            )
        return redirect("mailing:mailing_list")


class AttemptSendListView(BaseListView):
    """Представление для отображения попыток рассылок."""

    model = AttemptToSend
    title = "Попытки рассылок"

    def get_queryset(self):
        return AttemptToSend.objects.filter(
            mailing__owner=self.request.user
        ).select_related("mailing__owner")


class StatisticsOutputView(ManageGroupMixin, View):
    """Представление для вывода статистики рассылок."""

    def get(self, request):
        title = "Статистика рассылок"
        owner = request.user
        page_title = (
            f"Статистика рассылок для {owner.username} <{owner.email}>"
        )
        template_name = "mailing/statistics.html"
        mailings = Mailing.objects.filter(owner=owner)
        successful_attempts_count = sum(
            mailing.successful_attempts_count for mailing in mailings
        )
        unsuccessful_attempts_count = sum(
            mailing.unsuccessful_attempts_count for mailing in mailings
        )
        sent_messages_count = sum(
            mailing.sent_messages_count for mailing in mailings
        )
        return render(
            request,
            template_name,
            {
                "title": title,
                "page_title": page_title,
                "successful_attempts_count": successful_attempts_count,
                "unsuccessful_attempts_count": unsuccessful_attempts_count,
                "sent_messages_count": sent_messages_count,
            },
        )


class DisableMailingView(PermissionRequiredMixin, View):
    """Представление для отключения рассылки."""

    permission_required = "mailing.can_disable_mailing"

    def post(self, request, mailing_id):
        mailing = get_object_or_404(Mailing, id=mailing_id)
        mailing.status = Mailing.Status.COMPLETED
        mailing.save()
        return redirect("mailing:mailing_list")
