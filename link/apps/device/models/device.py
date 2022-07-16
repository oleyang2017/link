import re

from django.db import models
from shortuuid.django_fields import ShortUUIDField

from base.base_model import BaseModel
from emqx.models.data import EMQXData
from device.models.category import DeviceCategory


class Device(BaseModel):
    """设备"""

    client_id = ShortUUIDField(length=12, verbose_name="客户端ID", unique=True)
    client_name = ShortUUIDField(length=12, verbose_name="客户端名称", unique=True)
    category = models.ForeignKey(
        DeviceCategory,
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
    last_connect_time = models.DateTimeField(verbose_name="最近连接时间", null=True, blank=True)
    custom_info = models.CharField(verbose_name="自定义展示信息", null=True, blank=True, max_length=64)
    # e.g 当前温度[stream_name]，当前湿度[stream_name]
    token = ShortUUIDField(length=16, verbose_name="token")

    class Meta:
        db_table = "device"
        verbose_name = "设备"
        verbose_name_plural = verbose_name
        permissions = (("control_device", "Can control device"),)

    def __str__(self):
        return self.name

    def get_display_custom_info(self):
        if self.custom_info:
            display_custom_info = self.custom_info
            stream_list = re.findall(r"[\[](.*?)[\]]", display_custom_info)
            for name in stream_list:
                stream = self.streams.filter(name=name).first()
                data = "--"
                if stream:
                    last_data = (
                        EMQXData.objects.filter(
                            client_id=self.client_id,
                            topic__endswith=stream.stream_id,
                        )
                        .order_by("-timestamp")
                        .first()
                    )
                    if last_data:
                        data = f"{last_data.payload} {stream.unit}"
                display_custom_info = display_custom_info.replace(f"[{name}]", data)
            return display_custom_info
        else:
            return None
