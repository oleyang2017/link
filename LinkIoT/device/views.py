from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import *


class DeviceViewSet(viewsets.ModelViewSet):

    serializer_class = DeviceSerializer
    lookup_field = 'device_id'
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ('category',)
    ordering_fields = ('sequence', 'id')

    def get_queryset(self):
        return self.request.user.devices


class CategoryViewSet(viewsets.ModelViewSet):

    serializer_class = DeviceCategorySerializer
    lookup_field = 'id'
    queryset = DeviceCategory.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ('sequence', 'id')

    def get_queryset(self):
        return self.request.user.device_categories

