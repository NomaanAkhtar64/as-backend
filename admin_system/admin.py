from django.contrib import admin
from .models import AdminConfig, WorkingDay


admin.site.register(WorkingDay)
admin.site.register(AdminConfig)
