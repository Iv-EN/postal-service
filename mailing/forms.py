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
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local"}
        ),
        label="Дата и время начала отправки"
    )
    end_sending = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local"}
        ),
        label="Дата и время окончания отправки"
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



class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = ["topic", "text"]
