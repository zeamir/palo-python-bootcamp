"""Pydantic base models with automatic field name aliasing.

This module provides base model classes that automatically convert Python
snake_case field names to different naming conventions (camelCase, TitleCase,
PascalCase) during JSON serialization. All models support bidirectional
population using either aliases or original field names.

Example:
    class UserResponse(CamelCaseModel):
        user_name: str
        created_at: DatetimeUTC

    response = UserResponse(user_name="john", created_at=datetime.now())
    response.model_dump_json()  # {"userName": "john", "createdAt": "2024-..."}
"""
# pyre-ignore-all-errors[8,11,28]
# pylint: disable=no-value-for-parameter,unused-argument
# noinspection DuplicatedCode
from __future__ import annotations

import functools
import json
from abc import ABC
from datetime import datetime
from typing import Any, Dict

import pydantic
from pydantic import BaseModel, WrapSerializer
from pydantic.alias_generators import to_camel, to_pascal
from pydantic_core.core_schema import SerializerFunctionWrapHandler
from typing_extensions import Annotated

from ticketing_system.time_utils import to_iso8601_utc_str

DictStrAny = Dict[str, Any]


def title_case(string: str) -> str:
    """Convert a snake_case string to TitleCase (PascalCase).

    Similar to camelCase but with the first letter capitalized.

    Args:
        string: Snake_case string to convert.

    Returns:
        TitleCase string (e.g., 'my_field' -> 'MyField').
    """
    return string[0].upper() + to_camel(string)[1:]


def ser_datetime_wrap(v: Any, nxt: SerializerFunctionWrapHandler) -> str:
    """Serialize datetime to ISO 8601 UTC string format."""
    return to_iso8601_utc_str(v)


# Datetime type that serializes to ISO 8601 UTC format in JSON.
DatetimeUTC = Annotated[datetime, WrapSerializer(ser_datetime_wrap, when_used='json')]


class BaseDictModel(
        BaseModel,
        ABC,
        loc_by_alias=True,
):
    """Abstract base model with dictionary and JSON serialization helpers.

    Provides methods for converting models to dictionaries and JSON strings,
    with support for masking sensitive fields in subclasses.
    """

    def masked_dict(self) -> dict[str, Any]:
        """Return a dictionary representation with sensitive fields masked.

        Override in subclasses to hide sensitive data like passwords or tokens.
        Default implementation returns the full native_dict().

        Returns:
            Dictionary with string keys and primitive values.
        """
        return self.native_dict()

    def masked_json(self, indent: int = 0) -> str:
        """Return JSON string with sensitive fields masked.

        Args:
            indent: Number of spaces for indentation. 0 for compact JSON.

        Returns:
            JSON string representation with masked sensitive fields.
        """
        if indent:
            return json.dumps(self.masked_dict(), indent=indent)
        else:
            return json.dumps(self.masked_dict())

    def native_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable dictionary with primitive values.

        Converts all values to JSON-compatible primitives (no objects,
        enums, or complex types). Suitable for passing to json.dumps().

        Returns:
            Dictionary with all values as JSON primitives.
        """
        return json.loads(self.model_dump_json())

    def __str__(self) -> str:
        return f'{self.masked_dict()}'

    def __repr__(self) -> str:
        return f'{self.masked_dict()}'


class AliasedBaseModel(BaseDictModel, pydantic.BaseModel, populate_by_name=True):
    """Base model that serializes using field aliases.

    Accepts input using either field names or aliases (populate_by_name=True).
    Serialization methods (model_dump, model_dump_json) use aliases by default.
    """


# override the default json and dict methods to use by_alias=True
AliasedBaseModel.model_dump_json = functools.partialmethod(AliasedBaseModel.model_dump_json, by_alias=True)
AliasedBaseModel.model_dump = functools.partialmethod(AliasedBaseModel.model_dump, by_alias=True)


class CamelCaseModel(BaseDictModel, populate_by_name=True, alias_generator=to_camel):
    """Base model that converts snake_case fields to camelCase in JSON.

    Example:
        class User(CamelCaseModel):
            first_name: str  # Serializes as "firstName"
    """


# override the default json and dict methods to use by_alias=True
CamelCaseModel.model_dump_json = functools.partialmethod(CamelCaseModel.model_dump_json, by_alias=True)
CamelCaseModel.model_dump = functools.partialmethod(CamelCaseModel.model_dump, by_alias=True)


class TitleCaseModel(BaseDictModel, populate_by_name=True, alias_generator=title_case):
    """Base model that converts snake_case fields to Title Case in JSON.

    Example:
        class User(TitleCaseModel):
            first_name: str  # Serializes as "First Name"
    """


# override the default json and dict methods to use by_alias=True
TitleCaseModel.model_dump_json = functools.partialmethod(TitleCaseModel.model_dump_json, by_alias=True)
TitleCaseModel.model_dump = functools.partialmethod(TitleCaseModel.model_dump, by_alias=True)


class PascalCaseModel(BaseDictModel, populate_by_name=True, alias_generator=to_pascal):
    """Base model that converts snake_case fields to PascalCase in JSON.

    Example:
        class User(PascalCaseModel):
            first_name: str  # Serializes as "FirstName"
    """


# override the default json and dict methods to use by_alias=True
PascalCaseModel.model_dump_json = functools.partialmethod(PascalCaseModel.model_dump_json, by_alias=True)
PascalCaseModel.model_dump = functools.partialmethod(PascalCaseModel.model_dump, by_alias=True)
