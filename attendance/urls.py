from rest_framework import routers
from .views import AttendanceViewset

router = routers.SimpleRouter()
router.register(r"attendance", AttendanceViewset)

urlpatterns = router.urls
