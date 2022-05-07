from django.db import models
from django.conf import settings
from base.base_model import BaseModel


class DeviceCategory(BaseModel):
    """ 设备分类 """
    name = models.CharField(max_length=8, verbose_name='名称')
    sequence = models.IntegerField(default=0, verbose_name='序列')

    class Meta:
        db_table = 'device_category'
        verbose_name = '设备分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
