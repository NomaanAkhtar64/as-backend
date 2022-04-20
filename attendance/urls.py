from rest_framework import routers
from .views import AttendanceViewset, LeaveViewset

router = routers.SimpleRouter()
router.register(r"attendance", AttendanceViewset)
router.register(r"request/leave", LeaveViewset, basename="request-leave")

urlpatterns = router.urls
