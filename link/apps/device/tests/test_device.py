from django.test import TestCase
from rest_framework import status
from guardian.shortcuts import assign_perm, get_objects_for_user
from rest_framework.test import APITestCase

from device.models.chart import Chart
from device.models.device import Device
from device.models.stream import Stream
from device.models.category import DeviceCategory
from user.models.user_profile import UserProfile


class DeviceModelTestCase(TestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(username="test_device_user")

    def test_create_device(self):
        category = DeviceCategory.objects.create(name="c", create_user=self.user)
        Device.objects.create(name="1", create_user=self.user)
        Device.objects.create(name="1", create_user=self.user, category=category)


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
        count = Device.objects.filter(create_user=self.user).count()
        for i in response.data:
            self.assertEqual(i.get("create_user"), self.user.id)
        self.assertEqual(len(response.data), count)

        # 分享设备
        assign_perm("view_device", self.user, self.share_device)
        response = self.client.get("/api/devices/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 6)

        # 按设备分类筛选
        category = DeviceCategory.objects.create(name="2", create_user=self.user)
        device = Device.objects.create(name="c", category=category, create_user=self.user)
        assign_perm("view_device", self.user, device)
        response = self.client.get("/api/devices/", {"category": category.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        for i in response.data:
            self.assertEqual(i.get("category"), category.id)

        # 只获取自己创建的设备
        assign_perm("view_device", self.user, self.share_device)
        response = self.client.get("/api/devices/", {"owner": True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        count = Device.objects.filter(create_user=self.user).count()
        for i in response.data:
            self.assertEqual(i.get("create_user"), self.user.id)
        self.assertEqual(len(response.data), count)

        # 权限过滤
        assign_perm("change_device", self.user, self.share_device)
        assign_perm("change_device", self.user, device)
        perms = ["change_device"]
        response = self.client.get("/api/devices/", {"perms": perms})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        count = len(get_objects_for_user(self.user, perms=perms, klass=Device))
        self.assertEqual(len(response.data), count)

        perms = ["sub", "view_device"]
        response = self.client.get("/api/devices/", {"perms": perms})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        count = len(get_objects_for_user(self.user, perms=perms, klass=Device))
        self.assertEqual(len(response.data), count)

        # 权限过滤 + 只获取自己创建的设备
        perms = ["change_device"]
        response = self.client.get(
            "/api/devices/",
            {"perms": perms, "owner": True},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        count = len(
            get_objects_for_user(self.user, perms=perms, klass=Device).filter(create_user=self.user)
        )
        self.assertEqual(len(response.data), count)

    def test_create_device(self):
        # 基础创建
        response = self.client.post(
            "/api/devices/",
            {
                "name": "1",
                "desc": "test",
                "custom_info": "test",
                "sequence": 1,
                "image_url": "test",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("name"), "1")
        self.assertEqual(response.data.get("desc"), "test")
        self.assertEqual(response.data.get("custom_info"), "test")
        self.assertEqual(response.data.get("image_url"), "test")
        self.assertEqual(response.data.get("sequence"), 1)

        # 带有无效字段
        response = self.client.post(
            "/api/devices/",
            {
                "name": 1,
                "status": True,
                "is_super": True,
                "last_connect_time": "2020-01-01 00:00:00",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        device = Device.objects.filter(id=response.data.get("id")).first()
        self.assertEqual(response.data.get("name"), "1")
        self.assertEqual(device.status, False)
        self.assertEqual(device.is_super, False)
        self.assertEqual(device.last_connect_time, None)

        # 创建设备分类不存在
        response = self.client.post("/api/devices/", {"name": "1", "category": 1000})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0], "设备分类不存在！")

        # 创建时指定设备分类
        category = DeviceCategory.objects.create(name="2", create_user=self.user)
        response = self.client.post("/api/devices/", {"name": "1", "category": category.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 嵌套创建数据流
        body = {"name": 1, "category": category.id, "streams": [{"name": "s"}, {"name": "2"}]}
        response = self.client.post("/api/devices/", body, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 嵌套创建数据流+图表
        body = {
            "name": 1,
            "category": category.id,
            "streams": [{"name": "s"}, {"name": "2", "chart": {"name": "c"}}],
        }
        response = self.client.post("/api/devices/", body, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data.get("streams", [])), 2)
        self.assertEqual(response.data.get("streams")[1].get("chart").get("name"), "c")

        # 嵌套创建数据流名称重复
        body["streams"] = [{"name": "s"}, {"name": "s"}]
        response = self.client.post("/api/devices/", body, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0], "同一设备数据流名称不能重复！")

    def test_device_detail(self):
        body = {"name": 1, "streams": [{"name": "s"}, {"name": "2", "chart": {"name": "c"}}]}
        response = self.client.post("/api/devices/", body, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        device_id = response.data.get("id")
        # stream 数量
        response = self.client.get(f"/api/devices/{device_id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("streams", [])), 2)

        response = self.client.get(f"/api/devices/{device_id}/streams/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        # chart 数量
        response = self.client.get(f"/api/devices/{device_id}/charts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # stream的show_chart=False
        self.assertEqual(len(response.data), 0)

        # perms
        response = self.client.get(f"/api/devices/{device_id}/perms/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        perms = response.data
        self.assertEqual(
            set(response.data), {"view_device", "change_device", "delete_device", "control"}
        )

        # 无权限用户访问
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(f"/api/devices/{device_id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_device_perms(self):
        response = self.client.post("/api/devices/", {"name": "1"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        device_id = response.data.get("id")

        self.client.force_authenticate(user=self.user2)
        response = self.client.get(f"/api/devices/{device_id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        device = Device.objects.filter(id=device_id).first()
        assign_perm("view_device", self.user2, device)
        response = self.client.get(f"/api/devices/{device_id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_device_update(self):
        response = self.client.post("/api/devices/", {"name": "1"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        device_id = response.data.get("id")
        category = DeviceCategory.objects.create(name="c0", create_user=self.user)
        response = self.client.put(
            f"/api/devices/{device_id}/",
            {
                "name": "2",
                "desc": "test",
                "custom_info": "test",
                "sequence": 1,
                "image_url": "test",
                "status": True,
                "is_super": True,
                "category": category.id,
                "last_connect_time": "2020-01-01 00:00:00",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        device = Device.objects.filter(id=device_id).first()
        self.assertEqual(device.name, "2")
        self.assertEqual(device.desc, "test")
        self.assertEqual(device.custom_info, "test")
        self.assertEqual(device.sequence, 1)
        self.assertEqual(device.image_url, "test")
        self.assertEqual(device.category, category)

        # 无效字段
        self.assertEqual(device.status, False)
        self.assertEqual(device.is_super, False)
        self.assertEqual(device.last_connect_time, None)

        # 只有访问权限的用户无法修改
        self.client.force_authenticate(user=self.user2)
        assign_perm("view_device", self.user2, device)
        response = self.client.put(f"/api/devices/{device_id}/", {"name": "3"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # 赋予修改权限后可以修改
        assign_perm("change_device", self.user2, device)
        response = self.client.put(f"/api/devices/{device_id}/", {"name": "3"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("name"), "3")

        # 不能修改共享设备的设备分类
        category = DeviceCategory.objects.create(name="c1", create_user=self.user2)
        response = self.client.put(f"/api/devices/{device_id}/", {"category": category.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0], "不可修改设备分类！")

        # 不允许嵌套修改 streams
        response = self.client.put(
            f"/api/devices/{device_id}/",
            {"streams": [{"name": "s"}, {"name": "2", "chart": {"name": "c"}}]},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("streams", [])), 0)

    def test_device_streams(self):
        response = self.client.post("/api/devices/", {"name": "1"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        device_id = response.data.get("id")
        device = Device.objects.filter(id=device_id).first()
        Stream.objects.create(create_user=self.user, device=device, name="1")
        Stream.objects.create(create_user=self.user, device=device, name="2")
        response = self.client.get(f"/api/devices/{device_id}/streams/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_device_charts(self):
        response = self.client.post("/api/devices/", {"name": "1"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        device_id = response.data.get("id")
        device = Device.objects.filter(id=device_id).first()
        # 只有 stream.show_chart = True 才会返回
        stream = Stream.objects.create(
            create_user=self.user, device=device, name="1", show_chart=True
        )
        Chart.objects.create(create_user=self.user, stream=stream, name="1")
        response = self.client.get(f"/api/devices/{device.id}/charts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        stream.show_chart = False
        stream.save()
        response = self.client.get(f"/api/devices/{device.id}/charts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

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
        # 只有访问权限的用户无法删除
        assign_perm("view_device", self.user2, device)
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(f"/api/devices/{device_id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # 赋予修改权限后可以删除
        assign_perm("delete_device", self.user2, device)
        response = self.client.delete(f"/api/devices/{device_id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
