from rest_framework.serializers import ModelSerializer
from .models import Attendance


class AttendanceSerializer(ModelSerializer):
    class Meta:
        model = Attendance
        fields = "__all__"
