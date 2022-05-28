from django_filters.rest_framework import DjangoFilterBackend
from guardian.shortcuts import assign_perm, get_objects_for_user
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter


class BaseModelViewSet(viewsets.ModelViewSet):
    lookup_field = "id"
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ["created_time"]
    ordering = ["-created_time"]

    def get_queryset(self):
        return get_objects_for_user(self.request.user, "device.view_device", with_superuser=False)

    def get_raw_queryset(self):
        queryset = super(BaseModelViewSet, self).get_queryset()
        return queryset

    # 由于微信小程序不支持patch方法，所以这里默认部分更新
    def get_serializer(self, *args, **kwargs):
        kwargs["partial"] = True
        return super(BaseModelViewSet, self).get_serializer(*args, **kwargs)

    def perform_create(self, serializer):
        user = self.request.user
        device = serializer.save(create_user=user)
        assign_perm("control_device", user, device)
        assign_perm("add_device", user, device)
        assign_perm("view_device", user, device)
        assign_perm("change_device", user, device)
        assign_perm("delete_device", user, device)

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
