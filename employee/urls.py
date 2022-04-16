from django.urls import path
from rest_framework import routers

from .views import (
    EmployeeViewSet,
    PartialEmployeeViewSet,
    employee_attendance,
    markable_attendance,
    mark_attendance,
    employee_signup,
    GeneratePdf,
)

router = routers.SimpleRouter()
router.register(r"employee", EmployeeViewSet)
router.register(r"registrations", PartialEmployeeViewSet)

urlpatterns = [
    path("markable_attendance/", markable_attendance),
    path("mark_attendance/<int:id>/", mark_attendance),
    path("employee_attendance/", employee_attendance),
    path("employee_signup/", employee_signup),
    path("employee/<int:id>/attendance/", employee_attendance),
    path("report/<int:id>/<int:year>/<int:month>/", GeneratePdf.as_view()),
    path("report/<int:id>/<int:year>/", GeneratePdf.as_view()),
] + router.urls
