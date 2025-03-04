from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.core.validators import EmailValidator
from django.db import models


class BaseModel(models.Model):
    """Абстрактный класс содержащий поле 'owner'."""

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Владелец",
        related_name="%(class)s_related",
        on_delete=models.CASCADE,
        null=True,
    )

    class Meta:
        abstract = True


class MailingRecipient(BaseModel):
    """Модель получателя рассылки."""

    email = models.CharField(
        max_length=254,
        unique=True,
        verbose_name="Электронная почта",
        validators=[
            EmailValidator(
                message="Введите корректный адрес электронной почты."
            )
        ],
    )
    name = models.CharField(max_length=50, verbose_name="Ф.И.О.")
    comment = models.TextField(verbose_name="Комментарий")

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Получатель рассылки"
        verbose_name_plural = "Получатели рассылки"
        permissions = [
            ("can_view_mailingrecipient", "Просмотр получателей рассылки"),
        ]


class Message(BaseModel):
    """Модель сообщения рассылки."""

    topic = models.CharField(max_length=50, verbose_name="Тема письма")
    text = models.TextField(verbose_name="Содержание письма")

    def __str__(self):
        return self.topic

    def sent_messages_count(self):
        return self.mailings.count()

    class Meta:
        verbose_name = "Сообщение рассылки"
        verbose_name_plural = "Сообщения рассылки"
        permissions = [
            ("can_view_message", "Просмотр сообщений рассылки"),
        ]


class Mailing(BaseModel):
    """Модель рассылки."""

    class Status(models.TextChoices):
        """Статусы рассылки."""

        COMPLETED = "completed", "Завершена"
        CREATED = "created", "Создана"
        STARTED = "started", "Запущена"

    start_sending = models.DateTimeField(
        verbose_name="Дата и время начала отправки"
    )
    end_sending = models.DateTimeField(
        verbose_name="Дата и время окончания отправки"
    )
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

    def get_owner(self):
        """Возвращает владельца рассылки."""
        return f"{self.owner.username} <{self.owner.email}>"

    @property
    def successful_attempts_count(self):
        """Возвращает количество успешных попыток рассылки."""
        return self.attempts.filter(
            status=AttemptToSend.Status.SUCCESSFULLY
        ).count()

    @property
    def unsuccessful_attempts_count(self):
        """Возвращает количество неуспешных попыток рассылки."""
        return self.attempts.filter(
            status=AttemptToSend.Status.UNSUCCESSFULLY
        ).count()

    @property
    def sent_messages_count(self):
        """Возвращает количество отправленных писем."""
        return self.message.sent_messages_count()

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        permissions = [
            ("can_view_mailing", "Просмотр рассылки"),
            ("can_disable_mailing", "Отключение рассылки"),
        ]


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


class ManagerGroup:
    """Класс для создания группы менеджеров."""

    @staticmethod
    def create_group():
        """Создает группу менеджеров и добавляет к ней все необходимые права."""
        group, created = Group.objects.get_or_create(name="Менеджеры")
        permissions = [
            "can_view_mailingrecipient",
            "can_view_message",
            "can_view_mailing",
            "can_list_users",
            "can_block_user",
            "can_disable_mailing",
        ]
        for perm in permissions:
            permission = Permission.objects.get(codename=perm)
            group.permissions.add(permission)
        return group, created
