from hashids import Hashids
from django.conf import settings

hashids = Hashids(salt=settings.SECRET_KEY, min_length=8)


class AnonymousId:

    def encode(self, value):
        return hashids.encode(value)

    def decode(self, values):
        return hashids.decode(values)


anonymous_id = AnonymousId()
