from rest_framework.routers import DefaultRouter

from control.views.action import ActionViewSet
from control.views.command import CommandViewSet
from control.views.automation import AutomationViewSet
from control.views.command_log import CommandLogViewSet
from control.views.automation_log import AutomationLogViewSet

router = DefaultRouter()

router.register("actions", ActionViewSet, basename="actions")
router.register("automations", AutomationViewSet, basename="automations")
router.register("automation_logs", AutomationLogViewSet, basename="automation_logs")
router.register("commands", CommandViewSet, basename="commands")
router.register("command_logs", CommandLogViewSet, basename="command_logs")

urlpatterns = router.urls
