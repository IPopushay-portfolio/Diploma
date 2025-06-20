from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Пользователь"""

    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"

    ROLE_CHOICES = [
        (STUDENT, "Студент"),
        (TEACHER, "Преподаватель"),
        (ADMIN, "Администратор"),
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=7, choices=ROLE_CHOICES, default=STUDENT)

    @property
    def is_teacher(self):
        return self.role == self.TEACHER

    @property
    def is_student(self):
        return self.role == self.STUDENT

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
