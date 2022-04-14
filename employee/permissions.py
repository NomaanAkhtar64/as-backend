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

        if "/api/employee/" in request.path:
            employee_id = int(
                request.path.replace("/api/employee/", "").replace("/attendance/", "")
            )
            employee = Employee.objects.get(id=employee_id)
            if employee.user != request.user.id:
                return False

        return True
