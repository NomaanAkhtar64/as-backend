from rest_framework import serializers
from .models import Attendance, Leave
from employee.serializers import EmployeeSerializer


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = "__all__"


class LeaveSerializer(serializers.ModelSerializer):
    employee_detail = serializers.SerializerMethodField('get_employee', read_only=True)

    def get_employee(self, obj):
        return EmployeeSerializer(obj.employee).data

    class Meta:
        model = Leave
        fields = "__all__"
