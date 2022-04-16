from rest_framework.permissions import BasePermission, SAFE_METHODS

from employee.models import Employee


class IsOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.id == None:
            return False
        if not request.method in SAFE_METHODS:
            return False
        if request.user.is_staff:
            return True

        try:
            if "id" in view.kwargs:
                employee = Employee.objects.get(id=view.kwargs.get("id"))
                if employee.user.id != request.user.id:
                    return False
            return True

        except Employee.DoesNotExist:
            return False
