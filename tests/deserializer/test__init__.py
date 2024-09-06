"""Test functions in __init__.py."""

from typing import Any
from deserializer import deserialize
from deserializer import get_log_level
from deserializer import set_log_level


def test_log_level():
    """Test set_log_level and get_log_level function."""
    set_log_level("DEBUG")
    assert get_log_level() == "DEBUG"


def test_deserialize():
    """Test deserialize function when everything is fine."""

    class NestedClass:
        value1: int = 1

    class TestClass:
        value1: int = 0
        value2: str | None = None
        value3: NestedClass = NestedClass()

    json: dict[str, Any] = {"value1": 1, "value2": "test", "value3": {"value1": 3}}

    instance = deserialize(TestClass, json)
    assert instance.value1 == 1
    assert instance.value2 == "test"
    assert instance.value3.value1 == 3
