from rest_framework.routers import DefaultRouter

from .views import ChartViewSet, DeviceViewSet, StreamViewSet, TriggerViewSet, CategoryViewSet

router = DefaultRouter()

router.register("devices", DeviceViewSet, basename="devices")
router.register("categories", CategoryViewSet, basename="categories")
router.register("streams", StreamViewSet, basename="streams")
router.register("charts", ChartViewSet, basename="charts")
router.register("triggers", TriggerViewSet, basename="triggers")

urlpatterns = router.urls
