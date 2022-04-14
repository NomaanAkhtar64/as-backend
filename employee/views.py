# MODULES
import datetime as dt
from zoneinfo import ZoneInfo
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from django.conf import settings

# LOCAL
from admin_system.models import AdminConfig
from attendance.serializers import AttendanceSerializer
from employee.permissions import IsOwnerOrAdmin
from .models import Employee
from attendance.models import Attendance
from .serializers import EmployeeSerializer

tz = ZoneInfo(settings.TIME_ZONE)


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]


@api_view(["GET"])
@permission_classes([IsOwnerOrAdmin])
def employee_attendance(request, id=None):
    if id == None:
        employee = Employee.objects.get(user=request.user.id)
    else:
        employee = Employee.objects.get(id=id)

    view_mode = request.GET.get("viewmode", None)

    date = dt.datetime.now(tz=tz).date()
    if view_mode == "7days":
        days = 7
    elif view_mode == "Month":
        days = 30
    elif view_mode == "Year":
        days = 365
    else:
        days = 0
    attendance = Attendance.objects.filter(
        employee=employee,
        date__gte=(date - dt.datetime.timedelta(days=days)),
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
