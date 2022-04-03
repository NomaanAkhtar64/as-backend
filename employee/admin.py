from django.contrib import admin
from .models import Employee


class EmployeeAdmin(admin.ModelAdmin):
    list_display = [
        "first_name",
        "last_name",
        "wage_per_hour",
        "mac_address",
    ]


admin.site.register(Employee, EmployeeAdmin)
