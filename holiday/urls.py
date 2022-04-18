from django.urls import path
from holiday.views import get_holidays, create_holiday

urlpatterns = [
    path("holidays/", get_holidays),
    path("holidays/create/", create_holiday),
]
