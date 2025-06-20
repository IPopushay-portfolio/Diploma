from rest_framework import serializers

from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    authored_courses = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    authored_modules = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    enrolled_modules = serializers.SerializerMethodField("get_enrolled_modules")

    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "role", "authored_courses", "authored_modules", "enrolled_modules"]
        extra_kwargs = {"password": {"write_only": True}}

    def get_enrolled_modules(self, obj):
        """Получаем ID модулей, на которые записан пользователь"""
        return [enrollment.module.id for enrollment in obj.enrollments.all()]


class CustomUserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password", "role"]

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
