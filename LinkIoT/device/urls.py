from rest_framework.routers import DefaultRouter

from .views import DeviceViewSet, CategoryViewSet

router = DefaultRouter()

router.register('devices', DeviceViewSet, basename='devices')
router.register('categories', CategoryViewSet, basename='categories')

urlpatterns = router.urls
