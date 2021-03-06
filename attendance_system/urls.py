from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("rest-auth/", include("rest_auth.urls")),
    path("api/", include("attendance.urls")),
    path("api/", include("employee.urls")),
    path("api/", include("holiday.urls")),
    path("api/", include("chart.urls")),
]

admin.site.site_header = "Pi-Tendance Admin"
admin.site.index_title = "Pi-Tendance Features"
