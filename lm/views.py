from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions

from lm.models import Course, EducationalModule, Enrollment, Material
from lm.serializers import CourseSerializer, EducationalModuleSerializer, EnrollmentSerializer, MaterialSerializer
from users.permissions import IsStudent, IsTeacherOrReadOnly


# Курсы
class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["title", "teacher"]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "title"]


class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]


class CourseCreateView(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsTeacherOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)


class CourseUpdateView(generics.UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsTeacherOrReadOnly]


class CourseDeleteView(generics.DestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsTeacherOrReadOnly]


# Образовательные модули
class EducationalModuleListView(generics.ListAPIView):
    queryset = EducationalModule.objects.all()
    serializer_class = EducationalModuleSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["title", "author"]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "title"]


class EducationalModuleDetailView(generics.RetrieveAPIView):
    queryset = EducationalModule.objects.all()
    serializer_class = EducationalModuleSerializer
    permission_classes = [permissions.IsAuthenticated]


class EducationalModuleCreateView(generics.CreateAPIView):
    queryset = EducationalModule.objects.all()
    serializer_class = EducationalModuleSerializer
    permission_classes = [IsTeacherOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class EducationalModuleUpdateView(generics.UpdateAPIView):
    queryset = EducationalModule.objects.all()
    serializer_class = EducationalModuleSerializer
    permission_classes = [IsTeacherOrReadOnly]


class EducationalModuleDeleteView(generics.DestroyAPIView):
    queryset = EducationalModule.objects.all()
    serializer_class = EducationalModuleSerializer
    permission_classes = [IsTeacherOrReadOnly]


# Материалы
class MaterialListView(generics.ListAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    permission_classes = [permissions.IsAuthenticated]


class MaterialDetailView(generics.RetrieveAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    permission_classes = [permissions.IsAuthenticated]


class MaterialCreateView(generics.CreateAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    permission_classes = [IsTeacherOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)


class MaterialUpdateView(generics.UpdateAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    permission_classes = [IsTeacherOrReadOnly]


class MaterialDeleteView(generics.DestroyAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    permission_classes = [IsTeacherOrReadOnly]


# Записи на модули
class EnrollmentListView(generics.ListAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        return Enrollment.objects.filter(student=self.request.user)


class EnrollmentDetailView(generics.RetrieveAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        return Enrollment.objects.filter(student=self.request.user)


class EnrollmentCreateView(generics.CreateAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsStudent]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


class EnrollmentUpdateView(generics.UpdateAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        return Enrollment.objects.filter(student=self.request.user)


class EnrollmentDeleteView(generics.DestroyAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        return Enrollment.objects.filter(student=self.request.user)
