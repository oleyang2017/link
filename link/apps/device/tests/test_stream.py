from django.test import TestCase
from rest_framework import status
from django.db.utils import IntegrityError
from guardian.shortcuts import assign_perm
from rest_framework.test import APITestCase

from device.models.device import Device
from device.models.stream import Stream
from user.models.user_profile import UserProfile


class StreamModelTestCase(TestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(username="test_stream_user")
        self.device = Device.objects.create(name="d", create_user=self.user)

    def test_create_stream(self):
        Stream.objects.create(device=self.device, create_user=self.user, name="s")
        try:
            Stream.objects.create(device=self.device, create_user=self.user, name="s")
        except IntegrityError:
            pass


class StreamAPITestCase(APITestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(username="test_stream_api_user")
        self.user2 = UserProfile.objects.create(username="test_stream_api_user_2")
        self.client.force_authenticate(user=self.user)

    def test_stream_list(self):
        response = self.client.post("/api/devices/", {"name": 1}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        device_id = response.data.get("id")
        device = Device.objects.filter(id=device_id).first()
        Stream.objects.create(device=device, create_user=self.user, name="s")
        Stream.objects.create(device=device, create_user=self.user, name="s1")
        Stream.objects.create(device=device, create_user=self.user2, name="s3")
        response = self.client.get("/api/streams/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        response = self.client.get(f"/api/devices/{device.id}/streams/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_stream_create(self):
        response = self.client.post("/api/devices/", {"name": 1}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        device_id = response.data.get("id")
        response = self.client.post("/api/streams/", {"name": "1", "device": device_id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post("/api/streams/", {"name": "1", "device": device_id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["non_field_errors"][0], "同一设备数据流名称不能重复！")

        response = self.client.post("/api/streams/", {"name": "2"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["device"][0], "该字段是必填项。")

        self.client.force_authenticate(user=self.user2)
        response = self.client.post("/api/streams/", {"name": "12", "device": device_id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        device = Device.objects.filter(id=device_id).first()
        assign_perm("change_device", self.user2, device)
        response = self.client.post("/api/streams/", {"name": "12", "device": device_id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_stream_update(self):
        response = self.client.post("/api/devices/", {"name": 1}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        device = Device.objects.filter(id=response.data.get("id")).first()
        stream1 = Stream.objects.create(name="s1", device=device, create_user=self.user)
        stream2 = Stream.objects.create(name="s2", device=device, create_user=self.user2)

        response = self.client.put(f"/api/streams/{stream1.id}/", {"name": "s2"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["non_field_errors"][0], "同一设备数据流名称不能重复！")

        response = self.client.put(f"/api/streams/{stream1.id}/", {"name": "s3"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.put(f"/api/streams/{stream1.id}/", {"device": 1})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.put(f"/api/streams/{stream1.id}/", {"data_type": "char"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.client.force_authenticate(user=self.user2)
        response = self.client.put(f"/api/streams/{stream2.id}/", {"name": "cs"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        assign_perm("view_device", self.user2, device)
        assign_perm("change_device", self.user2, device)
        response = self.client.put(f"/api/streams/{stream2.id}/", {"name": "cs"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
