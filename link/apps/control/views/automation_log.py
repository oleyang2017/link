from base.base_viewsets import BaseModelViewSet
from control.models.automation_log import AutomationLog
from control.serializers.automation_log import AutomationLogSerializer


class AutomationLogViewSet(BaseModelViewSet):
    lookup_field = "id"
    serializer_class = AutomationLogSerializer
    queryset = AutomationLog.objects
