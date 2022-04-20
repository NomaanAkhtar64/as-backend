from rest_framework import serializers
from .models import Employee, PartialEmployee


class EmployeeSerializer(serializers.ModelSerializer):
    employee_status = serializers.SerializerMethodField()

    def get_employee_status(self, obj):
        return obj.status()

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
            "user",
            "date_of_birth",
        )


class PartialEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartialEmployee
        fields = "__all__"
