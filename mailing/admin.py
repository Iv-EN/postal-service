from django.contrib import admin

from .models import Mailing, MailingRecipient, Message


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("start_sending", "end_sending", "status", "message")
    list_filter = ("start_sending", "end_sending", "status")


@admin.register(MailingRecipient)
class MailingRecipientAdmin(admin.ModelAdmin):
    list_display = ("email", "name", "comment")
    list_filter = ("email",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("topic", "text")
