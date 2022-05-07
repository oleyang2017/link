from django.db import models
from shortuuid.django_fields import ShortUUIDField

from base.base_model import BaseModel


class Stream(BaseModel):
    """
    数据流
    """
    QOS_CHOICE = (
        (0, '0'),
        (1, '1'),
        (2, '2'),
    )
    DATA_TYPE_CHOICE = (
        ('int', '整型'),
        ('float', '浮点型'),
        ('bool', '布尔型'),
        ('char', '字符型'),
    )
    stream_id = ShortUUIDField(db_index=True, unique=True, verbose_name='数据流ID')
    name = models.CharField(max_length=16, verbose_name='名称')
    device_id = models.ForeignKey('device.Device', related_name='streams', verbose_name='所属设备',
                                  on_delete=models.CASCADE, db_constraint=False)
    unit_name = models.CharField(max_length=8, blank=True, default='', verbose_name='单位名称')
    unit = models.CharField(max_length=8, blank=True, default='', verbose_name='单位')
    qos = models.IntegerField(choices=QOS_CHOICE, default=0, verbose_name='Qos')
    data_type = models.CharField(max_length=8, default='int', choices=DATA_TYPE_CHOICE, verbose_name='数据类型')

    class Meta:
        db_table = 'stream'
        verbose_name = '数据流'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
