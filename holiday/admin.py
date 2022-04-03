from django.contrib import admin

from holiday.models import Holiday


class HolidayAdmin(admin.ModelAdmin):
    list_display = ["name", "repeats", "date", "type", "created_at", "updated_at"]
    list_filter = ('type', 'repeats',)
    search_fields = ['name', 'date']


admin.site.register(Holiday, HolidayAdmin)
