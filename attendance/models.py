from datetime import datetime
from django.db import models
from attendance.filters import (
    MonthAttendance,
    MonthAttendanceSerializer,
    YearAttendance,
    YearAttendanceSerializer,
)
from employee.models import Employee

ATTENDANCE_CHOICES = [("Paid Leave", "Paid Leave"), ("Present", "Present")]


def hrs_diff(start, end):
    delta = (
        (end.hour - start.hour) * 60
        + end.minute
        - start.minute
        + (end.second - start.second) / 60.0
    )
    return round(delta / 60)


class Attendance(models.Model):
    employee = models.ForeignKey(to=Employee, on_delete=models.CASCADE)
    date = models.DateField(auto_created=True)
    status = models.CharField(max_length=10, choices=ATTENDANCE_CHOICES)
    checked_in = models.TimeField(null=True, blank=True)
    checked_out = models.TimeField(null=True, blank=True)

    @classmethod
    def has_marked_todays_attendance(employee):
        try:
            Attendance.objects.get(employee=employee, date=datetime.now())
            return True
        except Attendance.DoesNotExist:
            return False

    def __str__(self):
        return f"Attendance: {self.date} {self.employee.first_name} {self.employee.last_name}"

    @classmethod
    def hours_worked(cls, queryset):
        hours_worked = 0
        if len(queryset) == 0:
            return 0
        for att in queryset:
            hours_worked += hrs_diff(att.checked_in, att.checked_out)
        return hours_worked

    @classmethod
    def by_month(cls, employee):
        att = cls.objects.filter(employee=employee)
        latest = att.order_by("-date")[0].date
        oldest = employee.joining_date

        months = (latest.year - oldest.year) * 12 + (latest.month - oldest.month) + 1

        m_atts = []
        for m in range(months):
            month = oldest.month + m
            year = oldest.year
            if month > 12:
                year += 1
                month = month - 12

            queryset = cls.objects.filter(
                date__year__gte=year,
                date__month__gte=month,
                date__year__lte=year,
                date__month__lte=month,
                employee=employee,
            )

            m_atts.append(
                MonthAttendance(
                    year=year, month=month, hours_worked=cls.hours_worked(queryset)
                )
            )
        m_atts.reverse()
        serializer = MonthAttendanceSerializer(
            m_atts,
            many=True,
        )
        return serializer.data

    @classmethod
    def by_year(cls, employee):
        att = cls.objects.filter(employee=employee)
        latest = att.order_by("-date")[0].date
        oldest = employee.joining_date

        years = (latest.year - oldest.year) + 1
        y_atts = []
        for y in range(years):
            year = oldest.year + y

            queryset = cls.objects.filter(
                date__year__gte=year,
                date__year__lte=year,
                employee=employee,
            )

            y_atts.append(
                YearAttendance(year=year, hours_worked=cls.hours_worked(queryset))
            )

        y_atts.reverse()
        serializer = YearAttendanceSerializer(
            y_atts,
            many=True,
        )
        return serializer.data
