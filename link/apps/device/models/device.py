from django.db import models
from django.conf import settings
from base.base_model import BaseModel
from shortuuid.django_fields import ShortUUIDField


class Device(BaseModel):
    """ 设备 """
    client_id = ShortUUIDField(max_length=12, verbose_name="client_id")
    device_id = ShortUUIDField(max_length=12, verbose_name="device_id")
    category = models.ForeignKey("device.DeviceCategory", null=True, blank=True, related_name='devices', verbose_name='所属分类', on_delete=models.SET_NULL)
    name = models.CharField(max_length=8, verbose_name='设备名称')
    desc = models.TextField(blank=True, default='', verbose_name='说明')
    status = models.BooleanField(default=False, verbose_name='设备状态')
    image = models.URLField(null=True, blank=True, verbose_name='图片')
    is_super = models.BooleanField(default=False)
    sequence = models.IntegerField(default=0, verbose_name='序列')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    last_connect_time = models.DateTimeField(verbose_name='最新连接时间', null=True, blank=True)
    token = ShortUUIDField(max_length=16, verbose_name="token")

    class Meta:
        verbose_name = '设备'
        verbose_name_plural = verbose_name
        ordering = ('sequence',)

    def __str__(self):
        return self.name
