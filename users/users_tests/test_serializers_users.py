import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase

from lm.models import Course, EducationalModule, Enrollment

from ..serializers import CustomUserCreateSerializer, CustomUserSerializer

CustomUser = get_user_model()


@pytest.mark.django_db
class CustomUserSerializerTest(TestCase):
    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
            "role": "student",
        }
        self.user = CustomUser.objects.create_user(**self.user_data)
        self.serializer = CustomUserSerializer(instance=self.user)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        expected_fields = {
            "id",
            "username",
            "email",
            "role",
            "authored_courses",
            "authored_modules",
            "enrolled_modules",
        }
        self.assertEqual(set(data.keys()), expected_fields)

    def test_authored_courses_field(self):
        teacher = CustomUser.objects.create_user(
            username="teacher", email="teacher@example.com", password="pass123", role="teacher"
        )
        course = Course.objects.create(title="Test Course", description="Test Description", teacher=teacher)
        serializer = CustomUserSerializer(instance=teacher)
        self.assertIn(course.id, serializer.data["authored_courses"])

    def test_authored_modules_field(self):
        teacher = CustomUser.objects.create_user(
            username="teacher2", email="teacher2@example.com", password="pass123", role="teacher"
        )
        course = Course.objects.create(title="Test Course", description="Test Description", teacher=teacher)
        module = EducationalModule.objects.create(
            order_number=1, title="Test Module", description="Test Description", course=course, author=teacher
        )
        serializer = CustomUserSerializer(instance=teacher)
        self.assertIn(module.id, serializer.data["authored_modules"])

    def test_enrolled_modules_field(self):
        """Тест поля enrolled_modules"""
        # Создаем курс
        course = Course.objects.create(title="Test Course", description="Test Description", teacher=self.teacher)

        # Создаем модуль
        module = EducationalModule.objects.create(
            order_number=1, title="Test Module", description="Test Description", course=course, author=self.teacher
        )

        # Создаем запись на модуль
        enrollment = Enrollment.objects.create(student=self.user, module=module, progress=0.0, status="enrolled")

        serializer = CustomUserSerializer(instance=self.user)

        # Проверяем, что модуль появился в enrolled_modules
        self.assertEqual(serializer.data["enrolled_modules"], [module.id])
        self.assertIn(enrollment.module.id, serializer.data["enrolled_modules"])


@pytest.mark.django_db
class CustomUserCreateSerializerTest(TestCase):
    def setUp(self):
        self.user_data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "newpass123",
            "role": "student",
        }
        self.serializer = CustomUserCreateSerializer(data=self.user_data)

    def test_validates_data(self):
        self.assertTrue(self.serializer.is_valid())

    def test_creates_user(self):
        self.assertTrue(self.serializer.is_valid())
        user = self.serializer.save()
        self.assertEqual(user.username, self.user_data["username"])
        self.assertEqual(user.email, self.user_data["email"])
