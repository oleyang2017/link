from django.db import models


class DataSet(models.Model):

    stream_id = models.CharField(max_length=64, verbose_name='数据流')  # 这里不和stream模型做建立关联,目的是便于日后使用时序数据库
    client_id = models.CharField(max_length=32, verbose_name='设备')  # 非device_id
    topic = models.CharField(max_length=100, verbose_name='Topic')
    time = models.DateTimeField(auto_now_add=True, verbose_name='数据上传时间')

    float_data = models.FloatField(null=True, blank=True)
    int_data = models.IntegerField(null=True, blank=True)
    bool_data = models.BooleanField(null=True, blank=True)
    char_data = models.CharField(max_length=64, null=True, blank=True)
