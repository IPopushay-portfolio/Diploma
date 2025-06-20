# lm/tests/test_views.py
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from users.models import CustomUser

from ..apps import LmConfig
from ..models import Course, EducationalModule, Enrollment, Material

User = get_user_model()


class CourseViewsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.teacher = User.objects.create_user(
            username="teacher", email="teacher@test.com", password="testpass123", role="teacher"
        )
        # Аутентифицируем пользователя для всех тестов
        self.client.force_authenticate(user=self.teacher)

        self.course = Course.objects.create(title="Test Course", description="Test Description", teacher=self.teacher)
        self.course_data = {"title": "New Course", "description": "New Description"}

    def test_course_list(self):
        url = reverse(f"{LmConfig.name}:course-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_course_detail(self):
        url = reverse(f"{LmConfig.name}:course-detail", kwargs={"pk": self.course.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class EducationalModuleViewsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.teacher = User.objects.create_user(
            username="teacher2", email="teacher2@test.com", password="testpass123", role="teacher"
        )
        # Аутентифицируем пользователя
        self.client.force_authenticate(user=self.teacher)

        self.course = Course.objects.create(title="Test Course", description="Test Description", teacher=self.teacher)
        self.module_data = {
            "order_number": 1,
            "title": "Test Module",
            "description": "Test Description",
            "course": self.course.id,
        }

    def test_module_list(self):
        url = reverse(f"{LmConfig.name}:module-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class MaterialViewsTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Создаем преподавателя
        self.teacher = CustomUser.objects.create_user(
            username="teacher", email="teacher@test.com", password="testpass123", role="teacher"
        )

        # Создаем студента
        self.student = CustomUser.objects.create_user(
            username="student", email="student@test.com", password="testpass123", role="student"
        )

        # Создаем тестовые материалы
        self.material = Material.objects.create(
            title="Test Material", content="Test Content", type="text", uploaded_by=self.teacher
        )

        self.material_data = {"title": "New Material", "content": "New Content", "type": "text"}

    def test_list_material_authenticated(self):
        """Тест получения списка материалов (аутентифицированный пользователь)"""
        self.client.force_authenticate(user=self.student)
        url = reverse(f"{LmConfig.name}:material-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_material_unauthenticated(self):
        """Тест получения списка материалов (неаутентифицированный пользователь)"""
        url = reverse(f"{LmConfig.name}:material-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_detail_material_authenticated(self):
        """Тест получения деталей материала (аутентифицированный пользователь)"""
        self.client.force_authenticate(user=self.student)
        url = reverse(f"{LmConfig.name}:material-detail", kwargs={"pk": self.material.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.material.title)

    def test_detail_material_unauthenticated(self):
        """Тест получения деталей материала (неаутентифицированный пользователь)"""
        url = reverse(f"{LmConfig.name}:material-detail", kwargs={"pk": self.material.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_material_teacher(self):
        """Тест создания материала преподавателем"""
        self.client.force_authenticate(user=self.teacher)
        url = reverse(f"{LmConfig.name}:material-create")
        response = self.client.post(url, self.material_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], self.material_data["title"])
        self.assertEqual(response.data["uploaded_by"], self.teacher.id)

    def test_create_material_student(self):
        """Тест создания материала студентом (должно быть запрещено)"""
        self.client.force_authenticate(user=self.student)
        url = reverse(f"{LmConfig.name}:material-create")
        response = self.client.post(url, self.material_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_material_teacher(self):
        """Тест обновления материала преподавателем"""
        self.client.force_authenticate(user=self.teacher)
        url = reverse(f"{LmConfig.name}:material-update", kwargs={"pk": self.material.pk})
        update_data = {"title": "Updated Material", "content": "Updated Content", "type": "text"}
        response = self.client.put(url, update_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.material.refresh_from_db()
        self.assertEqual(self.material.title, update_data["title"])

    def test_update_material_student(self):
        """Тест обновления материала студентом (должно быть запрещено)"""
        self.client.force_authenticate(user=self.student)
        url = reverse(f"{LmConfig.name}:material-update", kwargs={"pk": self.material.pk})
        update_data = {"title": "Updated Material", "content": "Updated Content", "type": "text"}
        response = self.client.put(url, update_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_material_teacher(self):
        """Тест удаления материала преподавателем"""
        self.client.force_authenticate(user=self.teacher)
        url = reverse(f"{LmConfig.name}:material-delete", kwargs={"pk": self.material.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Material.objects.filter(pk=self.material.pk).exists())

    def test_delete_material_student(self):
        """Тест удаления материала студентом (должно быть запрещено)"""
        self.client.force_authenticate(user=self.student)
        url = reverse(f"{LmConfig.name}:material-delete", kwargs={"pk": self.material.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Material.objects.filter(pk=self.material.pk).exists())

    def test_create_material_invalid_type(self):
        """Тест создания материала с неверным типом"""
        self.client.force_authenticate(user=self.teacher)
        url = reverse(f"{LmConfig.name}:material-create")
        invalid_data = self.material_data.copy()
        invalid_data["type"] = "invalid_type"
        response = self.client.post(url, invalid_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class EnrollmentViewsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.student = User.objects.create_user(
            username="student", email="student@test.com", password="testpass123", role="student"
        )
        self.teacher = User.objects.create_user(
            username="teacher4", email="teacher4@test.com", password="testpass123", role="teacher"
        )
        self.course = Course.objects.create(title="Test Course", description="Test Description", teacher=self.teacher)
        self.module = EducationalModule.objects.create(
            order_number=1,
            title="Test Module",
            description="Test Description",
            course=self.course,
            author=self.teacher,
        )

    def test_enrollment_update(self):
        self.client.force_authenticate(user=self.student)
        enrollment = Enrollment.objects.create(
            student=self.student, module=self.module, progress=0.0, status="enrolled"
        )
        url = reverse(f"{LmConfig.name}:enrollment-update", kwargs={"pk": enrollment.pk})
        data = {"module": self.module.id, "progress": 50.0, "status": "in_progress"}  # Добавляем обязательное поле
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_student_access_only(self):
        self.client.force_authenticate(user=self.teacher)
        url = reverse(f"{LmConfig.name}:enrollment-list")
        response = self.client.get(url)
        # Проверяем, что преподаватель не может получить доступ к записям
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
