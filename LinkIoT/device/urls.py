from rest_framework.routers import DefaultRouter

from .views import DeviceViewSet, CategoryViewSet, StreamViewSet, ChartViewSet

router = DefaultRouter()

router.register('devices', DeviceViewSet, basename='devices')
router.register('categories', CategoryViewSet, basename='categories')
router.register('streams', StreamViewSet, basename='streams')
router.register('charts', ChartViewSet, basename='charts')

urlpatterns = router.urls
