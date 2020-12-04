from django.db import models
from django.conf import settings
from utils.field_extend import ShortUUIDField


class DeviceCategory(models.Model):
    """ 设备分类 """
    id = ShortUUIDField(verbose_name='设备ID', db_index=True, primary_key=True)
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='device_categories', verbose_name='创建人', on_delete=models.CASCADE)
    name = models.CharField(max_length=16, verbose_name='名称')
    sequence = models.IntegerField(default=0, verbose_name='序列')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '设备分类'
        verbose_name_plural = verbose_name
        ordering = ('sequence',)

    def __str__(self):
        return self.name


class Device(models.Model):
    """ 设备 """
    id = ShortUUIDField(verbose_name='设备ID', db_index=True, primary_key=True)
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='devices', verbose_name='创建人', on_delete=models.CASCADE)
    category = models.ForeignKey(DeviceCategory, null=True, blank=True, related_name='devices', verbose_name='所属分类', on_delete=models.SET_NULL)
    client_id = ShortUUIDField(verbose_name='客户端ID')
    name = models.CharField(max_length=8, verbose_name='设备名称')
    desc = models.TextField(blank=True, default='', verbose_name='说明')
    status = models.BooleanField(default=False, verbose_name='设备状态')
    image = models.ImageField(upload_to='device/', null=True, blank=True, verbose_name='图片')
    is_super = models.BooleanField(default=False)
    sequence = models.IntegerField(default=0, verbose_name='序列')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    last_connect_time = models.DateTimeField(verbose_name='最新连接时间', null=True, blank=True)

    class Meta:
        verbose_name = '设备'
        verbose_name_plural = verbose_name
        ordering = ('sequence',)

    def __str__(self):
        return self.name
