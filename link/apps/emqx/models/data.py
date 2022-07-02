from django.db import models


class EMQXData(models.Model):
    """
    历史消息
    """

    node = models.CharField(max_length=32, verbose_name="节点")
    msg_id = models.CharField(max_length=64, verbose_name="消息ID")
    client_id = models.CharField(max_length=64, verbose_name="client_id", db_index=True)
    topic = models.CharField(max_length=128, verbose_name="数据流", db_index=True)
    payload = models.CharField(max_length=256, verbose_name="消息内容")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="上传时间")

    class Meta:
        db_table = "emqx_data"
        verbose_name = "MQTT消息"
        verbose_name_plural = verbose_name
