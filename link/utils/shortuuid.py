from typing import Any, Tuple

from shortuuid.django_fields import ShortUUIDField as _ShortUUIDField


class ShortUUIDField(_ShortUUIDField):
    def __init__(self, *args: Tuple, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.db_index: bool = kwargs.pop("db_index", True)
        self._unique: bool = kwargs.pop("unique", True)
        self.length: int = kwargs.pop("length", 12)
        self.alphabet: str = kwargs.pop("alphabet", "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")
