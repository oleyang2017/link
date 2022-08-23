from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from device.models.category import DeviceCategory
from user.models.user_profile import UserProfile


class DeviceCategoryModelTestCase(TestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(username="test_category_user")

    def test_create_device_category(self):
        categroy = DeviceCategory.objects.create(name="c", create_user=self.user)
        categroy = DeviceCategory.objects.create(name="c", create_user=self.user)


class DeviceCategoryAPITestCase(APITestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(username="test_category_api_user")
        self.user2 = UserProfile.objects.create(username="test_category_api_user_2")
        self.client.force_authenticate(user=self.user)

    def test_category_list(self):
        DeviceCategory.objects.create(name="c", create_user=self.user)
        DeviceCategory.objects.create(name="c1", create_user=self.user)
        DeviceCategory.objects.create(name="c2", create_user=self.user2)
        response = self.client.get("/api/categories/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_category_create(self):
        response = self.client.post("/api/categories/", {"name": "1"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_category_update(self):
        category = DeviceCategory.objects.create(name="c", create_user=self.user)
        response = self.client.put(f"/api/categories/{category.id}/", {"name": 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_delete(self):
        category = DeviceCategory.objects.create(name="c", create_user=self.user)
        response = self.client.delete(f"/api/categories/{category.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_category_sort(self):
        categories = DeviceCategory.objects.filter(create_user=self.user).all()
        data = {}
        for index, category in enumerate(categories):
            data[category.id] = index
        response = self.client.put("/api/categories/sort/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        categories = DeviceCategory.objects.filter(create_user=self.user).all()
        for category in categories:
            self.assertEqual(category.sequence, data[category.id])
