from rest_framework.routers import DefaultRouter

from device.views.chart import ChartViewSet
from device.views.device import DeviceViewSet
from device.views.stream import StreamViewSet
from device.views.category import CategoryViewSet

router = DefaultRouter()

router.register("devices", DeviceViewSet, basename="devices")
router.register("categories", CategoryViewSet, basename="categories")
router.register("streams", StreamViewSet, basename="streams")
router.register("charts", ChartViewSet, basename="charts")

urlpatterns = router.urls
