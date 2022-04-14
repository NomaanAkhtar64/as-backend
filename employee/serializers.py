from rest_framework import serializers
from .models import Employee, PartialEmployee
import datetime


class EmployeeSerializer(serializers.ModelSerializer):
    employee_status = serializers.SerializerMethodField()

    def get_employee_status(self, obj):
        if obj.leaving_date == None:
            return "Active"
        if obj.leaving_date > datetime.datetime.now(tz=datetime.timezone.utc).date():
            return "Active"
        return "Ex-Employee"

    class Meta:
        model = Employee
        fields = (
            "id",
            "first_name",
            "last_name",
            "wage_per_hour",
            "joining_date",
            "leaving_date",
            "employee_status",
        )


class PartialEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartialEmployee
        fields = "__all__"
