from guardian.shortcuts import assign_perm, get_objects_for_user
from rest_framework.response import Response

from base.base_viewsets import BaseModelViewSet
from control.models.automation import Automation
from control.serializers.automation import AutomationListSerializer, AutomationDetailSerializer


class AutomationViewSet(BaseModelViewSet):
    lookup_field = "id"
    serializer_class = AutomationListSerializer
    filterset_fields = ["name", "enable"]
    ordering_fields = ["created_time"]
    ordering = ["-created_time"]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return AutomationListSerializer
        else:
            return AutomationDetailSerializer

    def get_queryset(self):
        q_set = get_objects_for_user(self.request.user, perms=["view_automation"], klass=Automation)
        return q_set

    def perform_create(self, serializer):
        current_user = self.request.user
        automation = serializer.save(create_user=current_user)
        assign_perm("view_automation", current_user, automation)
        assign_perm("change_automation", current_user, automation)
        assign_perm("delete_automation", current_user, automation)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = AutomationDetailSerializer(instance, context={"request": request})
        return Response(serializer.data)
