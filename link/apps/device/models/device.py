from django.db import models
from shortuuid.django_fields import ShortUUIDField

from base.base_model import BaseModel


class Device(BaseModel):
    """设备"""

    client_id = ShortUUIDField(length=12, verbose_name="客户端ID", unique=True)
    client_name = ShortUUIDField(length=12, verbose_name="客户端名称", unique=True)
    category = models.ForeignKey(
        "device.DeviceCategory",
        null=True,
        blank=True,
        related_name="devices",
        verbose_name="所属分类",
        on_delete=models.SET_NULL,
        db_constraint=False,
    )
    name = models.CharField(max_length=8, verbose_name="设备名称")
    desc = models.TextField(blank=True, null=True, verbose_name="说明")
    status = models.BooleanField(default=False, verbose_name="设备状态")
    image = models.ImageField(null=True, blank=True, verbose_name="图片", upload_to="images/device")
    is_super = models.BooleanField(default=False, verbose_name="权限设备")
    sequence = models.IntegerField(default=0, verbose_name="序列")
    last_connect_time = models.DateTimeField(
        verbose_name="最近连接时间", null=True, blank=True
    )
    token = ShortUUIDField(length=16, verbose_name="token")

    class Meta:
        db_table = "device"
        verbose_name = "设备"
        verbose_name_plural = verbose_name
        permissions = (
            ("control_device", "Can control device"),
        )

    def __str__(self):
        return self.name
