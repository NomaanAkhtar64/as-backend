from rest_framework import routers
from .views import EmployeeViewSet

router = routers.SimpleRouter()
router.register(r"employee", EmployeeViewSet)

urlpatterns = router.urls
