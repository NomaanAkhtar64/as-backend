from django.contrib import admin
from .models import Attendance


class AttendanceAdmin(admin.ModelAdmin):
    list_display = ["employee", "date", "checked_in", "checked_out"]
    list_filter = ('employee', 'status', 'date')
    search_fields = ['employee__username']


admin.site.register(Attendance, AttendanceAdmin)
