from datetime import datetime, timedelta

from guardian.shortcuts import assign_perm, get_user_perms, get_objects_for_user
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend

from base.base_viewsets import BaseModelViewSet

from .models import Chart, Device, Stream, Trigger, DeviceCategory
from .serializers import (
    ChartSerializer,
    DeviceSerializer,
    StreamSerializer,
    TriggerSerializer,
    DeviceDetailSerializer,
    DeviceCategorySerializer,
)


class DeviceViewSet(BaseModelViewSet):
    lookup_field = "id"
    serializer_class = DeviceSerializer
    filter_fields = ["category"]
    ordering_fields = ["sequence", "created_time"]
    ordering = ["sequence", "-created_time"]

    # queryset = Device.objects

    def get_serializer_class(self):
        if self.request.method == "GET":
            return DeviceSerializer
        else:
            return DeviceDetailSerializer

    def get_queryset(self):
        return get_objects_for_user(self.request.user, perms="view_device", klass=Device)

    def perform_create(self, serializer):
        current_user = self.request.user
        device = serializer.save(create_user=current_user)
        assign_perm("control_device", current_user, device)
        assign_perm("add_device", current_user, device)
        assign_perm("view_device", current_user, device)
        assign_perm("change_device", current_user, device)
        assign_perm("delete_device", current_user, device)

    def perform_update(self, serializer):
        if not self.request.user.has_perm("change_device", serializer.instance):
            raise PermissionDenied("你没有修改该设备的权限")
        else:
            serializer.save(last_update_user=self.request.user)

    def perform_destroy(self, instance):
        if not self.request.user.has_perm("delete_device", instance):
            raise PermissionDenied("你没有删除该设备的权限")
        else:
            instance.delete()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = DeviceDetailSerializer(instance, context={"request": request})
        return Response(serializer.data)

    @action(methods=["post"], detail=True)
    def upload(self, request, *args, **kwargs):
        # 微信小程序上传文件是post方式，单独处理
        device = self.get_object()
        serializer = self.get_serializer(device, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @action(methods=["get"], detail=True)
    def streams(self, request, *args, **kwargs):
        device = self.get_object()
        serializer = StreamSerializer(device.streams, many=True)
        return Response(serializer.data)

    @action(methods=["get"], detail=True)
    def charts(self, request, *args, **kwargs):
        device = self.get_object()
        serializer = ChartSerializer(device.charts, many=True)
        return Response(serializer.data)

    @action(methods=["get"], detail=True)
    def triggers(self, request, *args, **kwargs):
        device = self.get_object()
        serializer = TriggerSerializer(device.triggers, many=True)
        return Response(serializer.data)

    @action(methods=["get"], detail=True)
    def perms(self, request, *args, **kwargs):
        device = self.get_object()
        perms = get_user_perms(request.user, device)
        return Response(perms)


class CategoryViewSet(BaseModelViewSet):
    serializer_class = DeviceCategorySerializer
    lookup_field = "id"
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ["sequence", "created_time"]
    ordering = ["sequence", "-created_time"]
    queryset = DeviceCategory.objects

    @action(methods=["put"], detail=False)
    def sort(self, request, *args, **kwargs):
        for cid in request.data:
            category = DeviceCategory.objects.filter(id=cid, create_user=request.user).first()
            if category:
                category.sequence = request.data[cid]
                category.save()
        return Response({})


class StreamViewSet(BaseModelViewSet):
    serializer_class = StreamSerializer
    lookup_field = "id"
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ["device", "name", "data_type", "show"]
    search_fields = ["device"]
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
        start_time = self.request.query_params.get("start_time", datetime.now() + timedelta(days=7))
        end_time = self.request.query_params.get("end_time", datetime.now())
        # TODO: 从数据模型中取出前端所需要的dataset


class TriggerViewSet(BaseModelViewSet):
    serializer_class = TriggerSerializer
    lookup_field = "id"
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ("device", "stream")
    queryset = Trigger.objects
