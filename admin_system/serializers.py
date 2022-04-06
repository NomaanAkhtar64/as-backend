from rest_framework import serializers
from django.contrib.auth.models import User
from employee.models import Employee


class UserDetailSerializer(serializers.ModelSerializer):
    employee_id = serializers.SerializerMethodField()

    def get_employee_id(self, obj):
        try:
            return Employee.objects.get(user__id=obj.pk).pk
        except Employee.DoesNotExist:
            return None

    class Meta:
        model = User
        fields = ["is_staff", "employee_id", "is_superuser"]
