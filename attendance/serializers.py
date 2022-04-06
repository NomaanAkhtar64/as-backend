from rest_framework import serializers
from .models import Attendance
import datetime


class AttendanceSerializer(serializers.ModelSerializer):
    employee_status = serializers.SerializerMethodField()

    def get_employee_status(self, obj):
        if obj.joining_date == None:
            return "Active"
        if (
            obj.joining_date
            > datetime.datetime.now(tz=datetime.timezone.tzname("Asia/Karachi")).date()
        ):
            return "Active"
        return "Ex-Employee"

    class Meta:
        model = Attendance
        fields = (
            "id",
            "first_name",
            "last_name",
            "wage_per_hour",
            "joining_date",
            "leaving_date",
            "employee_status",
        )
