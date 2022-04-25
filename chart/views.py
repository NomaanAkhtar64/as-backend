from rest_framework.views import Response
from rest_framework.decorators import api_view
from rest_framework import status
import datetime as dt
from django.conf import settings
from backports.zoneinfo import ZoneInfo
import calendar
from attendance.models import Attendance
from employee.models import Employee
import random


def get_bar_labels(currentDate):
    return [calendar.month_name[i] for i in range(1, currentDate.month + 1)]


def get_avg_hrs_chart(currentDate):
    data = []
    for m in range(1, currentDate.month + 1):
        data.append(
            Attendance.hours_worked(
                Attendance.objects.filter(date__year=currentDate.year, date__month=m)
            )
        )

    return {
        "title": "Average Hours Worked",
        "key": "bhw",
        "background_color": "rgba(53, 162, 235, 0.5)",
        "data": data,
    }


def get_avg_hrs_chart(currentDate):
    data = []
    for m in range(1, currentDate.month + 1):
        data.append(
            Attendance.hours_worked(
                Attendance.objects.filter(date__year=currentDate.year, date__month=m)
            )
        )

    return {
        "title": "Average Hours Worked",
        "key": "bhw",
        "background_color": "rgb(62, 57, 212)",
        "data": data,
    }


def get_attendance_percentage_chart(currentDate):
    data = []
    ecount = Employee.objects.count()
    for m in range(1, currentDate.month + 1):
        presents = Attendance.presents(
            Attendance.objects.filter(date__year=currentDate.year, date__month=m)
        )
        wdays = Attendance.working_days(year=currentDate.year, month=m)
        if wdays != 0 and ecount != 0:
            data.append(presents / (wdays * ecount) * 100)
    return {
        "title": "Average Attendance %",
        "key": "bap",
        "background_color": "rgb(219, 88, 92)",
        "data": data,
    }


COLORS = [
    "rgba(235, 64, 52)",
    "rgba(48, 110, 227)",
    "rgb(217, 189, 52)",
    "rgb(52, 217, 101)",
    "rgb(88, 56, 207)",
    "rgb(209, 132, 61)",
    "rgb(209, 61, 103)",
]


def get_hours_worked_chart(currentMonth):
    data = []
    labels = []
    background_colors = []

    for employee in Employee.objects.all():
        labels.append(
            str(employee),
        )
        data.append(
            Attendance.hours_worked(
                Attendance.objects.filter(employee=employee, date__month=currentMonth)
            )
        )
        background_colors.append(random.choice(COLORS))

    return {
        "title": "Hours Worked",
        "key": "phw",
        "labels": labels,
        "data": data,
        "background_colors": background_colors,
    }


def get_present_chart(currentMonth):
    data = []
    labels = []
    background_colors = []

    for employee in Employee.objects.all():
        labels.append(
            str(employee),
        )
        data.append(
            Attendance.presents(
                Attendance.objects.filter(employee=employee, date__month=currentMonth)
            )
        )
        background_colors.append(random.choice(COLORS))

    return {
        "title": "Presents",
        "key": "ppr",
        "labels": labels,
        "data": data,
        "background_colors": background_colors,
    }


@api_view(["GET"])
def get_chart(request):
    currentDate = dt.datetime.now(tz=ZoneInfo(settings.TIME_ZONE))
    chart_data = {
        "bar": [
            get_avg_hrs_chart(currentDate),
            get_attendance_percentage_chart(currentDate),
        ],
        "pie": [
            get_hours_worked_chart(currentDate.month),
            get_present_chart(currentDate.month),
        ],
        "month_label": get_bar_labels(currentDate),
    }
    return Response(data=chart_data, status=status.HTTP_200_OK)
