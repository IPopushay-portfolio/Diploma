import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

CustomUser = get_user_model()


@pytest.mark.django_db
class TestUserViews:
    def setup_method(self):
        self.client = APIClient()

        # Создаем обычного пользователя
        self.user = CustomUser.objects.create_user(
            username="testuser", email="test@test.com", password="testpass123", role="student"
        )

        # Создаем админа
        self.admin = CustomUser.objects.create_superuser(
            username="admin", email="admin@test.com", password="adminpass123"
        )

        # Базовые данные для создания пользователя
        self.user_data = {"username": "newuser", "email": "new@test.com", "password": "newpass123", "role": "student"}

    def test_user_list_authenticated(self):
        """Тест получения списка пользователей (аутентифицированный пользователь)"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("users:user-list"))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0

    def test_user_list_unauthenticated(self):
        """Тест получения списка пользователей (неаутентифицированный пользователь)"""
        response = self.client.get(reverse("users:user-list"))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_list_filter_by_role(self):
        """Тест фильтрации пользователей по роли"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("users:user-list") + "?role=student")
        assert response.status_code == status.HTTP_200_OK
        assert all(user["role"] == "student" for user in response.data)

    def test_user_detail_authenticated(self):
        """Тест получения деталей пользователя (аутентифицированный пользователь)"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("users:user-detail", kwargs={"pk": self.user.pk}))
        assert response.status_code == status.HTTP_200_OK
        assert response.data["username"] == self.user.username

    def test_user_detail_unauthenticated(self):
        """Тест получения деталей пользователя (неаутентифицированный пользователь)"""
        response = self.client.get(reverse("users:user-detail", kwargs={"pk": self.user.pk}))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_create_admin(self):
        """Тест создания пользователя администратором"""
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(reverse("users:user-create"), self.user_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert CustomUser.objects.filter(username=self.user_data["username"]).exists()

    def test_user_create_non_admin(self):
        """Тест создания пользователя не администратором"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse("users:user-create"), self.user_data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_user_update_admin(self):
        """Тест обновления пользователя администратором"""
        self.client.force_authenticate(user=self.admin)
        update_data = {"username": "updated_username"}
        response = self.client.patch(reverse("users:user-update", kwargs={"pk": self.user.pk}), update_data)
        assert response.status_code == status.HTTP_200_OK
        self.user.refresh_from_db()
        assert self.user.username == "updated_username"

    def test_user_update_non_admin(self):
        """Тест обновления пользователя не администратором"""
        self.client.force_authenticate(user=self.user)
        update_data = {"username": "updated_username"}
        response = self.client.patch(reverse("users:user-update", kwargs={"pk": self.user.pk}), update_data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_user_delete_admin(self):
        """Тест удаления пользователя администратором"""
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(reverse("users:user-delete", kwargs={"pk": self.user.pk}))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not CustomUser.objects.filter(pk=self.user.pk).exists()

    def test_user_delete_non_admin(self):
        """Тест удаления пользователя не администратором"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse("users:user-delete", kwargs={"pk": self.user.pk}))
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_user_invalid_data(self):
        """Тест создания пользователя с невалидными данными"""
        self.client.force_authenticate(user=self.admin)
        invalid_data = {
            "username": "",  # Пустое имя пользователя
            "email": "invalid_email",  # Неверный формат email
            "password": "pass",  # Слишком короткий пароль
            "role": "invalid_role",  # Несуществующая роль
        }
        response = self.client.post(reverse("users:user-create"), invalid_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_user_invalid_data(self):
        """Тест обновления пользователя с невалидными данными"""
        self.client.force_authenticate(user=self.admin)
        invalid_data = {"email": "invalid_email"}  # Неверный формат email
        response = self.client.patch(reverse("users:user-update", kwargs={"pk": self.user.pk}), invalid_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
