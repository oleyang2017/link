from django.shortcuts import get_object_or_404
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend

from base.base_viewsets import BaseModelViewSet
from common.models.invite_link import InviteLink
from common.serializers.invite_link import InviteLinkSerializer, InviteLinkDetailSerializer
from common.serializers.invite_record import InviteRecordSerializer


class InviteLinkViewSet(BaseModelViewSet):
    serializer_class = InviteLinkSerializer
    lookup_field = "id"
    filter_fields = ["code", "invite_type"]
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    queryset = InviteLink.objects

    def get_serializer_class(self):
        if self.request.method == "GET":
            return InviteLinkSerializer
        else:
            return InviteLinkDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = get_object_or_404(InviteLink, **kwargs)
        serializer = InviteLinkDetailSerializer(instance, context={"request": request})
        return Response(serializer.data)

    @action(methods=["get"], detail=True)
    def record_list(self, request, *args, **kwargs):
        link = self.get_object()
        serializer = InviteRecordSerializer(link.invite_records, many=True)
        return Response(serializer.data)

    @action(methods=["post"], detail=True)
    def action(self, request, *args, **kwargs):
        if self.request.data.get("action") not in ["accept", "reject"]:
            raise ValidationError("action必须是同意或者拒绝")
        pass
