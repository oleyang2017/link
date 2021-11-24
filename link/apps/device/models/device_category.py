from django.db import models
from django.conf import settings


class DeviceCategory(models.Model):
    """ 设备分类 """
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='device_categories', verbose_name='创建人', on_delete=models.CASCADE)
    name = models.CharField(max_length=8, verbose_name='名称')
    sequence = models.IntegerField(default=0, verbose_name='序列')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '设备分类'
        verbose_name_plural = verbose_name
        ordering = ('sequence',)

    def __str__(self):
        return self.name
