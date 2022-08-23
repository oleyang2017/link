from guardian.shortcuts import assign_perm, get_user_perms, get_objects_for_user
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied

from base.base_viewsets import BaseModelViewSet
from device.models.device import Device
from device.serializers.chart import ChartSerializer
from device.serializers.device import DeviceSerializer, DeviceDetailSerializer
from device.serializers.stream import StreamSerializer
from device.serializers.trigger import TriggerSerializer


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
        q_set = get_objects_for_user(self.request.user, perms="view_device", klass=Device)
        if self.request.query_params.get("only_creator", False):
            q_set = q_set.filter(create_user=self.request.user)
        return q_set

    def perform_create(self, serializer):
        current_user = self.request.user
        device = serializer.save(create_user=current_user)
        assign_perm("control_device", current_user, device)
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
