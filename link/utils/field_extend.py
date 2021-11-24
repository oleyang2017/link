from django.db import models
import shortuuid


class ShortUUIDField(models.CharField):

    def __init__(self, generate=True, *args, **kwargs):
        self.generate = generate
        kwargs['max_length'] = 22
        if generate:
            kwargs['editable'] = False
            kwargs['blank'] = True
            kwargs['unique'] = True

        super(ShortUUIDField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        value = super(ShortUUIDField, self).pre_save(model_instance, add)
        if self.generate and not value:
            if self.max_length != 22:
                value = shortuuid.ShortUUID.random(self.max_length)
            else:
                value = shortuuid.uuid()
            setattr(model_instance, self.attname, value)
        return value

    def formfield(self, **kwargs):
        if self.generate:
            return None
        return super(ShortUUIDField, self).formfield(**kwargs)
