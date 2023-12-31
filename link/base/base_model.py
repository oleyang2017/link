import logging

from django.db import models
from django.conf import settings

logger = logging.getLogger(__name__)


# class BaseManager(models.Manager):
#     def get_queryset(self):
#         self.check_deleted_field()
#         return super(BaseManager, self).get_queryset().filter(deleted=False)
#
#     def check_deleted_field(self):
#         try:
#             self.model._meta.get_field("deleted")
#         except FieldDoesNotExist:
#             logger.error("model不存在deleted字段，不可以使用软删除")
#
#     def get_raw_queryset(self):
#         """获取原始queryset"""
#         return super(BaseManager, self).get_queryset()


class BaseModel(models.Model):
    create_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="创建人",
        on_delete=models.CASCADE,
        db_constraint=False,
    )
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    last_update_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="最后一次修改人",
        on_delete=models.DO_NOTHING,
        null=True,
        db_constraint=False,
        related_name="+",
    )

    class Meta:
        abstract = True
