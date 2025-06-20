from rest_framework import permissions


class IsTeacherOrReadOnly(permissions.BasePermission):
    """
    Преподаватели могут создавать и редактировать.
    Остальные пользователи могут только просматривать.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_teacher


class IsStudent(permissions.BasePermission):
    """
    Студенты могут просматривать и записываться на модули.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_student
