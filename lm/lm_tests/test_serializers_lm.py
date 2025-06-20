from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from users.models import CustomUser

from ..models import Course, EducationalModule, Enrollment, Material
from ..serializers import CourseSerializer, EducationalModuleSerializer, MaterialSerializer

User = get_user_model()


class CourseSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testteacher", email="teacher@test.com", password="testpass123", role="teacher"
        )
        self.course_data = {"title": "Test Course", "description": "Test Description"}
        self.course = Course.objects.create(teacher=self.user, **self.course_data)
        self.serializer = CourseSerializer(instance=self.course)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ["id", "title", "description", "teacher", "created_at", "updated_at"])

    def test_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["title"], self.course_data["title"])
        self.assertEqual(data["description"], self.course_data["description"])
        self.assertEqual(data["teacher"], self.user.id)


class EducationalModuleSerializerTest(TestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(
            username="testteacher", email="teacher@test.com", password="testpass123", role="teacher"
        )

        self.course = Course.objects.create(title="Test Course", description="Test Description", teacher=self.teacher)

        # Создаем тестовый материал
        self.material = Material.objects.create(
            title="Test Material", content="Test Content", type="text", uploaded_by=self.teacher
        )

        self.module_data = {
            "order_number": 1,
            "title": "Module 1",
            "description": "First module description",
            "course": self.course.id,
            "materials": [],  # Пустой список материалов
        }

        self.factory = APIRequestFactory()
        self.request = self.factory.post("/")
        self.request.user = self.teacher

    def test_create_module(self):
        """Тест создания модуля"""
        serializer = EducationalModuleSerializer(data=self.module_data, context={"request": self.request})

        if not serializer.is_valid():
            print("Validation errors:", serializer.errors)

        self.assertTrue(serializer.is_valid())
        module = serializer.save()

        self.assertEqual(module.order_number, self.module_data["order_number"])
        self.assertEqual(module.title, self.module_data["title"])
        self.assertEqual(module.description, self.module_data["description"])
        self.assertEqual(module.course.id, self.module_data["course"])
        self.assertEqual(module.author, self.teacher)

    def test_different_courses_same_order_number(self):
        """Тест возможности использования одинаковых номеров в разных курсах"""
        course2 = Course.objects.create(
            title="Second Course", description="Second Course Description", teacher=self.teacher
        )

        # Создаем первый модуль и проверяем его
        first_module = EducationalModule.objects.create(
            order_number=1,
            title="Module in First Course",
            description="Description",
            course=self.course,
            author=self.teacher,
        )
        self.assertEqual(first_module.order_number, 1)
        self.assertEqual(first_module.course, self.course)

        # Создаем второй модуль в другом курсе
        second_module_data = {
            "order_number": 1,
            "title": "Module in Second Course",
            "description": "Description",
            "course": course2.id,
            "materials": [],
        }

        serializer = EducationalModuleSerializer(data=second_module_data, context={"request": self.request})

        self.assertTrue(serializer.is_valid())
        module = serializer.save()
        self.assertEqual(module.order_number, 1)
        self.assertEqual(module.course, course2)

    def test_optional_materials(self):
        """Тест необязательности материалов"""
        data = {
            "order_number": 1,
            "title": "Module without materials",
            "description": "Description",
            "course": self.course.id,
        }

        serializer = EducationalModuleSerializer(data=data, context={"request": self.request})

        if not serializer.is_valid():
            print("Validation errors:", serializer.errors)

        self.assertTrue(serializer.is_valid())
        module = serializer.save()
        self.assertEqual(list(module.materials.all()), [])

    def test_with_materials(self):
        """Тест с материалами"""
        data = self.module_data.copy()
        data["materials"] = [self.material.id]

        serializer = EducationalModuleSerializer(data=data, context={"request": self.request})

        if not serializer.is_valid():
            print("Validation errors:", serializer.errors)

        self.assertTrue(serializer.is_valid())
        module = serializer.save()
        self.assertIn(self.material, module.materials.all())


class MaterialSerializerTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username="testuploader", email="uploader@test.com", password="testpass123"
        )
        self.material_data = {"title": "Test Material", "content": "Test Content", "type": "text"}
        self.request = self.factory.post("/fake-url/")
        self.request.user = self.user

    def test_create_material(self):
        serializer = MaterialSerializer(data=self.material_data, context={"request": self.request})
        self.assertTrue(serializer.is_valid())
        material = serializer.save()
        self.assertEqual(material.uploaded_by, self.user)
        self.assertEqual(material.title, self.material_data["title"])

    def test_validate_type(self):
        invalid_data = self.material_data.copy()
        invalid_data["type"] = "invalid"
        serializer = MaterialSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())


