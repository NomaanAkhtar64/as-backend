from django.urls import path
from rest_framework import routers
from .views import (
    EmployeeViewSet,
    employee_attendance,
    markable_attendance,
    mark_attendance,
)

router = routers.SimpleRouter()
router.register(r"employee", EmployeeViewSet)

urlpatterns = [
    path("markable_attendance/", markable_attendance),
    path("mark_attendance/<int:id>/", mark_attendance),
    path("employee_attendance/", employee_attendance),
    path("employee/<int:id>/attendance/", employee_attendance),
] + router.urls
