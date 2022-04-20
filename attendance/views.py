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
        if "approved" in self.request.query_params:
            return Leave.objects.filter(approved=self.request.query_params['approved'])
        return Leave.objects.all()
