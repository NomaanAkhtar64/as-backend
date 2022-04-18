from requests import Response
from rest_framework.decorators import api_view

from holiday.models import Holiday
from .serializers import HolidaySerializer
from rest_framework import status
from rest_framework.response import Response
import datetime as dt
from calendar import monthrange


@api_view(["GET"])
def get_holidays(request):
    if "viewmode" in request.GET:
        if request.GET["viewmode"] == "Month":
            today = dt.datetime.now()
            return Response(
                data={
                    "holidays": HolidaySerializer(
                        Holiday.objects.filter(date__month=today.month), many=True
                    ).data,
                    "month_days": monthrange(today.year, today.month)[1],
                },
                status=status.HTTP_200_OK,
            )

    return Response(
        data=HolidaySerializer(Holiday.objects.all(), many=True).data,
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
def create_holiday(request):
    serializer = HolidaySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )

    return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)
