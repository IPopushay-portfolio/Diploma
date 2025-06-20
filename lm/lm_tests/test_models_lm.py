from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from lm.models import Course, EducationalModule, Enrollment, Material

User = get_user_model()


class CourseModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testteacher", email="teacher@test.com", password="testpass123", role="teacher"
        )
        cls.course = Course.objects.create(title="Test Course", description="Test Description", teacher=cls.user)


class EducationalModuleModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testauthor", email="author@test.com", password="testpass123", role="teacher"
        )
        cls.course = Course.objects.create(title="Test Course", description="Test Description", teacher=cls.user)

    def test_unique_order_number(self):
        """Тест уникальности порядкового номера в рамках курса"""
        # Создаем второй курс для теста
        second_course = Course.objects.create(
            title="Second Course", description="Second Course Description", teacher=self.user
        )

        # Создаем модуль для первого курса
        module1 = EducationalModule.objects.create(
            order_number=1,
            title="Module 1",
            description="First module",
            course=self.course,  # первый курс
            author=self.user,
        )

        # Создаем модуль с тем же номером для другого курса
        module2 = EducationalModule.objects.create(
            order_number=1,
            title="Module 2",
            description="Second module",
            course=second_course,  # второй курс
            author=self.user,
        )

        # Проверяем, что модули созданы
        self.assertEqual(module1.order_number, 1)
        self.assertEqual(module2.order_number, 1)
        self.assertNotEqual(module1.course, module2.course)

        # Проверяем, что нельзя создать модуль с тем же номером в том же курсе
        with self.assertRaises(IntegrityError):
            EducationalModule.objects.create(
                order_number=1,
                title="Module 3",
                description="Third module",
                course=self.course,  # тот же курс, что и у module1
                author=self.user,
            )


class MaterialModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuploader", email="uploader@test.com", password="testpass123"  # добавляем email
        )

    def test_invalid_material_type(self):
        with self.assertRaises(ValidationError):  # меняем на ValidationError
            material = Material(
                title="Invalid Type", content="Test", type="invalid", uploaded_by=self.user  # неверный тип
            )
            material.full_clean()  # проверяем валидацию


class EnrollmentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем студента
        cls.student = User.objects.create_user(
            username="teststudent", email="student@test.com", password="testpass123", role="student"  # добавляем email
        )
        # Создаем преподавателя
        cls.teacher = User.objects.create_user(
            username="testteacher",
            email="teacher2@test.com",  # уникальный email
            password="testpass123",
            role="teacher",
        )
        # Создаем курс
        cls.course = Course.objects.create(title="Test Course", description="Test Description", teacher=cls.teacher)
        # Создаем модуль
        cls.module = EducationalModule.objects.create(
            order_number=1, title="Test Module", description="Test Description", course=cls.course, author=cls.teacher
        )

    def test_enrollment_creation(self):
        enrollment = Enrollment.objects.create(
            student=self.student, module=self.module, progress=0.0, status="enrolled"
        )
        self.assertEqual(enrollment.student, self.student)
        self.assertEqual(enrollment.module, self.module)
        self.assertEqual(enrollment.progress, 0.0)
        self.assertEqual(enrollment.status, "enrolled")

    def test_invalid_progress_values(self):
        with self.assertRaises(ValidationError):
            enrollment = Enrollment(student=self.student, module=self.module, progress=101.0)  # невалидное значение
            enrollment.full_clean()

    def test_invalid_status(self):
        with self.assertRaises(ValidationError):
            enrollment = Enrollment(
                student=self.student, module=self.module, progress=0.0, status="invalid"  # невалидный статус
            )
            enrollment.full_clean()
