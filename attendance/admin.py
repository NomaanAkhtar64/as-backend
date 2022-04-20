from django.contrib import admin
from .models import Attendance, Leave


class AttendanceAdmin(admin.ModelAdmin):
    list_display = ["employee", "date", "checked_in", "checked_out"]
    list_filter = ('employee', 'status', 'date')
    search_fields = ['employee__username']


class LeaveAdmin(admin.ModelAdmin):
    list_display = ['employee', 'reason', 'date', 'approved']
    list_filter = ['employee', 'approved', 'date']
    search_fields = ['employee__username', 'reason']


admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Leave, LeaveAdmin)
