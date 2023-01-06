from django.shortcuts import get_object_or_404
from guardian.shortcuts import assign_perm
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

from user.models import GroupExtend
from base.base_viewsets import BaseModelViewSet
from device.models.device import Device
from invite.models.invite_link import InviteLink
from invite.models.invite_record import InviteRecord
from invite.serializers.invite_link import InviteLinkSerializer, InviteLinkDetailSerializer
from invite.serializers.invite_record import InviteRecordSerializer


class InviteLinkViewSet(BaseModelViewSet):
    serializer_class = InviteLinkSerializer
    lookup_field = "id"
    filter_fields = ["code", "invite_type", "object_id"]
    queryset = InviteLink.objects

    def get_serializer_class(self):
        if self.request.method == "GET":
            return InviteLinkSerializer
        else:
            return InviteLinkDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        # 这里不处理权限，邀请链接是可以公开访问的
        instance = get_object_or_404(InviteLink, **kwargs)
        serializer = InviteLinkDetailSerializer(instance, context={"request": request})
        return Response(serializer.data)

    @action(methods=["get"], detail=True)
    def record_list(self, *args, **kwargs):
        link = self.get_object()
        serializer = InviteRecordSerializer(link.invite_records, many=True)
        return Response(serializer.data)

    @action(methods=["post"], detail=True)
    def share(self, *args, **kwargs):
        link = get_object_or_404(InviteLink, **kwargs)
        operation = self.request.data.get("operation")

        if operation not in ["accept", "reject"]:
            raise ValidationError("结果必须是同意或者拒绝")
        link.check_can_join(operation, self.request.user)
        if link.invite_type == "device" and operation == "accept":
            device = get_object_or_404(Device, id=link.object_id, create_user=link.create_user)
            for i in link.permissions:
                assign_perm(i, self.request.user, device)
        if link.invite_type == "group" and operation == "accept":
            group_ext = get_object_or_404(
                GroupExtend, create_user=link.create_user, group_id=link.object_id
            )
            group_ext.group.user_set.add(self.request.user)

        record = InviteRecord.objects.create(
            code=link.code,
            invite_link=link,
            object_id=link.object_id,
            permissions=link.permissions,
            operation=operation,
            create_user=self.request.user,
        )
        record.save()

        return Response()
