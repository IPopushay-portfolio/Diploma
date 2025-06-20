from django.core.management.base import BaseCommand

from lm.models import Course, Lesson
from users.models import CustomUser, Pay


class Command(BaseCommand):
    help = "Add pay to the database"

    def handle(self, *args, **kwargs):
        user, updated = CustomUser.objects.update_or_create(
            email="ussome@yandex.ru",
            username="user_123",
            phone_number=89991234567,
            country="Russia",
        )
        course, updated = Course.objects.update_or_create(title="Developer")
        lesson, updated = Lesson.objects.update_or_create(title="Django_drf")

        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.set_password("58Ty0bYxa")
        user.save()

        user.pay = [
            {
                "user": user,
                "paid_course": course,
                "paid_lesson": lesson,
                "date_pay": "2024-01-01",
                "payment_amount": 2000,
                "payment_method": "bank account",
            },
            {
                "user": user,
                "paid_course": course,
                "paid_lesson": lesson,
                "date_pay": "2023-01-01",
                "payment_amount": 1700,
                "payment_method": "bank account",
            },
        ]

        for pay_data in user.pay:
            pay, created = Pay.objects.get_or_create(**pay_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Successfully added pay:{user.pay}"))
            else:
                self.stdout.write(self.style.WARNING(f"Pay already exist:{user.pay}"))
