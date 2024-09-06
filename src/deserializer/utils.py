"""Utils for deserializer."""
# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownVariableType=false
# pyright: reportAny=false

import inspect
from types import UnionType
from typing import Any
from typing import Literal
from typing import Callable
from typing import TypeGuard
from typing import get_args
from typing import get_origin
from deserializer.defines import JsonType
from deserializer.defines import NonArgumentConstructorProtocol


CheckerType = Callable[[object], TypeGuard[type[NonArgumentConstructorProtocol]]]


def _is_type_args_infinite(t: type) -> bool:
    return t is Literal or t is UnionType or t is tuple


def _is_type_list_like(t: type) -> bool:
    return t is list or t is set


def _is_type_dict_like(t: type) -> bool:
    return t is dict


def _is_union_type(i: object) -> TypeGuard[UnionType]:
    return get_origin(i) is UnionType


def _check_generics(i: object, origin: type, args: tuple[Any, ...]) -> bool:
    if _is_type_args_infinite(origin):
        return type(i) in args
    if _is_type_list_like(origin):
        return is_type_match(i, args[0])
    if _is_type_dict_like(origin):
        return is_type_match(i, args[1])
    raise NotImplementedError("Unsupported type {}".format(origin))


def _is_parameters_valid(*parameters: inspect.Parameter) -> bool:
    if len(parameters) == 0:
        return False
    if parameters[0].name != "self":
        return False
    for parameter in parameters[1:]:
        allowed_empty_default_parameter_kinds = [
            inspect.Parameter.VAR_POSITIONAL,
            inspect.Parameter.VAR_KEYWORD,
        ]
        if (
            parameter.default == inspect.Parameter.empty
            and parameter.kind not in allowed_empty_default_parameter_kinds
        ):
            return False
    return True


def is_valid_json(i: object) -> TypeGuard[JsonType]:
    """Check if object given is JsonType."""

    def is_value_match(i: object) -> bool:
        return isinstance(i, str | int | bool | None) or is_valid_json(i)

    if isinstance(i, dict):
        keys_match = all(isinstance(key, str) for key in i)
        values_match = all(is_value_match(value) for value in i.values())
        return keys_match and values_match
    return False


def _is_valid_class(i: object) -> TypeGuard[type[NonArgumentConstructorProtocol]]:
    if isinstance(i, type) and hasattr(i, "__init__") and callable(i.__init__):
        signature = inspect.signature(i.__init__)
        return _is_parameters_valid(*signature.parameters.values())
    return False


def to_valid_class(
    i: object,
    checker: CheckerType = _is_valid_class,
) -> type[NonArgumentConstructorProtocol]:
    """Convert type given to NonArgumentConstructor."""
    if checker(i):
        return i
    if _is_union_type(i):
        args = get_args(i)
        for arg in args:
            if checker(arg):
                return arg
        raise ValueError("No type matches checker can be extracted from UnionType.")
    raise NotImplementedError("Unsupported object {}".format(i))


def is_type_match(i: object, t: type) -> bool:
    """Check if object matches type given."""
    args = get_args(t)
    if len(args) > 0:
        origin = get_origin(t)
        if origin is None:
            # t is not a generic type, which does not match len(args) > 0
            # So this should never be reached.
            return False
        return _check_generics(i, origin, args)
    return isinstance(i, t)
