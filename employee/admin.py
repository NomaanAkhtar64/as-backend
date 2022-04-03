from django.contrib import admin
from .models import Employee


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["name", "gross_salary"]


admin.site.register(Employee, EmployeeAdmin)
