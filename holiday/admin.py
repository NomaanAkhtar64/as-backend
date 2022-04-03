from django.contrib import admin

from holiday.models import Holiday


class HolidayAdmin(admin.ModelAdmin):
    list_display = []


admin.site.register(Holiday, HolidayAdmin)
