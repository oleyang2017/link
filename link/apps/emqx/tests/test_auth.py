from rest_framework import status
from rest_framework.test import APITestCase

from device.models.device import Device
from user.models.user_profile import UserProfile


class AuthAPITestCase(APITestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(username="test_auth_api_user")
        self.user2 = UserProfile.objects.create(username="test_auth_api_user_2")
        self.device = Device.objects.create(name="device", create_user=self.user)

    def test_auth(self):
        # 正常
        payload = {
            "username": self.user.emqx_user.username,
            "password": self.user.emqx_user.password,
            "client_id": self.device.client_id,
        }
        response = self.client.post("/api/emqx/auth/", payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # client_id错误
        payload = {
            "username": self.user.emqx_user.username,
            "password": self.user.emqx_user.password,
            "client_id": "test",
        }
        response = self.client.post("/api/emqx/auth/", payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # password错误
        payload = {
            "username": self.user.emqx_user.username,
            "password": "test",
            "client_id": self.device.client_id,
        }
        response = self.client.post("/api/emqx/auth/", payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # username错误
        payload = {
            "username": "test",
            "password": self.user.emqx_user.password,
            "client_id": self.device.client_id,
        }
        response = self.client.post("/api/emqx/auth/", payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # 不是这个用户的设备
        payload = {
            "username": self.user2.emqx_user.username,
            "password": self.user2.emqx_user.password,
            "client_id": self.device.client_id,
        }
        response = self.client.post("/api/emqx/auth/", payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
