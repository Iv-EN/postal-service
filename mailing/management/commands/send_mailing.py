from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone

from mailing.models import Mailing, AttemptToSend


class Command(BaseCommand):
    help = "Отправка сообщений из рассылки."

    def add_arguments(self, parser):
        parser.add_argument(
            "--id",
            type=int,
            help="ID рассылки для отправки",
        )

    def get_time(self):
        """Получает время в заданной временной зоне."""
        return timezone.localtime(timezone.now())

    def status_update(self):
        """Проверка и обновление статуса рассылки."""
        current_time = self.get_time()
        started_mailings = Mailing.objects.filter(
            start_sending__lte=current_time, status=Mailing.Status.CREATED
        )
        for mailing in started_mailings:
            mailing.status = Mailing.Status.STARTED
            mailing.save()
            self.stdout.write(
                f"Статус рассылки '{mailing.message.topic}' изменён на 'Запущена'"
            )
        expired_mailings = Mailing.objects.filter(end_sending__lt=current_time)
        for mailing in expired_mailings:
            if mailing.status != Mailing.Status.COMPLETED:
                mailing.status = Mailing.Status.COMPLETED
                mailing.save()
                self.stdout.write(
                    f"Статус рассылки '{mailing.message.topic}' изменён на 'Завершена'"
                )

    def send_email(self, mailing, recipient):
        """Отправляет письмо получателю и обрабатывает статус."""
        name, email = recipient.split(" <")
        email = email[:-1]
        try:
            response = send_mail(
                mailing.message.topic,
                mailing.message.text,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            return AttemptToSend.Status.SUCCESSFULLY, response
        except Exception as e:
            return AttemptToSend.Status.UNSUCCESSFULLY, str(e)

    def handle(self, *args, **kwargs):
        """Отправляет сообщения."""
        self.status_update()
        current_time_local = self.get_time()
        mailing_id = kwargs.get("id")
        if mailing_id:
            mailings = Mailing.objects.filter(pk=mailing_id)
        else:
            mailings = Mailing.objects.filter(
                status=Mailing.Status.CREATED,
                start_sending__lte=current_time_local,
                end_sending__gte=current_time_local,
            )
        for mailing in mailings:
            self.stdout.write(
                f"Обрабатывается рассылка: {mailing.message.topic}"
            )
            recipients = mailing.get_recipients().split(", ")
            attempts = []
            for recipient in recipients:
                status, response = self.send_email(mailing, recipient)
                self.stdout.write(f"Письмо {status} отправлено {recipient}")
                attempts.append(
                    AttemptToSend(
                        mailing=mailing,
                        status=status,
                        server_response=response,
                    )
                )
            AttemptToSend.objects.bulk_create(attempts)
            if all(
                attempt.status == AttemptToSend.Status.SUCCESSFULLY
                for attempt in attempts
            ):
                mailing.status = Mailing.Status.STARTED
                mailing.save()
        self.stdout.write(self.style.SUCCESS("Рассылка завершена"))
