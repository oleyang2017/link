from django.test import TestCase
from rest_framework import status
from guardian.shortcuts import assign_perm
from rest_framework.test import APITestCase

from device.models.device import Device
from device.models.stream import Stream
from device.models.category import DeviceCategory
from user.models.user_profile import UserProfile


class DeviceModelTestCase(TestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(username="test_device_user")

    def test_create_device(self):
        categroy = DeviceCategory.objects.create(name="c", create_user=self.user)
        Device.objects.create(name="1", create_user=self.user)
        Device.objects.create(name="1", create_user=self.user, category=categroy)


class DeviceAPITestCase(APITestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(username="test_device_api_user")
        self.user2 = UserProfile.objects.create(username="test_device_api_user_2")
        self.client.force_authenticate(user=self.user)
        for i in range(5):
            device = Device.objects.create(name=f"{i}", create_user=self.user)
            assign_perm("view_device", self.user, device)
        self.share_device = Device.objects.create(name="user2", create_user=self.user2)
        assign_perm("view_device", self.user2, self.share_device)

    def test_device_list(self):
        response = self.client.get("/api/devices/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for i in response.data:
            self.assertEqual(i.get("create_user"), self.user.id)
        self.assertEqual(len(response.data), 5)

        # 分享设备
        assign_perm("view_device", self.user, self.share_device)
        response = self.client.get("/api/devices/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 6)

        # 按设备分类筛选
        categroy = DeviceCategory.objects.create(name="2", create_user=self.user)
        device = Device.objects.create(name="c", category=categroy, create_user=self.user)
        assign_perm("view_device", self.user, device)
        response = self.client.get("/api/devices/", {"category": categroy.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        for i in response.data:
            self.assertEqual(i.get("category"), categroy.id)

    def test_create_device(self):
        response = self.client.post("/api/devices/", {"name": 1})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post("/api/devices/", {"name": 1, "category": 1000})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0], "设备分类不存在！")

        categroy = DeviceCategory.objects.create(name="2", create_user=self.user)
        response = self.client.post("/api/devices/", {"name": 1, "category": categroy.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 嵌套创建数据流
        body = {"name": 1, "category": categroy.id, "streams": [{"name": "s"}, {"name": "2"}]}
        response = self.client.post("/api/devices/", body, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        body["streams"] = [{"name": "s"}, {"name": "s"}]
        response = self.client.post("/api/devices/", body, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0], "同一设备数据流名称不能重复！")

    def test_device_detail(self):
        body = {"name": 1, "streams": [{"name": "s"}, {"name": "2"}]}
        response = self.client.post("/api/devices/", body, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        device_id = response.data.get("id")

        response = self.client.get(f"/api/devices/{device_id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(f"/api/devices/{device_id}/streams/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        self.client.force_authenticate(user=self.user2)
        response = self.client.get(f"/api/devices/{device_id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_device_perms(self):
        response = self.client.post("/api/devices/", {"name": 1}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        device_id = response.data.get("id")
        response = self.client.get(f"/api/devices/{device_id}/perms/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(user=self.user2)
        response = self.client.get(f"/api/devices/{device_id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        device = Device.objects.filter(id=device_id).first()
        assign_perm("view_device", self.user2, device)
        response = self.client.get(f"/api/devices/{device_id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_device_update(self):
        response = self.client.post("/api/devices/", {"name": 1}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        device_id = response.data.get("id")
        response = self.client.put(f"/api/devices/{device_id}/", {"name": 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        device = Device.objects.filter(id=device_id).first()

        self.client.force_authenticate(user=self.user2)
        assign_perm("view_device", self.user2, device)
        response = self.client.put(f"/api/devices/{device_id}/", {"name": 3})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        assign_perm("change_device", self.user2, device)
        response = self.client.put(f"/api/devices/{device_id}/", {"name": 3})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_device_streams(self):
        response = self.client.post("/api/devices/", {"name": 1}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        device_id = response.data.get("id")
        device = Device.objects.filter(id=device_id).first()
        Stream.objects.create(create_user=self.user, device=device, name="1")
        Stream.objects.create(create_user=self.user, device=device, name="2")
        response = self.client.get(f"/api/devices/{device_id}/streams/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_device_delete(self):
        response = self.client.post("/api/devices/", {"name": 1}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        device_id = response.data.get("id")
        response = self.client.delete(f"/api/devices/{device_id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.post("/api/devices/", {"name": 1}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        device_id = response.data.get("id")
        device = Device.objects.filter(id=device_id).first()
        assign_perm("view_device", self.user2, device)
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(f"/api/devices/{device_id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
