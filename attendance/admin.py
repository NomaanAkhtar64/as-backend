from django.contrib import admin
from .models import Attendance


class AttendanceAdmin(admin.ModelAdmin):
    list_display = ["employee", "date", "checked_in", "checked_out"]


admin.site.register(Attendance, AttendanceAdmin)
