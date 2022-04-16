# MODULES
import datetime as dt
from zoneinfo import ZoneInfo
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
from admin_system.models import AdminConfig
from attendance.serializers import AttendanceSerializer
from employee.permissions import IsOwnerOrAdmin
from .models import Employee, PartialEmployee
from attendance.models import Attendance
from .serializers import EmployeeSerializer, PartialEmployeeSerializer
from .utils import html_to_pdf

tz = ZoneInfo(settings.TIME_ZONE)


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]


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
        return Response(data=Attendance.by_month(employee), status=status.HTTP_200_OK)

    elif view_mode == "Year":
        return Response(data=Attendance.by_year(employee), status=status.HTTP_200_OK)

    else:
        # LAST 7 DAYS
        attendance = Attendance.objects.filter(
            employee=employee,
            date__gte=(date - dt.timedelta(days=7)),
            date__lte=date,
        ).order_by("-date")
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
    current_time = dt.datetime.now(tz=tz).time()
    employee = Employee.objects.get(id=id)
    data = request.data
    date = dt.datetime.strptime(data["date"], "%Y-%m-%d").date()

    try:
        attendance = Attendance.objects.get(employee=employee, date=date)

    except Attendance.DoesNotExist:
        attendance = Attendance.objects.create(employee=employee, date=date)

    if data["mark"] == "checkin":
        attendance.checked_in = current_time
    elif data["mark"] == "checkout":
        attendance.checked_out = current_time
    elif data["mark"] == "both":
        attendance.checked_in = current_time
        attendance.checked_out = AdminConfig.objects.all()[0].end_time
    else:
        return Response(
            data="mark option not a valid value", status=status.HTTP_400_BAD_REQUEST
        )
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
    def get(self, request, *args, **kwargs):
        data = Employee.objects.get(id=request.id)
        open("templates/temp.html", "w").write(
            render_to_string("employee_report.html", {"data": data})
        )
        # Converting the HTML template into a PDF file
        pdf = html_to_pdf("temp.html")
        return HttpResponse(pdf, content_type="application/pdf")
