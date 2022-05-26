from datetime import datetime, timedelta

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from base.base_viewsets import BaseModelViewSet
from .models import DeviceCategory, Device, Stream, Chart
from .serializers import (
    DeviceSerializer,
    DeviceDetailSerializer,
    DeviceCategorySerializer,
    StreamSerializer,
    ChartSerializer,
    TriggerSerializer,
)


class DeviceViewSet(BaseModelViewSet):
    lookup_field = "id"
    serializer_class = DeviceSerializer
    filter_fields = ["category"]
    ordering_fields = ["sequence", "created_time"]
    ordering = ["sequence", "-created_time"]
    queryset = Device.objects

    def get_serializer_class(self):
        if self.request.method == "GET":
            return DeviceSerializer
        else:
            return DeviceDetailSerializer

    @action(methods=["get"], detail=True)
    def streams(self, request, *args, **kwargs):
        device = self.get_object()
        serializer = StreamSerializer(device.streams, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = DeviceDetailSerializer(instance, context={"request": request})
        return Response(serializer.data)

    @action(methods=["post"], detail=True)
    def upload(self, request, *args, **kwargs):
        device = self.get_object()
        device.image = request.data.get("file")
        device.save()
        serializer = DeviceDetailSerializer(device, context={"request": request})
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = DeviceCategorySerializer
    lookup_field = "id"
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ["sequence", "created_time"]
    ordering = ["sequence", "-created_time"]
    queryset = DeviceCategory.objects

    def perform_create(self, serializer):
        serializer.save(create_user=self.request.user)

    @action(methods=["put"], detail=False)
    def sort(self, request, *args, **kwargs):
        for cid in request.data:
            category = DeviceCategory.objects.filter(
                id=cid, create_user=request.user
            ).first()
            if category:
                category.sequence = request.data[cid]
                category.save()
        return Response({})


class StreamViewSet(BaseModelViewSet):
    serializer_class = StreamSerializer
    lookup_field = "id"
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ["device", "name", "data_type"]
    queryset = Stream.objects


class ChartViewSet(BaseModelViewSet):
    lookup_field = "id"
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ["device", "name"]
    ordering_fields = ["sequence", "-created_time"]
    ordering = ["sequence", "-created_time"]
    queryset = Chart.objects
    serializer_class = ChartSerializer

    def perform_create(self, serializer):
        serializer.save(create_user=self.request.user)

    @action(methods=["get"], detail=True)
    def data(self, request, *args, **kwargs):
        """
        获取图表数据
        """
        start_time = self.request.query_params.get(
            "start_time", datetime.now() + timedelta(days=7)
        )
        end_time = self.request.query_params.get("end_time", datetime.now())
        # TODO: 从数据模型中取出前端所需要的dataset


class TriggerViewSet(viewsets.ModelViewSet):
    serializer_class = TriggerSerializer
    lookup_field = "id"
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ("device", "stream")

    def get_queryset(self):
        return self.request.user.triggers
