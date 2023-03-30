from django.db import models
from timescale.db.models.models import TimescaleModel


class EMQXData(TimescaleModel):
    """
    历史消息
    """

    node = models.CharField(max_length=32, verbose_name="节点")
    client_id = models.CharField(max_length=64, verbose_name="device client_id", db_index=True)
    stream_id = models.IntegerField(verbose_name="stream id", db_index=True)
    value = models.FloatField(verbose_name="数据", null=False, blank=False)

    class Meta:
        db_table = "emqx_data"
        verbose_name = "MQTT消息"
        verbose_name_plural = verbose_name
        index_together = ["stream_id", "time"]
