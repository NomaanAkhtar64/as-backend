from calendar import calendar
from datetime import datetime
from backports.zoneinfo import ZoneInfo
from django.conf import settings
from django.db import models
from attendance.filters import (
    MonthAttendance,
    MonthAttendanceSerializer,
    YearAttendance,
    YearAttendanceSerializer,
)
from employee.models import Employee
from holiday.models import Holiday
from admin_system.models import AdminConfig, WorkingDay
import calendar

ATTENDANCE_CHOICES = [("Early", "Early"), ("Present", "Present"), ("Late", "Late")]


def hrs_diff(start, end):
    delta = (
        (end.hour - start.hour) * 60
        + end.minute
        - start.minute
        + (end.second - start.second) / 60.0
    )
    return round(delta / 60)


def min_diff(start, end):
    delta = (
        (end.hour - start.hour) * 60
        + end.minute
        - start.minute
        + (end.second - start.second) / 60.0
    )
    return round(delta)


class Leave(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    reason = models.CharField(max_length=255)
    date = models.DateField()
    msg = models.TextField()
    approved = models.BooleanField(default=False)

    def __str__(self):
        return str(self.employee) + " Leave"


class Attendance(models.Model):
    employee = models.ForeignKey(to=Employee, on_delete=models.CASCADE)
    date = models.DateField(auto_created=True)
    status = models.CharField(max_length=10, choices=ATTENDANCE_CHOICES)
    checked_in = models.TimeField()
    checked_out = models.TimeField(null=True, blank=True)

    def save(self, *arg, **kwargs):
        if not self.id:
            config = AdminConfig.objects.all()[0]
            check_in = datetime.strptime(self.checked_in, "%H:%M:%S").time()
            if check_in < config.start_time:
                self.status = "Early"
            else:
                if min_diff(config.start_time, check_in) <= 30:
                    self.status = "Present"
                else:
                    self.status = "Late"

        super().save(*arg, **kwargs)

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
        config = AdminConfig.objects.all()[0]
        if len(queryset) == 0:
            return 0
        for att in queryset:
            if att.checked_out:
                if att.status == "Present" or att.status == "Early":
                    hours_worked += hrs_diff(config.start_time, att.checked_out)
                else:
                    hours_worked += hrs_diff(att.checked_in, att.checked_out)
        return hours_worked

    @classmethod
    def presents(cls, queryset):
        presents = 0
        for att in queryset:
            if att.status == "Present":
                presents += 1

        return presents

    @classmethod
    def months(cls, employee):
        att = cls.objects.filter(employee=employee)
        if len(att) == 0:
            return []
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
    def working_days(cls, month, year):
        working_days = 0
        today = datetime.now()
        wdays = WorkingDay.day_list()
        for week in calendar.Calendar().monthdays2calendar(
            year=int(year), month=int(month)
        ):
            for (dom, dow) in week:
                if dom == 0:
                    continue
                if today.month == month and dom > today.day:
                    continue
                if (
                    Holiday.objects.filter(
                        date__month=month,
                        date__year=year,
                        date__day=dom,
                        repeats=False,
                    ).count()
                    > 0
                ):
                    continue

                if (
                    Holiday.objects.filter(
                        date__month=month, date__day=dom, repeats=True
                    ).count()
                    > 0
                ):
                    continue

                if dow in wdays:
                    working_days += 1

        return working_days

    @classmethod
    def absents_by_month(cls, employee, month, year, today, wdays):
        absents = 0
        for week in calendar.Calendar().monthdays2calendar(
            year=int(year), month=int(month)
        ):
            for (dom, dow) in week:
                if dom == 0 or dow not in wdays:
                    continue

                if today.month == month:
                    if dom > today.day:
                        continue

                if (
                    Holiday.objects.filter(
                        date__month=month, date__year=year, date__day=dom, repeats=False
                    ).count()
                    > 0
                ):
                    continue

                if (
                    Holiday.objects.filter(
                        date__month=month, date__day=dom, repeats=True
                    ).count()
                    > 0
                ):
                    continue

                if (
                    Leave.objects.filter(
                        employee=employee,
                        date__month=month,
                        date__year=year,
                        date__day=dom,
                        approved=True,
                    ).count()
                    > 0
                ):
                    continue

                if (
                    Attendance.objects.filter(
                        date=datetime(
                            int(year),
                            int(month),
                            dom,
                            tzinfo=ZoneInfo(settings.TIME_ZONE),
                        ),
                        employee=employee,
                    ).count()
                    == 0
                ):
                    absents += 1

        return absents

    @classmethod
    def absents(cls, employee, month, year):
        absents = 0
        today = datetime.now()
        wdays = WorkingDay.day_list()
        if month == None:
            if today.year == year:
                mcount = today.month
            else:
                mcount = 12

            for i in range(mcount):
                absents += cls.absents_by_month(employee, i + 1, year, today, wdays)

        else:
            absents += cls.absents_by_month(employee, month, year, today, wdays)

        return absents

    @classmethod
    def by_month(cls, employee, month, year):
        presents = 0
        hours_worked = 0
        absents = 0

        if month == None:
            att = cls.objects.filter(
                date__year=year,
                employee=employee,
            )
        else:
            att = cls.objects.filter(
                date__year=year,
                date__month=month,
                employee=employee,
            )

        if len(att) > 0:
            hours_worked = cls.hours_worked(att)
            presents = cls.presents(att)
            absents = cls.absents(employee, month, year)
        return {"presents": presents, "hours_worked": hours_worked, "absents": absents}

    @classmethod
    def years(cls, employee):
        att = cls.objects.filter(employee=employee)
        if len(att) == 0:
            return []
        latest = att.order_by("-date")[0].date
        oldest = employee.joining_date

        years = (latest.year - oldest.year) + 1
        y_atts = []
        for y in range(years):
            year = oldest.year + y

            queryset = cls.objects.filter(
                date__year=year,
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
