from django.contrib import admin
from django.urls import path, include

from holiday.views import get_holidays

urlpatterns = [
    path("admin/", admin.site.urls),
    path("rest-auth/", include("rest_auth.urls")),
    path("api/", include("attendance.urls")),
    path("api/", include("employee.urls")),
    path("api/holidays/", get_holidays)
]
