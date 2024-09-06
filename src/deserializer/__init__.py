"""Deserialize class from dict from json/yaml/toml."""
# pyright: reportAny=false

import inspect
import logging
from typing import TypeVar
from deserializer.utils import is_type_match
from deserializer.utils import is_valid_json
from deserializer.utils import to_valid_class
from deserializer.defines import JsonType
from deserializer.defines import LogLevelType
from deserializer.defines import KeyConverterType
from deserializer.defines import NonArgumentConstructorProtocol


__version__ = "0.1.0"
__all__ = ["deserialize", "get_log_level", "set_log_level"]


T = TypeVar("T", bound=NonArgumentConstructorProtocol)


_logger = logging.getLogger(__name__)
_fmt = logging.Formatter("%(asctime)s-%(levelname)s-%(message)s", "%Y-%m-%d %H:%M:%S")
_logger.addHandler(logging.StreamHandler())
for handler in _logger.handlers:
    handler.setFormatter(_fmt)


def set_log_level(level: LogLevelType):
    """Set the log level of this module."""
    _logger.setLevel(level)
    for handler in _logger.handlers:
        handler.setLevel(level)


def get_log_level() -> LogLevelType:
    """Get the log level of this module."""
    level = logging.getLevelName(_logger.level)
    match level:
        case "DEBUG" | "INFO" | "WARNING" | "ERROR" | "CRITICAL":
            return level
        case _:
            return "NOTSET"


def deserialize(
    type_of_object: type[T],
    json: JsonType,
    key_converter: KeyConverterType = None,
) -> T:
    """Deserialize class from dict from json/yaml/toml.

    Args:
        type_of_object: type[T]: The class itself.
        json: JsonType: The input json.
        key_converter: KeyConverterType: a function converts json key to attribute name.

    Returns:
        T: The instance of the class given.

    Example:
        ```python
        class NestedClass:
            nested_value1: str = "value1"

        class MyClass:
            value1: int = 0
            value2: str = "value2"
            value3: int | None = None
            value4: NestedClass | None = None

        json = {
            "value1": 1,
            "value2": "changed-value2",
            "value3": 3
        }
        instance = deserialize(MyClass, json)
        isinstance(instance, MyClass)       # True
        instance.value1 == 1                # True
        instance.value2 == "changed-value2" # True
        instance.value3 == 3                # True
        instance.value4 is None             # True

        json_adds_nested_class = json.copy()
        json_adds_nested_class["value4"] = {
            "nested_value1": "nested_value1"
        }
        instance2 = deserialize(MyClass, json_adds_nested_class)
        nested_class = instance2.value4
        nested_class is not None                        # True
        nested_class.nested_value1 == "nested_value1"   # True
        ```
    """
    types_of_instance = inspect.get_annotations(type_of_object)
    instance = type_of_object()
    for key, value in json.items():
        attribute_name = key_converter(key) if key_converter is not None else key
        if hasattr(instance, attribute_name):
            type_of_attribute = types_of_instance.get(attribute_name)
            if type_of_attribute is None:
                _logger.error(
                    "Cannot get type annotations of %s.%s, ignoring.",
                    type_of_object.__name__,
                    attribute_name,
                )
            elif is_valid_json(value):
                _logger.debug("Calling deserialize() recursively...")
                deserialized_value = deserialize(
                    to_valid_class(type_of_attribute),
                    value,
                    key_converter,
                )
                setattr(instance, attribute_name, deserialized_value)
            elif is_type_match(value, type_of_attribute):
                _logger.debug(
                    "Type match, setting value of %s directly.", attribute_name
                )
                setattr(instance, attribute_name, value)
            else:
                _logger.error(
                    "Do not know how to deserialize %s, ignoring.", attribute_name
                )
    return instance


set_log_level("INFO")
