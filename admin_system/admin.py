from django.contrib import admin
from .models import AdminConfig, WorkingDay, Company


class WorkingDayAdmin(admin.ModelAdmin):
    list_display = ["day"]


admin.site.register(WorkingDay, WorkingDayAdmin)
admin.site.register(AdminConfig)
admin.site.register(Company)
