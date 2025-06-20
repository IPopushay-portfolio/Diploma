from celery import shared_task
from config.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from datetime import timezone
from users.models import CustomUser


@shared_task
def send_letter(email="ussome@yandex.ru"):
    send_mail("Новое письмо", "Материалы курса обновлены", EMAIL_HOST_USER, [email])


@shared_task
def last_user_login():
    today = timezone.now().today().date()
    users = CustomUser.objects.filter(
        last__login__isnull=False, last__login__lt=today - timezone.timedelta(days=30)
    )
    if users:
        for user in users:
            user.is_active = False
            user.save()
