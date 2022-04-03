from django.contrib import admin
from .models import AdminConfig, WorkingDay


class WorkingDayAdmin(admin.ModelAdmin):
    list_display = ["day_name", "updated_at"]


admin.site.register(WorkingDay, WorkingDayAdmin)
admin.site.register(AdminConfig)
