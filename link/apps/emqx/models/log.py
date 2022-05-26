from django.db import models


class EMQXLog(models.Model):
    """EMQX设备连接日志"""

    node = models.CharField(max_length=32, verbose_name="节点")
    ip = models.GenericIPAddressField(verbose_name="IP")
    port = models.CharField(max_length=8, verbose_name="端口")
    client_id = models.CharField(max_length=32, verbose_name="client_id")
    proto = models.CharField(max_length=32, verbose_name="协议")
    connected = models.BooleanField(verbose_name="连接/断开")

    class Meta:
        db_table = "emqx_log"
        verbose_name = "EMQX设备连接日志"
