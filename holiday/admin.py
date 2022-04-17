from django.contrib import admin

from holiday.models import Holiday


class HolidayAdmin(admin.ModelAdmin):
    list_display = ["name", "repeats", "date"]
    search_fields = ["name", "date"]


admin.site.register(Holiday, HolidayAdmin)
