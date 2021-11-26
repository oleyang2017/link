from django.db import models
from django.conf import settings


class BaseManager(models.Manager):
    
    def get_queryset(self):
        if 'deleted' in self.model:
            return 


class BaseModel(models.Model):
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='创建人', on_delete=models.SET_NULL, null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True
        # objects = BaseManager()



