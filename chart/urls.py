from django.urls import path
from .views import get_chart

urlpatterns = [path("chart-data/", get_chart)]
