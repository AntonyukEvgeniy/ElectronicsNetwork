from rest_framework import permissions


class IsActiveUser(permissions.BasePermission):
    """
    Доступ разрешён только активным сотрудникам (is_active=True и is_staff=True).
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_active
            and (not getattr(view, "staff_required", False) or request.user.is_staff)
        )
