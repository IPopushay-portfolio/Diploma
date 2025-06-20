from django.urls import path

from .views import UserCreateAPIView, UserDeleteAPIView, UserDetailAPIView, UserListAPIView, UserUpdateAPIView

app_name = "users"

urlpatterns = [
    path("users/", UserListAPIView.as_view(), name="user-list"),
    path("users/<int:pk>/", UserDetailAPIView.as_view(), name="user-detail"),
    path("users/create/", UserCreateAPIView.as_view(), name="user-create"),
    path("users/<int:pk>/update/", UserUpdateAPIView.as_view(), name="user-update"),
    path("users/<int:pk>/delete/", UserDeleteAPIView.as_view(), name="user-delete"),
]
