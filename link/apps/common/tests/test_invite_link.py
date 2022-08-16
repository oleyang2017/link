import random
from datetime import datetime

from django.test import TestCase
from rest_framework.exceptions import ValidationError

from user.models.user_profile import UserProfile
from common.models.invite_link import InviteLink
from common.models.invite_record import InviteRecord


class InviteLinkModelTestCase(TestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(username="test_user")

    def test_invite_link_can_join(self):
        unable_link = InviteLink.objects.create(
            create_user=self.user,
            enable=False,
            object_id=1,
            invite_type="device",
        )
        try:
            unable_link.check_can_join("accept", self.user)
        except ValidationError as e:
            self.assertEqual(e.args[0], "邀请链接已不可使用")

        normal_link = InviteLink.objects.create(
            create_user=self.user,
            object_id=1,
            invite_type="device",
        )
        try:
            normal_link.check_can_join("accept", self.user)
        except ValidationError as e:
            self.assertEqual(e.args[0], "无法执行操作")

        expired_link = InviteLink.objects.create(
            create_user=self.user,
            object_id=1,
            invite_type="device",
            end_time=datetime(2000, 1, 1, 0, 0, 0),
        )
        try:
            expired_link.check_can_join("accept", self.user)
        except ValidationError as e:
            self.assertEqual(e.args[0], "邀请链接已过期")

        count_link = InviteLink.objects.create(
            create_user=self.user,
            object_id=1,
            invite_type="device",
            count=1,
        )
        for i in range(2):
            InviteRecord.objects.create(
                code=count_link.code,
                invite_link=count_link,
                object_id=count_link.object_id,
                permissions=count_link.permissions,
                operation="reject",
                create_user=UserProfile.objects.create(username=f"test_user_r{i}"),
            )
        count_link.check_can_join(
            "accept", UserProfile.objects.create(username=f"test_user_{random.randint(0, 999999)}")
        )
        InviteRecord.objects.create(
            code=count_link.code,
            invite_link=count_link,
            object_id=count_link.object_id,
            permissions=count_link.permissions,
            operation="accept",
            create_user=UserProfile.objects.create(username=f"test_user_a1"),
        )
        try:
            count_link.check_can_join(
                "accept", UserProfile.objects.create(username=f"test_user_{random.randint(0, 999999)}")
            )
        except ValidationError as e:
            self.assertEqual(e.args[0], "邀请人数已达上限")

