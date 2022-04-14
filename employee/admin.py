from django.contrib import admin
from .models import Employee, PartialEmployee


class EmployeeAdmin(admin.ModelAdmin):
    list_display = [
        "first_name",
        "last_name",
        "wage_per_hour",
        "mac_address",
    ]
    list_filter = ("brand_of_device", "wage_per_hour")
    search_fields = ["first_name", "last_name", "mac_address"]


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(PartialEmployee)