class EnrollmentModelTest(TestCase):
    def setUp(self):
        # Создаем студента
        self.student = CustomUser.objects.create_user(
            username="student", email="student@test.com", password="testpass123", role="student"
        )

        # Создаем преподавателя
        self.teacher = CustomUser.objects.create_user(
            username="teacher", email="teacher@test.com", password="testpass123", role="teacher"
        )

        # Создаем курс
        self.course = Course.objects.create(title="Test Course", description="Test Description", teacher=self.teacher)

        # Создаем модуль
        self.module = EducationalModule.objects.create(
            order_number=1,
            title="Test Module",
            description="Test Description",
            course=self.course,
            author=self.teacher,
        )

    def test_enrollment_creation(self):
        """Тест создания записи на модуль"""
        enrollment = Enrollment.objects.create(
            student=self.student, module=self.module, progress=0.0, status="enrolled"
        )

        self.assertEqual(enrollment.student, self.student)
        self.assertEqual(enrollment.module, self.module)
        self.assertEqual(enrollment.progress, 0.0)
        self.assertEqual(enrollment.status, "enrolled")
        self.assertIsNotNone(enrollment.enrolled_at)

    def test_progress_validation(self):
        """Тест валидации прогресса"""
        # Тест значения ниже 0
        with self.assertRaises(ValidationError):
            enrollment = Enrollment(student=self.student, module=self.module, progress=-1.0, status="enrolled")
            enrollment.full_clean()

        # Тест значения выше 100
        with self.assertRaises(ValidationError):
            enrollment = Enrollment(student=self.student, module=self.module, progress=101.0, status="enrolled")
            enrollment.full_clean()

        # Тест граничных значений
        enrollment_min = Enrollment.objects.create(
            student=self.student, module=self.module, progress=0.0, status="enrolled"
        )
        enrollment_min.full_clean()  # Не должно вызывать исключение

        enrollment_max = Enrollment.objects.create(
            student=self.student, module=self.module, progress=100.0, status="enrolled"
        )
        enrollment_max.full_clean()  # Не должно вызывать исключение

    def test_status_choices(self):
        """Тест выбора статуса"""
        # Тест всех допустимых статусов
        valid_statuses = ["enrolled", "in_progress", "completed"]

        for status in valid_statuses:
            enrollment = Enrollment.objects.create(
                student=self.student, module=self.module, progress=0.0, status=status
            )
            enrollment.full_clean()  # Не должно вызывать исключение
            self.assertEqual(enrollment.status, status)

        # Тест недопустимого статуса
        with self.assertRaises(ValidationError):
            enrollment = Enrollment(student=self.student, module=self.module, progress=0.0, status="invalid_status")
            enrollment.full_clean()

    def test_default_values(self):
        """Тест значений по умолчанию"""
        enrollment = Enrollment.objects.create(student=self.student, module=self.module)

        self.assertEqual(enrollment.progress, 0.0)
        self.assertEqual(enrollment.status, "enrolled")
        self.assertIsNotNone(enrollment.enrolled_at)

    def test_str_method(self):
        """Тест строкового представления"""
        enrollment = Enrollment.objects.create(
            student=self.student, module=self.module, progress=0.0, status="enrolled"
        )
        expected_str = f"{self.student} - {self.module}"
        self.assertEqual(str(enrollment), expected_str)

    def test_required_fields(self):
        """Тест обязательных полей"""
        # Тест без student
        with self.assertRaises(ValidationError):
            enrollment = Enrollment(module=self.module, progress=0.0, status="enrolled")
            enrollment.full_clean()

        # Тест без module
        with self.assertRaises(ValidationError):
            enrollment = Enrollment(student=self.student, progress=0.0, status="enrolled")
            enrollment.full_clean()
