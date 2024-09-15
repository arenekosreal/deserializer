"""Test functions in utils.py."""

from deserializer.utils import is_type_match
from deserializer.utils import is_valid_json
from deserializer.utils import to_valid_class


def test_is_type_match():
    """Test is_type_match function."""
    assert is_type_match(1, int)
    assert is_type_match([1], list[int])
    assert is_type_match([], list[int])
    assert is_type_match({"1": 1}, dict[str, int])
    assert is_type_match({}, dict[str, int])
    assert not is_type_match(1, str)
    assert not is_type_match([1], list[str])
    assert not is_type_match({"1": 1}, dict[str, str])


def test_is_valid_json():
    """Test is_valid_json function."""
    assert is_valid_json({"test": "value"})
    assert not is_valid_json({1: "value"})


def test_to_valid_class():
    """Test to_valid_class function."""
    _ = to_valid_class(int | None)
