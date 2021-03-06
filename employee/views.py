# MODULES
import datetime as dt
from backports.zoneinfo import ZoneInfo
from django.views import View
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.models import User
import secrets

# LOCAL
from admin_system.models import AdminConfig, Company
from attendance.serializers import AttendanceSerializer
from employee.permissions import IsOwnerOrAdmin
from .models import Employee, PartialEmployee
from attendance.models import Attendance
from .serializers import EmployeeSerializer, PartialEmployeeSerializer
from .utils import html_to_pdf

tz = ZoneInfo(settings.TIME_ZONE)

MONTH = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December",
}


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = User.objects.get(pk=request.data["user"])
        user.is_active = True
        user.save()
        return super().create(request, *args, **kwargs)


class PartialEmployeeViewSet(viewsets.ModelViewSet):
    queryset = PartialEmployee.objects.all()
    serializer_class = PartialEmployeeSerializer
    permission_classes = [IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        try:
            if "complete" in request.GET:
                User.objects.get(
                    pk=PartialEmployee.objects.get(pk=kwargs["pk"]).user.id
                ).delete()
            else:
                PartialEmployee.objects.get(pk=kwargs["pk"]).delete()
        except PartialEmployee.DoesNotExist:
            return Response(data="ID not exists", status=status.HTTP_200_OK)
        return Response(data="Deleted", status=status.HTTP_200_OK)


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


@api_view(["GET"])
@permission_classes([IsOwnerOrAdmin])
def employee_attendance(request, id=None):
    if id is None:
        employee = Employee.objects.get(user=request.user.id)
    else:
        employee = Employee.objects.get(id=id)

    view_mode = request.GET.get("viewmode", None)

    date = dt.datetime.now(tz=tz).date()

    if view_mode == "Month":
        return Response(data=Attendance.months(employee), status=status.HTTP_200_OK)

    elif view_mode == "Year":
        return Response(data=Attendance.years(employee), status=status.HTTP_200_OK)

    else:
        # LAST 7 DAYS
        attendance = (
            Attendance.objects.filter(
                employee=employee,
                date__gte=(date - dt.timedelta(days=7)),
                date__lte=date,
            )
            .exclude(checked_out=None)
            .order_by("-date")
        )
        serialized = AttendanceSerializer(attendance, many=True)

        return Response(data=serialized.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def markable_attendance(request):
    today = dt.datetime.now(tz=tz).date()
    output = {"date": today, "attendance": []}
    for employee in Employee.objects.all():
        outobj = {
            "id": employee.id,
            "name": str(employee),
            "has_checkin": False,
            "has_checkout": False,
        }
        try:
            attendance = Attendance.objects.get(date=today, employee=employee)
            outobj["has_checkin"] = attendance.checked_in != None
            outobj["has_checkout"] = attendance.checked_out != None

            if not (outobj["has_checkin"] and outobj["has_checkout"]):
                output["attendance"].append(outobj)

        except Attendance.DoesNotExist:
            output["attendance"].append(outobj)

    return Response(data=output, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAdminUser])
def mark_attendance(request, id):
    employee = Employee.objects.get(id=id)
    data = request.data
    date = dt.datetime.strptime(data["date"], "%Y-%m-%d").date()
    try:
        attendance = Attendance.objects.get(employee=employee, date=date)

    except Attendance.DoesNotExist:
        attendance = Attendance(employee=employee, date=date)

    if "checkin" in data:
        attendance.checked_in = data["checkin"]
    if "checkout" in data:
        attendance.checked_out = data["checkout"]

    attendance.save()
    return Response(
        data=f'Marked Attendance for Employee: {employee} for Date: {date.strftime("%d-%m-%Y")}'
    )


@api_view(["POST"])
def employee_signup(request):
    email = request.data["email"]
    password = request.data["password"]
    device = request.data["device"]
    first_name = request.data["first_name"]
    last_name = request.data["last_name"]
    dob = request.data["date_of_birth"]
    contact = request.data["contact"]
    user = User.objects.create_user(secrets.token_hex(16), email, password)
    user.is_active = False
    user.save()
    PartialEmployee.objects.create(
        user=user,
        first_name=first_name,
        last_name=last_name,
        brand_of_device=device,
        date_of_birth=dob,
        contact=contact,
        ip=get_client_ip(request),
    )

    return Response(data="REGISTERED EMPLOYEE", status=status.HTTP_200_OK)


class GeneratePdf(View):
    def get(self, request, year, id, month=None):
        employee = Employee.objects.get(id=id)
        attendance = Attendance.objects.all()
        company = Company.objects.all()[0]
        d = Attendance.by_month(employee, month, year)
        salary = d["hours_worked"] * employee.wage_per_hour
        month_text = None
        if month:
            month_text = MONTH[month]
        open("templates/temp.html", "w").write(
            render_to_string(
                "employee_report.html",
                {
                    "employee": employee,
                    "attendance": attendance,
                    "company": company,
                    "month": month_text,
                    "year": year,
                    "presents": d["presents"],
                    "absents": d["absents"],
                    "hours_worked": d["hours_worked"],
                    "salary": salary,
                },
            )
        )

        pdf = html_to_pdf("temp.html")
        return HttpResponse(pdf, content_type="application/pdf")
