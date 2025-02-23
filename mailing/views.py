from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import DeleteView

from .forms import MailingForm, MailingRecipientForm, MessageForm
from .models import Mailing, MailingRecipient, Message


class BaseListView(ListView):
    template_name = "mailing/mailing_list.html"
    context_object_name = "context"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        return context

class MailingRecipientListView(BaseListView):
    """Представление для отображения списка получателей рассылок."""
    model = MailingRecipient
    title = "Получатели рассылок"


class MailingRecipientCreateView(View):
    """Представление для создания получателя рассылок."""
    model = MailingRecipient
    template_name = "mailing/mailing_form.html"

    def get(self, request):
        form = MailingRecipientForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = MailingRecipientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("mailing:mailing_recipient_list")
        return render(request, self.template_name, {"form": form})


class MailingRecipientDetailsView(DetailView):
    """
    Представление для отображения детальной информации о получателе рассылки.
    """
    model = MailingRecipient

class MailingRecipientUpdateView(View):
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


class MailingRecipientDeleteView(View):
    def get(self, request, pk):
        recipient = get_object_or_404(MailingRecipient, pk=pk)
        recipient.delete()
        return redirect("mailing_recipient_list")


# Message Views


class MessageListView(BaseListView):
    """Представление для отображения списка сообщений."""
    model = Message
    title = "Сообщения"


class MessageDetailsView(DetailView):
    """Представление для отображения детальной информации о сообщении."""
    model = Message
class MessageCreateView(View):
    """Представление для создания сообщения."""
    model = Message
    template_name = "mailing/mailing_form.html"
    def get(self, request):
        form = MessageForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("mailing:message_list")
        return render(request, self.template_name, {"form": form})


class MessageUpdateView(View):
    """Представление для редактирования сообщения."""
    model = Message
    template_name = "mailing/mailing_form.html"
    def get(self, request, pk):
        message = get_object_or_404(Message, pk=pk)
        form = MessageForm(instance=message)
        return render(request, self.template_name, {"form": form})

    def post(self, request, pk):
        message = get_object_or_404(Message, pk=pk)
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect("mailing:message_list")
        return render(request, self.template_name, {"form": form})


class MessageDeleteView(DeleteView):
    """Представление для удаления сообщения."""
    model = Message
    template_name = "mailing/message_confirm_delete.html"
    success_url = reverse_lazy("mailing:message_list")

    def delete(self, request, *args, **kwargs):
        """Удаляет продукт."""
        messages.success(request, "Рассылка успешно удалена.")
        return super().delete(request, *args, **kwargs)


# Mailing Views


class MailingListView(BaseListView):
    """Представление для отображения списка рассылок."""
    model = Mailing
    title = "Рассылки"


class MailingDetailsView(DetailView):
    """Представление для отображения детальной информации о рассылке."""
    model = Mailing
class MailingCreateView(View):
    """Представление для создания новой рассылки."""
    model = Mailing
    template_name = "mailing/mailing_form.html"

    def get(self, request):
        form = MailingForm()
        title = "Создать рассылку"
        return render(request, self.template_name, {"form": form, "title": title})

    def post(self, request):
        form = MailingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("mailing:mailing_list")
        return render(request, "mailing/mailing_form.html", {"form": form})


class MailingUpdateView(View):
    """Представление для редактирования рассылки."""
    model = Mailing
    template_name = "mailing/mailing_form.html"

    def get(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        form = MailingForm(initial={
            "start_sending":mailing.start_sending,
            "end_sending":mailing.end_sending,
            "status": mailing.status,
            "message": mailing.message,
            "recipients": mailing.recipients.all(),
        })
        title = "Редактировать рассылку"
        return render(
            request,
            self.template_name,
            {"form": form, "title": title}
        )

    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        form = MailingForm(request.POST)
        if form.is_valid():
            mailing = form.save(commit=False)
            mailing.id = pk
            mailing.save()
            form.save_m2m()
            return redirect("mailing:mailing_list")
        return render(request, self.template_name,
                      {"form": form, "title":"Редактировать рассылку"})


class MailingDeleteView(DeleteView):
    """Представление для удаления рассылки."""
    model = Mailing
    template_name = "mailing/mailing_confirm_delete.html"
    success_url = reverse_lazy("mailing:mailing_list")

    def delete(self, request, *args, **kwargs):
        """Удаляет продукт."""
        messages.success(request, "Рассылка успешно удалена.")
        return super().delete(request, *args, **kwargs)


class HomeView(View):
    """Представление для отображения главной страницы."""
    def get(self, request):
        title = "Домашняя страница"
        template_name = "mailing/home.html"
        return render(
            request,
            template_name,
            {
                "title": title,
                "mailings_count": Mailing.objects.count(),
                "mailing_active_count": Mailing.objects.filter(
                    status=Mailing.Status.STARTED
                ).count(),
                "recipients_count": MailingRecipient.objects.count(),
            },
        )
