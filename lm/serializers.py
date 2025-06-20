from rest_framework import serializers

from lm.models import Course, EducationalModule, Enrollment, Material


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для курса"""

    class Meta:
        model = Course
        fields = ["id", "title", "description", "teacher", "created_at", "updated_at"]
        read_only_fields = ["teacher", "created_at", "updated_at"]


class EducationalModuleSerializer(serializers.ModelSerializer):
    """Сериализатор для образовательного модуля"""

    materials = serializers.PrimaryKeyRelatedField(many=True, queryset=Material.objects.all(), required=False)

    class Meta:
        model = EducationalModule
        fields = [
            "id",
            "order_number",
            "title",
            "description",
            "course",
            "author",
            "materials",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["author", "created_at", "updated_at"]

    def create(self, validated_data):
        if "materials" not in validated_data:
            validated_data["materials"] = []
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)


class MaterialSerializer(serializers.ModelSerializer):
    """Сериализатор для учебного материала"""

    def create(self, validated_data):
        validated_data["uploaded_by"] = self.context["request"].user
        return super().create(validated_data)

    class Meta:
        model = Material
        fields = ["id", "title", "content", "file", "type", "uploaded_by", "uploaded_at"]
        read_only_fields = ["uploaded_by", "uploaded_at"]
        verbose_name = "Учебный материал"
        verbose_name_plural = "Учебные материалы"


class EnrollmentSerializer(serializers.ModelSerializer):
    """Сериализатор для записи на модуль"""

    def create(self, validated_data):
        validated_data["student"] = self.context["request"].user
        return super().create(validated_data)

    class Meta:
        model = Enrollment
        fields = ["id", "student", "module", "enrolled_at", "progress", "status"]
        read_only_fields = ["student", "enrolled_at"]
        verbose_name = "Запись на модуль"
        verbose_name_plural = "Записи на модули"
