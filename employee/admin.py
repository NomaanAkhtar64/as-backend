from django.contrib import admin
from .models import Employee


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["name", "gross_salary", "mac_address"]


admin.site.register(Employee, EmployeeAdmin)
