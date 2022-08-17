import random
from datetime import datetime

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.exceptions import ValidationError

from device.models.device import Device
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
                "accept",
                UserProfile.objects.create(username=f"test_user_{random.randint(0, 999999)}"),
            )
        except ValidationError as e:
            self.assertEqual(e.args[0], "邀请人数已达上限")


class InviteLinkAPITestCase(APITestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(username="test_list_view1")
        self.user2 = UserProfile.objects.create(username="test_list_view2")
        self.client.force_authenticate(user=self.user)

    def test_list_view(self):
        for i in range(2):
            InviteLink.objects.create(
                create_user=self.user,
                object_id=1,
                invite_type="device",
            )
        InviteLink.objects.create(
            create_user=self.user2,
            object_id=1,
            invite_type="device",
        )
        response = self.client.get("/api/invite_links/")
        for item in response.data:
            self.assertEqual(item.get("create_user"), self.user.id)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_invite_link(self):
        device = Device.objects.create(name="device", create_user=self.user)
        device2 = Device.objects.create(name="device2", create_user=self.user2)
        response = self.client.post(
            "/api/invite_links/", {"object_id": device.id, "invite_type": "device"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(
            "/api/invite_links/", {"object_id": device2.id, "invite_type": "device"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0], "设备不存在")

    def test_update_invite_link(self):
        unable_link = InviteLink.objects.create(
            create_user=self.user, object_id=1, invite_type="device", enable=0
        )
        response = self.client.put(f"/api/invite_links/{unable_link.id}/", {"count": 1})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0], "已关闭的邀请链接不可以修改")

        enable_link = InviteLink.objects.create(
            create_user=self.user,
            object_id=1,
            invite_type="device",
        )
        response = self.client.put(f"/api/invite_links/{enable_link.id}/", {"count": 1})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0], "邀请链接不可修改非enable之外的信息")

        response = self.client.put(f"/api/invite_links/{enable_link.id}/", {"enable": False})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("enable"), False)

    def test_delete_invite_link(self):
        invite_link = InviteLink.objects.create(
            create_user=self.user,
            object_id=1,
            invite_type="device",
        )
        response = self.client.delete(f"/api/invite_links/{invite_link.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_detail_invite_link(self):
        invite_link = InviteLink.objects.create(
            create_user=self.user,
            object_id=1,
            invite_type="device",
        )
        InviteRecord.objects.create(
            code=invite_link.code,
            invite_link=invite_link,
            object_id=invite_link.object_id,
            permissions=invite_link.permissions,
            operation="reject",
            create_user=self.user,
        )
        InviteRecord.objects.create(
            code=invite_link.code,
            invite_link=invite_link,
            object_id=invite_link.object_id,
            permissions=invite_link.permissions,
            operation="accept",
            create_user=self.user2,
        )
        response = self.client.get(f"/api/invite_links/{invite_link.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("records", [])), 2)
