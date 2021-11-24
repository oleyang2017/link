from django.db import models
from django.conf import settings
from hashids import Hashids

hashids = Hashids(salt=settings.SECRET_KEY, min_length=8)


class BaseModel(models.Model):
    """
    基础模型
    一般的模型都应该继承这个模型定义，这里会实现一些通用的处理，例如匿名ID（将ID加密返回出去，查询的时候再解密）
    权限问题
    manager
    缓存
    """
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='创建人', on_delete=models.SET_NULL)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class BaseManager(models.Manager):
    def get_queryset(self):
        print(11111)

        ret = super(BaseManager, self).get_queryset()
        for each in ret:
            each.id = hashids.encode(int(each.id))
            print(type(each.id))
            print(hashids.encode(each.id))
            print(hashids.encode(1))
            print(each.id)
            each.id = hashids.encode(1)
        print(ret)
        print(555)
        return ret
    
    def all(self):
        print(3333)
        ret = super(BaseManager, self).all()
        for each in ret:
            print(each.id)
        print(ret)
        print(344444)
        return ret

