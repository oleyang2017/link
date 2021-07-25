from django.db import models


class DataPoint(models.Model):
    """
    历史消息
    """
    node = models.CharField(max_length=32, verbose_name="节点")
    msg_id = models.CharField(max_length=64, verbose_name="消息ID")
    client_id = models.CharField(max_length=16, verbose_name='client_id', db_index=True)
    topic = models.CharField(max_length=32, verbose_name='数据流', db_index=True)
    payload = models.CharField(max_length=256, verbose_name="消息内容")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='上传时间')
