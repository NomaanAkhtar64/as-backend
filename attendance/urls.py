from django.urls import path
from . import views

urlpatterns = [
    path("check", views.check_attendance),
    path("mark", views.mark_attendance),
]
