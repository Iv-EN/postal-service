from django import forms

from .models import MailingRecipient, Message, Mailing


class MailingRecipientForm(forms.ModelForm):
    class Meta:
        model = MailingRecipient
        fields = ["email", "name", "comment"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Электронная почта",
            }
        )
        self.fields["name"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Фамилия Имя Отчество.",
            }
        )
        self.fields["comment"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Комментарий",
            }
        )


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ["start_sending", "end_sending", "status", "message", "recipients"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["start_sending"].widget.attrs.update(
            {
                "class": "form-control",
                "type": "datetime-local",
                "placeholder": "Дата и время начала отправки",
            }
        )
        self.fields["end_sending"].widget.attrs.update(
            {
                "class": "form-control",
                "type": "datetime-local",
                "placeholder": "Дата и время окончания отправки",
            }
        )
        self.fields["status"].widget = forms.Select(
            choices=Mailing.Status.choices,
            attrs={"class": "form-control"},
        )
        self.fields["message"].queryset = Message.objects.all()
        self.fields["recipients"].queryset = MailingRecipient.objects.all()


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["topic", "text"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["topic"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Тема письма",
            }
        )
        self.fields["text"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Содержание письма",
            }
        )
