from datetime import datetime
from django.db import models
from employee.models import Employee

ATTENDANCE_CHOICES = [("Paid Leave", "Paid Leave"), ("Present", "Present")]

# Create your models here.
class Attendance(models.Model):
    employee = models.ForeignKey(to=Employee, on_delete=models.PROTECT)
    date = models.DateField(auto_created=True)
    status = models.CharField(max_length=10, choices=ATTENDANCE_CHOICES)
    checked_in = models.TimeField(auto_created=True)
    checked_out = models.TimeField(null=True, blank=True)

    @classmethod
    def has_marked_todays_attendance(employee):
        try:
            Attendance.objects.get(employee=employee, date=datetime.now())
            return True
        except Attendance.DoesNotExist:
            return False