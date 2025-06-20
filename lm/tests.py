from rest_framework.test import APITestCase
from rest_framework import status
from lms.models import Course, Lesson
from users.models import CustomUser
from lms.models import Subscription
from django.urls import reverse
from django.contrib.auth import get_user_model


class LessonTestCase(APITestCase):
    def setUp(self):
        self.superuser = get_user_model().objects.create_superuser(
            username="username",
            email="admin@sky.pro",
            password="12345",
        )
        self.course = Course.objects.create(
            title="Developer",
        )
        self.lessons = Lesson.objects.create(
            title="Django_drf",
            course=self.course,
        )
        self.client.force_authenticate(
            user=self.superuser,
        )

    def test_lesson_retrieve(self):
        url = reverse(
            "lms:lesson-get",
            args=[
                self.lessons.pk,
            ],
        )
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lessons.title)

    def test_lesson_create(self):
        url = reverse("lms:lesson-create")
        data = {
            "title": "Django_drf",
            "description": "Developer",
            "video": "https://www.youtube.com/1",
            "course": self.course,
        }
        response = self.client.post(
            url,
            data,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        url = reverse(
            "lms:lesson-update",
            args=[
                self.lessons.pk,
            ],
        )
        data = {"title": "Data_analysis"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "Data_analysis")

    def test_lesson_delete(self):
        url = reverse(
            "lms:lesson-delete",
            args=[
                self.lessons.pk,
            ],
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse("lms:lesson-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(email="admin@sky.pro")
        self.course = Course.objects.create(title=self.user)
        self.subscription = Subscription.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscription_create(self):
        url = reverse("lms:subscription-create")
        data = {"user": self.user.pk, "course": self.course.pk}
        response = self.client.post(url, data)
        print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
