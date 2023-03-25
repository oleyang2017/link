from django.test import TestCase
from rest_framework import status
from django.db.utils import IntegrityError
from guardian.shortcuts import assign_perm
from rest_framework.test import APITestCase

from device.models.chart import Chart
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

        # 普通创建
        response = self.client.post(
            "/api/streams/",
            {
                "name": "1",
                "device": device_id,
                "data_type": "number",
                "unit": "test",
                "unit_name": "test",
                "show": True,
                "icon": "test",
                "color": "test",
                "save_data": True,
                "show_chart": True,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("name"), "1")
        self.assertEqual(response.data.get("device"), device_id)
        self.assertEqual(response.data.get("data_type"), "number")
        self.assertEqual(response.data.get("unit"), "test")
        self.assertEqual(response.data.get("unit_name"), "test")
        self.assertEqual(response.data.get("icon"), "test")
        self.assertEqual(response.data.get("color"), "test")
        self.assertTrue(response.data.get("show"))
        self.assertTrue(response.data.get("save_data"))
        self.assertTrue(response.data.get("show_chart"))

        # 数据流名称重复创建
        response = self.client.post("/api/streams/", {"name": "1", "device": device_id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["non_field_errors"][0], "同一设备数据流名称不能重复！")

        # 设备为空创建
        response = self.client.post("/api/streams/", {"name": "2"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["device"][0], "该字段是必填项。")

        # 没有修改设备权限创建
        self.client.force_authenticate(user=self.user2)
        response = self.client.post("/api/streams/", {"name": "12", "device": device_id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # 有修改设备权限创建
        device = Device.objects.filter(id=device_id).first()
        assign_perm("change_device", self.user2, device)
        response = self.client.post("/api/streams/", {"name": "12", "device": device_id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 错误的数据类型创建
        response = self.client.post(
            "/api/streams/",
            {
                "name": "1",
                "device": device_id,
                "data_type": "test",
                "show": "test",
                "save_data": "test",
                "show_chart": "test",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["data_type"][0], "“test” 不是合法选项。")
        self.assertEqual(response.data["show"][0], "Must be a valid boolean.")
        self.assertEqual(response.data["save_data"][0], "Must be a valid boolean.")
        self.assertEqual(response.data["show_chart"][0], "Must be a valid boolean.")

    def test_stream_create_with_chart(self):
        # 嵌套创建图表
        response = self.client.post("/api/devices/", {"name": 1}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        device_id = response.data.get("id")

        response = self.client.post(
            "/api/streams/",
            {
                "name": "2",
                "device": device_id,
                "show_chart": True,
                "chart": {"title": "test", "name": "test", "option": "test"},
            },
            format = "json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        stream_id = response.data.get("id")
        chart = Chart.objects.filter(stream=stream_id).first()
        self.assertIsNotNone(chart)
        self.assertEqual(chart.title, "test")
        self.assertEqual(chart.name, "test")
        self.assertEqual(chart.option, "test")

    def test_stream_update(self):
        response = self.client.post("/api/devices/", {"name": 1}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        device = Device.objects.filter(id=response.data.get("id")).first()
        stream1 = Stream.objects.create(name="s1", device=device, create_user=self.user)
        stream2 = Stream.objects.create(name="s2", device=device, create_user=self.user2)

        # 正常修改
        response = self.client.put(f"/api/streams/{stream1.id}/", {
            "name": "test",
            "unit": "test",
            "unit_name": "test",
            "show": True,
            "icon": "test",
            "color": "test",
            "save_data": True,
            "show_chart": True,
        }, )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("name"), "test")
        self.assertEqual(response.data.get("unit"), "test")
        self.assertEqual(response.data.get("unit_name"), "test")
        self.assertEqual(response.data.get("icon"), "test")
        self.assertEqual(response.data.get("color"), "test")
        self.assertTrue(response.data.get("show"))
        self.assertTrue(response.data.get("save_data"))
        self.assertTrue(response.data.get("show_chart"))

        # 错误类型
        response = self.client.put(f"/api/streams/{stream1.id}/", {
            "show": "test",
            "save_data": "test",
            "show_chart": "test",
        }, )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["show"][0], "Must be a valid boolean.")
        self.assertEqual(response.data["save_data"][0], "Must be a valid boolean.")
        self.assertEqual(response.data["show_chart"][0], "Must be a valid boolean.")

        # 重名修改
        response = self.client.put(f"/api/streams/{stream1.id}/", {"name": "s2"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["non_field_errors"][0], "同一设备数据流名称不能重复！")

        # 修改设备、数据类型、图表
        other_device =  Device.objects.first()
        response = self.client.put(
            f"/api/streams/{stream1.id}/", {"device": other_device.id, "chart": {"title": "test"}}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("device"), device.id)
        self.assertEqual(response.data.get("chart").get("title"), "test")

        # 没有修改设备权限修改
        self.client.force_authenticate(user=self.user2)
        response = self.client.put(f"/api/streams/{stream2.id}/", {"name": "cs"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # 有修改设备权限修改
        assign_perm("view_device", self.user2, device)
        assign_perm("change_device", self.user2, device)
        response = self.client.put(f"/api/streams/{stream2.id}/", {"name": "cs"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("name"), "cs")

    def test_stream_update_with_chart(self):
        response = self.client.post("/api/devices/", {"name": 1}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        device_id = response.data.get("id")
        response = self.client.post(
            "/api/streams/",
            {
                "name": "2",
                "device": device_id,
                "show_chart": True,
                "chart": {"title": "test", "name": "test", "option": "test"},
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        stream_id = response.data.get("id")

        response = self.client.put(
            f"/api/streams/{stream_id}/",
            {
                "name": "3",
                "device": device_id,
                "show_chart": True,
                "chart": {"title": "test1", "name": "test1", "option": "test1"},
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        chart = Chart.objects.filter(stream=stream_id).first()
        self.assertIsNotNone(chart)
        self.assertEqual(chart.title, "test1")
        self.assertEqual(chart.name, "test1")
        self.assertEqual(chart.option, "test1")
