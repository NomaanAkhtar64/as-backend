from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Attendance
from .decorators import check_mac


@check_mac
@api_view(["POST"])
def check_attendance(request, **kwargs):
    if Attendance.has_marked_todays_attendance(kwargs["employee"]):
        return Response(data=True, status=status.HTTP_200_OK)
    return Response(data=False, status=status.HTTP_200_OK)


@check_mac
@api_view(["POST"])
def mark_attendance(request, **kwargs):
    Attendance.objects.create(employee=kwargs["employee"])
    return Response(data="Attendance Marked", status=status.HTTP_200_OK)
