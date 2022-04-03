from datetime import datetime
from django.db import models
from employee.models import Employee

ATTENDANCE_CHOICES = [("Paid Leave", "Paid Leave"), ("Present", "Present")]


class Attendance(models.Model):
    employee = models.ForeignKey(to=Employee, on_delete=models.PROTECT)
    date = models.DateField(auto_created=True)
    status = models.CharField(max_length=10, choices=ATTENDANCE_CHOICES)
    checked_in = models.TimeField(null=True, blank=True)
    checked_out = models.TimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    @classmethod
    def has_marked_todays_attendance(employee):
        try:
            Attendance.objects.get(employee=employee, date=datetime.now())
            return True
        except Attendance.DoesNotExist:
            return False

    def __str__(self):
        return f"Attendance: {self.date} {self.employee.first_name} {self.employee.last_name}"
