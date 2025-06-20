from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
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
        module1 = EducationalModule.objects.create(
            order_number=1, title="Module 1", description="First module", course=self.course, author=self.user
        )

        # Проверяем, что модуль создан успешно
        self.assertEqual(module1.order_number, 1)
        self.assertEqual(module1.title, "Module 1")

        # Пытаемся создать второй модуль с тем же номером
        with self.assertRaises(ValidationError):
            module2 = EducationalModule.objects.create(
                order_number=1, title="Module 2", description="Second module", course=self.course, author=self.user
            )
            module2.full_clean()

        # Создаем другой курс для второго модуля
        course2 = Course.objects.create(title="Test Course 2", description="Test Description 2", teacher=self.user)

        # Теперь создаем модуль с тем же номером, но для другого курса
        module2 = EducationalModule.objects.create(
            order_number=1,
            title="Module 2",
            description="Second module",
            course=course2,  # другой курс
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
