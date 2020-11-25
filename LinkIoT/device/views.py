from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import *


class DeviceViewSet(viewsets.ModelViewSet):

    serializer_class = DeviceSerializer
    lookup_field = 'id'
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ('category',)
    ordering_fields = ('sequence',)

    def get_queryset(self):
        return self.request.user.devices

    @action(methods=['get'], detail=True)
    def streams(self, request, *args, **kwargs):
        device = self.get_object()
        serializer = StreamSerializer(device.streams, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = DeviceDetailSerializer(instance)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):

    serializer_class = DeviceCategorySerializer
    lookup_field = 'id'
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ('sequence', 'id')

    def get_queryset(self):
        return self.request.user.device_categories


class StreamViewSet(viewsets.ModelViewSet):
    serializer_class = StreamSerializer
    lookup_field = 'id'
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ('device',)

    def get_queryset(self):
        return self.request.user.streams
