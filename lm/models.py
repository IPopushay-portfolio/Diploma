from django.conf import settings
from django.db import models


CustomUser = get_user_model


class Course(models.Model):
    title = models.CharField(
        max_length=150, verbose_name="Наименование курса", null=True
    )
    image = models.ImageField(
        upload_to="images/", verbose_name="Изображение", null=True, blank=True
    )
    description = models.TextField(null=True, blank=True, verbose_name="Описание курса")
    lessons = models.CharField(verbose_name="Наименование урока", null=True)
    amount = models.PositiveIntegerField(
        verbose_name="Стоимость курса",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"
        ordering = ["title"]


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name="Наименование", null=True)
    description = models.TextField(null=True, blank=True, verbose_name="Описание курса")
    image = models.ImageField(
        upload_to="images/", verbose_name="Изображение", null=True, blank=True
    )
    video = models.CharField(max_length=150, verbose_name="Наименование", null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"


class Subscription(models.Model):
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name = "подписка"
        verbose_name_plural = "подписки"
