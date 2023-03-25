from rest_framework import status
from guardian.shortcuts import assign_perm
from rest_framework.test import APITestCase

from device.models.device import Device
from user.models.user_profile import UserProfile


class AclAPITestCase(APITestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(username="test_acl_api_user")
        self.user2 = UserProfile.objects.create(username="test_acl_api_user_2")
        self.device = Device.objects.create(name="device", create_user=self.user)

    def test_sub_cmd(self):
        payload = {
            "access": "1",
            "username": self.user.emqx_user.username,
            "topic": f"$cmd/test",
        }
        response = self.client.post("/api/emqx/acl/", payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_sub_sub(self):
        # 未授权
        payload = {
            "access": "1",
            "username": self.user2.emqx_user.username,
            "topic": f"$sub/{self.device.client_id}",
        }
        response = self.client.post("/api/emqx/acl/", payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # 授权
        assign_perm("sub", self.user2, self.device)
        payload = {
            "access": "1",
            "username": self.user2.emqx_user.username,
            "topic": f"$sub/{self.device.client_id}",
        }
        response = self.client.post("/api/emqx/acl/", payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_pub_save(self):
        payload = {
            "access": "2",
            "username": self.user.emqx_user.username,
            "topic": f"$save",
        }
        response = self.client.post("/api/emqx/acl/", payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_pub_resp(self):
        payload = {
            "access": "2",
            "username": self.user.emqx_user.username,
            "topic": f"$resp",
        }
        response = self.client.post("/api/emqx/acl/", payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_bad_request(self):
        payload = {
            "access": "3",
            "username": self.user.emqx_user.username,
            "topic": f"$resp",
        }
        response = self.client.post("/api/emqx/acl/", payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        payload = {
            "access": "1",
            "username": self.user.emqx_user.username,
            "topic": "test",
        }
        response = self.client.post("/api/emqx/acl/", payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        payload = {
            "access": "2",
            "username": self.user.emqx_user.username,
            "topic": "test",
        }
        response = self.client.post("/api/emqx/acl/", payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        payload = {
            "access": "1",
            "username": "test",
            "topic": "$sub",
        }
        response = self.client.post("/api/emqx/acl/", payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
