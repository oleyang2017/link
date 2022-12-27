from django.shortcuts import get_object_or_404
from rest_framework.status import HTTP_201_CREATED
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django_filters.rest_framework import DjangoFilterBackend

from invite.models.invite_record import InviteRecord
from invite.serializers.invite_record import InviteRecordSerializer


class InviteRecordViewSet(ViewSet):
    serializer_class = InviteRecordSerializer
    lookup_field = "_id"
    filter_fields = ["code", "invite_link"]
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    queryset = InviteRecord.objects

    def retrieve(self, request, _id):
        # 只有查看当前用户创建的邀请链接记录详情
        queryset = InviteRecord.objects.filter(invite_link__create_user_id=self.request.user.id)
        obj = get_object_or_404(queryset, id=_id)
        serializer = InviteRecordSerializer(obj)
        return Response(serializer.data)
