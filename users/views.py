from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import CustomUser
from .serializers import CustomUserCreateSerializer, CustomUserSerializer


class UserListAPIView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = CustomUser.objects.all()
        role = self.request.query_params.get("role", None)
        if role:
            queryset = queryset.filter(role=role)
        return queryset


class UserDetailAPIView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]


class UserCreateAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserCreateSerializer
    permission_classes = [IsAdminUser]


class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminUser]


class UserDeleteAPIView(generics.DestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminUser]
