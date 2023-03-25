from guardian.shortcuts import assign_perm, get_user_perms, get_objects_for_user
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied

from base.base_viewsets import BaseModelViewSet
from device.models.chart import Chart
from device.models.device import Device
from device.serializers.chart import ChartDetailSerializer
from device.serializers.device import (
    DeviceListSerializer,
    DeviceDetailSerializer,
    DeviceCreateOrUpdateSerializer,
)
from device.serializers.stream import StreamListSerializer


class DeviceViewSet(BaseModelViewSet):
    lookup_field = "id"
    serializer_class = DeviceListSerializer
    filterset_fields = [
        "category",
    ]
    ordering_fields = ["sequence", "created_time"]
    ordering = ["sequence", "-created_time"]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return DeviceListSerializer
        else:
            return DeviceCreateOrUpdateSerializer

    def get_queryset(self):
        perms = self.request.query_params.getlist("perms", ["view_device"])
        is_owner = self.request.query_params.get("owner", False)
        q_set = get_objects_for_user(self.request.user, perms=perms, klass=Device)
        if is_owner:
            q_set = q_set.filter(create_user=self.request.user)
        return q_set

    def perform_create(self, serializer):
        current_user = self.request.user
        device = serializer.save(create_user=current_user)
        assign_perm("control", current_user, device)
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
        return super(DeviceViewSet, self).perform_destroy(instance)

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
        serializer = StreamListSerializer(device.streams, many=True)
        return Response(serializer.data)

    @action(methods=["get"], detail=True)
    def charts(self, request, *args, **kwargs):
        device = self.get_object()
        charts = Chart.objects.filter(stream__device=device, stream__show_chart=True).all()
        serializer = ChartDetailSerializer(charts, many=True)
        return Response(serializer.data)

    @action(methods=["get"], detail=True)
    def perms(self, request, *args, **kwargs):
        device = self.get_object()
        perms = get_user_perms(request.user, device)
        return Response(perms.all())
