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


class PartialEmployeeAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "first_name",
        "last_name",
        "brand_of_device",
        "applied"
    ]
    list_filter = ("brand_of_device",)


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(PartialEmployee, PartialEmployeeAdmin)
