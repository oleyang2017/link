from base.base_serializers import BaseModelSerializer
from control.models.automation_log import AutomationLog


class AutomationLogSerializer(BaseModelSerializer):
    class Meta:
        model = AutomationLog
        fields = "__all__"
