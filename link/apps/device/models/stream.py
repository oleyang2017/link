from django.db import models

from base.base_model import BaseModel
from utils.fields import ShortUUIDField


class Stream(BaseModel):
    """
    数据流
    """
    DATA_TYPE_CHOICE = (("number", "数值"),)
    name = models.CharField(max_length=16, verbose_name="名称")
    device = models.ForeignKey(
        "device.Device",
        null=True,
        blank=True,
        related_name="streams",
        verbose_name="所属设备",
        on_delete=models.CASCADE,
        db_constraint=False,
    )
    unit_name = models.CharField(max_length=8, blank=True, default="", verbose_name="单位名称")
    unit = models.CharField(max_length=8, blank=True, default="", verbose_name="单位")
    data_type = models.CharField(
        max_length=8, default="number", choices=DATA_TYPE_CHOICE, verbose_name="数据类型"
    )
    show = models.BooleanField(default=False, verbose_name="首页显示")
    image = models.ImageField(null=True, blank=True, verbose_name="图片", upload_to="images/stream")
    icon = models.CharField(null=True, blank=True, max_length=32, verbose_name="icon名称")
    color = models.CharField(null=True, blank=True, max_length=32, verbose_name="背景颜色")
    save_data = models.BooleanField(default=True, verbose_name="保存数据")
    show_chart = models.BooleanField(default=False, verbose_name="显示图表")

    class Meta:
        db_table = "stream"
        verbose_name = "数据流"
        verbose_name_plural = verbose_name
        unique_together = (
            "device",
            "name",
        )

    def __str__(self):
        return self.name
