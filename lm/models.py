from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import CustomUser

User = get_user_model()


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="authored_courses")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class EducationalModule(models.Model):
    """Образовательный модуль"""

    order_number = models.PositiveIntegerField(
        verbose_name="Порядковый номер", help_text="Порядковый номер модуля в курсе"
    )
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    course = models.ForeignKey("Course", on_delete=models.CASCADE, related_name="modules")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="authored_modules")
    materials = models.ManyToManyField("Material")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.order_number}. {self.title}.{self.description}"

    class Meta:
        ordering = ["order_number"]
        unique_together = ["course", "order_number"]
        verbose_name = "Образовательный модуль"
        verbose_name_plural = "Образовательные модули"


class Material(models.Model):
    """Учебный материал"""

    MATERIAL_TYPES = [
        ("video", "Видео"),
        ("text", "Текст"),
        ("pdf", "PDF"),
        ("link", "Ссылка"),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    file = models.FileField(upload_to="materials/", blank=True, null=True)
    type = models.CharField(max_length=5, choices=MATERIAL_TYPES)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Учебный материал"
        verbose_name_plural = "Учебные материалы"


class Enrollment(models.Model):
    """Запись на модуль"""

    STATUS_CHOICES = [
        ("enrolled", "Записан"),
        ("in_progress", "В процессе"),
        ("completed", "Завершен"),
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enrollments")
    module = models.ForeignKey("EducationalModule", on_delete=models.CASCADE, related_name="enrollments")
    enrolled_at = models.DateTimeField(auto_now_add=True)
    progress = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)], default=0.0)
    status = models.CharField(
        max_length=11,
        choices=STATUS_CHOICES,
        default="enrolled",
    )

    def __str__(self):
        return f"{self.student} - {self.module}"

    class Meta:
        verbose_name = "Запись на модуль"
        verbose_name_plural = "Записи на модули"
