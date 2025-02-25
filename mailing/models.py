from django.core.validators import EmailValidator
from django.db import models


class MailingRecipient(models.Model):
    """Модель получателя рассылки."""

    email = models.CharField(
        max_length=254,
        unique=True,
        verbose_name="Электронная почта",
        validators=[
            EmailValidator(message="Введите корректный адрес электронной почты.")
        ],
    )
    name = models.CharField(max_length=50, verbose_name="Ф.И.О.")
    comment = models.TextField(verbose_name="Комментарий")

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Получатель рассылки"
        verbose_name_plural = "Получатели рассылки"


class Message(models.Model):
    """Модель сообщения рассылки."""

    topic = models.CharField(max_length=50, verbose_name="Тема письма")
    text = models.TextField(verbose_name="Содержание письма")

    def __str__(self):
        return self.topic

    class Meta:
        verbose_name = "Сообщение рассылки"
        verbose_name_plural = "Сообщения рассылки"


class Mailing(models.Model):
    """Модель рассылки."""

    class Status(models.TextChoices):
        """Статусы рассылки."""

        COMPLETED = "completed", "Завершена"
        CREATED = "created", "Создана"
        STARTED = "started", "Запущена"

    start_sending = models.DateTimeField(verbose_name="Дата и время начала отправки")
    end_sending = models.DateTimeField(verbose_name="Дата и время окончания отправки")
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.CREATED,
        verbose_name="Статус",
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        verbose_name="Сообщение",
        related_name="mailings",
    )
    recipients = models.ManyToManyField(
        MailingRecipient,
        verbose_name="Получатели",
        related_name="mailings",
    )

    def __str__(self):
        return f"Рассылка: {self.message.topic}"

    def get_recipients(self):
        """Возвращает получателей рассылки."""
        return ", ".join(
            [
                f"{recipient.name} <{recipient.email}>"
                for recipient in self.recipients.all()
            ]
        )

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"


class AttemptToSend(models.Model):
    """Модель попытки рассылки."""

    class Status(models.TextChoices):
        """Статусы попытки рассылки."""

        SUCCESSFULLY = "successfully", "Успешно"
        UNSUCCESSFULLY = "unsuccessfully", "Неуспешно"

    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        verbose_name="Рассылка",
        related_name="attempts",
    )
    time_of_attempt = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата и время попытки"
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=None,
        verbose_name="Статус",
        blank=True,
        null=True,
    )
    server_response = models.TextField(
        verbose_name="Ответ почтового сервера",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"
