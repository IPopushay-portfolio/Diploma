# users/tests/test_models.py
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase

User = get_user_model()


class CustomUserModelTest(TestCase):
    def setUp(self):
        self.user_data = {"username": "testuser", "email": "test@example.com", "password": "testpass123"}

    def test_create_user(self):
        """Тест создания обычного пользователя"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.username, self.user_data["username"])
        self.assertEqual(user.email, self.user_data["email"])
        self.assertTrue(user.check_password(self.user_data["password"]))
        self.assertEqual(user.role, User.STUDENT)  # Проверка роли по умолчанию
        self.assertTrue(user.is_student)
        self.assertFalse(user.is_teacher)
        self.assertFalse(user.is_admin)

    def test_create_teacher(self):
        """Тест создания преподавателя"""
        teacher_data = self.user_data.copy()
        teacher_data["role"] = User.TEACHER
        teacher = User.objects.create_user(**teacher_data)
        self.assertEqual(teacher.role, User.TEACHER)
        self.assertTrue(teacher.is_teacher)
        self.assertFalse(teacher.is_student)
        self.assertFalse(teacher.is_admin)

    def test_create_admin(self):
        """Тест создания администратора"""
        admin_data = self.user_data.copy()
        admin_data["role"] = User.ADMIN
        admin = User.objects.create_user(**admin_data)
        self.assertEqual(admin.role, User.ADMIN)
        self.assertTrue(admin.is_admin)
        self.assertFalse(admin.is_teacher)
        self.assertFalse(admin.is_student)

    def test_email_unique(self):
        """Тест уникальности email"""
        User.objects.create_user(**self.user_data)
        duplicate_user_data = {
            "username": "another_user",
            "email": "test@example.com",  # тот же email
            "password": "anotherpass123",
        }
        with self.assertRaises(IntegrityError):
            User.objects.create_user(**duplicate_user_data)

    def test_role_choices(self):
        """Тест допустимых значений роли"""
        user = User.objects.create_user(**self.user_data)
        valid_roles = [choice[0] for choice in User.ROLE_CHOICES]
        self.assertIn(user.role, valid_roles)

    def test_str_method(self):
        """Тест строкового представления пользователя"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), user.username)

    def test_default_role(self):
        """Тест роли по умолчанию"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.role, User.STUDENT)

    def test_role_properties(self):
        """Тест свойств is_teacher, is_student, is_admin"""
        # Создаем пользователей с разными ролями
        student = User.objects.create_user(
            username="student", email="student@example.com", password="pass123", role=User.STUDENT
        )
        teacher = User.objects.create_user(
            username="teacher", email="teacher@example.com", password="pass123", role=User.TEACHER
        )
        admin = User.objects.create_user(
            username="admin", email="admin@example.com", password="pass123", role=User.ADMIN
        )

        # Проверяем свойства для студента
        self.assertTrue(student.is_student)
        self.assertFalse(student.is_teacher)
        self.assertFalse(student.is_admin)

        # Проверяем свойства для преподавателя
        self.assertTrue(teacher.is_teacher)
        self.assertFalse(teacher.is_student)
        self.assertFalse(teacher.is_admin)

        # Проверяем свойства для администратора
        self.assertTrue(admin.is_admin)
        self.assertFalse(admin.is_teacher)
        self.assertFalse(admin.is_student)

    def test_email_field(self):
        """Тест поля email"""
        user = User.objects.create_user(**self.user_data)
        field = User._meta.get_field("email")

        # Проверяем настройки поля email
        self.assertTrue(field.unique)
        self.assertFalse(field.blank)
        self.assertFalse(field.null)

        # Проверяем сохраненное значение
        self.assertEqual(user.email, self.user_data["email"])
