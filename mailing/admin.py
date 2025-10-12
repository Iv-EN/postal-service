from django.contrib import admin

from .models import Mailing, MailingRecipient, Message, AttemptToSend


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = (
        "start_sending",
        "end_sending",
        "status",
        "message",
        "owner",
        "successful_attempts_count",
        "unsuccessful_attempts_count",
        "sent_messages_count",
    )
    list_filter = ("start_sending", "end_sending", "status", "owner")

    def successful_attempts_count(self, obj):
        return obj.successful_attempts_count

    successful_attempts_count.short_description = "Успешные попытки"

    def unsuccessful_attempts_count(self, obj):
        return obj.unsuccessful_attempts_count

    unsuccessful_attempts_count.short_description = "Неуспешные попытки"

    def sent_messages_count(self, obj):
        return obj.sent_messages_count

    sent_messages_count.short_description = "Отправленные сообщения"


@admin.register(MailingRecipient)
class MailingRecipientAdmin(admin.ModelAdmin):
    list_display = ("email", "name", "comment", "owner")
    list_filter = ("email",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("topic", "text", "owner")


@admin.register(AttemptToSend)
class AttemptToSendAdmin(admin.ModelAdmin):
    list_display = ("mailing", "time_of_attempt", "status", "server_response")
    list_filter = ("status",)
