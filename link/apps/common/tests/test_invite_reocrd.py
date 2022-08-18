from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from user.models.user_profile import UserProfile
from common.models.invite_link import InviteLink
from common.models.invite_record import InviteRecord


class InviteRecordModelTestCase(TestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(username="test_user")

    def test_create(self):
        inivte_link = InviteLink.objects.create(
            create_user=self.user,
            enable=False,
            object_id=1,
            invite_type="device",
        )
        InviteRecord.objects.create(
            code=inivte_link.code,
            invite_link=inivte_link,
            object_id=inivte_link.object_id,
            permissions=inivte_link.permissions,
            operation="accept",
            create_user=self.user,
        )


class InviteRecordAPITestCase(APITestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(username="test_list_view1")
        self.user2 = UserProfile.objects.create(username="test_list_view2")
        self.client.force_authenticate(user=self.user)

    def test_detail_invite_record(self):
        invite_link = InviteLink.objects.create(
            create_user=self.user,
            object_id=1,
            invite_type="device",
        )
        record = InviteRecord.objects.create(
            code=invite_link.code,
            invite_link=invite_link,
            object_id=invite_link.object_id,
            permissions=invite_link.permissions,
            operation="reject",
            create_user=self.user,
        )

        response = self.client.get(f"/api/invite_records/{record.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        invite_link = InviteLink.objects.create(
            create_user=self.user2,
            object_id=1,
            invite_type="device",
        )
        record = InviteRecord.objects.create(
            code=invite_link.code,
            invite_link=invite_link,
            object_id=invite_link.object_id,
            permissions=invite_link.permissions,
            operation="accept",
            create_user=self.user2,
        )
        response = self.client.get(f"/api/invite_records/{record.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
