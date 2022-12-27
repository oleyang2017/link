from rest_framework.routers import DefaultRouter

from invite.views.invite_link import InviteLinkViewSet
from invite.views.invite_record import InviteRecordViewSet

router = DefaultRouter()

router.register("invite_links", InviteLinkViewSet, basename="invite_links")
router.register("invite_records", InviteRecordViewSet, basename="invite_records")

urlpatterns = router.urls
