from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Attendance, Leave
from .serializers import AttendanceSerializer, LeaveSerializer


class AttendanceViewset(ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]


class LeaveViewset(ModelViewSet):
    serializer_class = LeaveSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Leave.objects.all()
        if "approved" in self.request.query_params:
            queryset = queryset.filter(approved=self.request.query_params["approved"])
        if "employee" in self.request.query_params:
            queryset = queryset.filter(employee=self.request.query_params["employee"])
        return queryset
