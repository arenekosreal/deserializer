"""Type defines of deserializer."""

from typing import Literal
from typing import Callable
from typing import Protocol


class NonArgumentConstructorProtocol(Protocol):
    """A protocol requires class with non-argument constructor."""

    def __init__(self):
        """The constructor of the class."""


JsonType = dict[str, "str | bool | int | JsonType | None"]
KeyConverterType = Callable[[str], str] | None
LogLevelType = Literal["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
