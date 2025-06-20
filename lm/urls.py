from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

from lm.apps import LmConfig
from lm.views import (
    CourseCreateView,
    CourseDeleteView,
    CourseDetailView,
    CourseListView,
    CourseUpdateView,
    EducationalModuleCreateView,
    EducationalModuleDeleteView,
    EducationalModuleDetailView,
    EducationalModuleListView,
    EducationalModuleUpdateView,
    EnrollmentCreateView,
    EnrollmentDeleteView,
    EnrollmentDetailView,
    EnrollmentListView,
    EnrollmentUpdateView,
    MaterialCreateView,
    MaterialDeleteView,
    MaterialDetailView,
    MaterialListView,
    MaterialUpdateView,
)

app_name = LmConfig.name

schema_view = get_schema_view(
    openapi.Info(
        title="Learning Modules API",
        default_version="v1",
        description="API for learning modules platform",
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path("courses/", CourseListView.as_view(), name="course-list"),
    path("courses/<int:pk>/", CourseDetailView.as_view(), name="course-detail"),
    path("courses/create/", CourseCreateView.as_view(), name="course-create"),
    path("courses/<int:pk>/update/", CourseUpdateView.as_view(), name="course-update"),
    path("courses/<int:pk>/delete/", CourseDeleteView.as_view(), name="course-delete"),
    path("modules/", EducationalModuleListView.as_view(), name="module-list"),
    path("modules/<int:pk>/", EducationalModuleDetailView.as_view(), name="module-detail"),
    path("modules/create/", EducationalModuleCreateView.as_view(), name="module-create"),
    path("modules/<int:pk>/update/", EducationalModuleUpdateView.as_view(), name="module-update"),
    path("modules/<int:pk>/delete/", EducationalModuleDeleteView.as_view(), name="module-delete"),
    path("materials/", MaterialListView.as_view(), name="material-list"),
    path("materials/<int:pk>/", MaterialDetailView.as_view(), name="material-detail"),
    path("materials/create/", MaterialCreateView.as_view(), name="material-create"),
    path("materials/<int:pk>/update/", MaterialUpdateView.as_view(), name="material-update"),
    path("materials/<int:pk>/delete/", MaterialDeleteView.as_view(), name="material-delete"),
    path("enrollments/", EnrollmentListView.as_view(), name="enrollment-list"),
    path("enrollments/<int:pk>/", EnrollmentDetailView.as_view(), name="enrollment-detail"),
    path("enrollments/create/", EnrollmentCreateView.as_view(), name="enrollment-create"),
    path("enrollments/<int:pk>/update/", EnrollmentUpdateView.as_view(), name="enrollment-update"),
    path("enrollments/<int:pk>/delete/", EnrollmentDeleteView.as_view(), name="enrollment-delete"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
