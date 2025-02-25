from django import forms
from django.forms import BooleanField

from .models import Mailing, MailingRecipient, Message


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class MailingRecipientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailingRecipient
        fields = ["email", "name", "comment"]


class MailingForm(StyleFormMixin, forms.ModelForm):
    start_sending = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
        label="Дата и время начала отправки",
    )
    end_sending = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
        label="Дата и время окончания отправки",
    )

    class Meta:
        model = Mailing
        fields = [
            "start_sending",
            "end_sending",
            "status",
            "message",
            "recipients",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["message"].queryset = Message.objects.all()
        self.fields["recipients"].queryset = MailingRecipient.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        start_sending = self.cleaned_data.get("start_sending")
        end_sending = self.cleaned_data.get("end_sending")
        if start_sending and end_sending and start_sending >= end_sending:
            raise forms.ValidationError(
                "Дата и время окончания рассылки должно быть больше даты и времени начала."
            )
        return cleaned_data


class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = ["topic", "text"]
