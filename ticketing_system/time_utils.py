"""Time utilities for UTC datetime handling.

This module provides functions for converting, formatting, and manipulating
datetime objects with UTC timezone handling. All functions expect and return
timezone-aware datetime objects.
"""
from datetime import UTC, datetime, timedelta, timezone
from typing import Callable, Final

_TIMEDELTA_ZERO = timedelta()

# "UTC timezone name constant.
_UTC: Final = 'UTC'


def to_utc_datetime(dt_with_tz: datetime) -> datetime:
    """Convert a timezone-aware datetime to UTC.

    Args:
        dt_with_tz: Datetime with timezone info attached.

    Returns:
        Datetime adjusted to UTC with UTC timezone info.

    Raises:
        ValueError: If the datetime has no timezone info.
    """
    if not dt_with_tz.tzinfo:
        raise ValueError('timezone info is missing')

    if dt_with_tz.tzname() == _UTC:
        # already UTC, so just return it
        return dt_with_tz

    # transform to UTC and return
    return dt_with_tz.astimezone(timezone.utc)


def time_of(datetime_str: str) -> datetime:
    """Parse an ISO 8601 datetime string to a UTC datetime.

    Args:
        datetime_str: ISO 8601 formatted datetime string (e.g., '2020-01-15T10:30:00Z').

    Returns:
        Datetime adjusted to UTC with UTC timezone info.

    Raises:
        ValueError: If the datetime string does not include timezone info.
    """

    if datetime_str[-1] == 'Z':
        datetime_str = datetime_str.replace('Z', '+00:00')
    _dt = datetime.fromisoformat(datetime_str)

    if not _dt.tzinfo:
        raise ValueError('Must provide datetime is iso 8601 with timezone')

    return to_utc_datetime(_dt)


# Alias for time_of function.
utc_datetime_from_iso8601: Callable[[str], datetime] = time_of


def to_iso8601_utc_str(dt_with_tz: datetime, time_delta: timedelta = _TIMEDELTA_ZERO) -> str:
    """Convert a datetime to ISO 8601 UTC string format.

    Args:
        dt_with_tz: Datetime with timezone info.
        time_delta: Optional timedelta to add before formatting. Defaults to zero.

    Returns:
        ISO 8601 formatted string with milliseconds precision (e.g., '2020-02-28T09:03:54.597Z').

    Raises:
        ValueError: If the datetime has no timezone info.
    """
    utc_dt = to_utc_datetime(dt_with_tz) + time_delta

    native_iso_str = utc_dt.isoformat(sep='T', timespec='milliseconds')
    # this yields the following string:   '2022-11-13T08:59:59.123+00:00'
    # replace the last 6 chars, which represent the timezone (+00:00) with 'Z'.
    return native_iso_str[:-6] + 'Z'


def epoch_time() -> int:
    """Get current UTC time as Unix epoch timestamp.

    Returns:
        Current time as integer seconds since Unix epoch.
    """
    return int(utcnow().timestamp())


def get_current_utc_time_format_for_http_response() -> str:
    """Get current UTC time formatted for HTTP responses.

    Returns:
        UTC time string in format '2020-04-21T06:50:39.331+0000'.
    """
    utc_time_str = str(datetime.now(UTC))
    # not transform this format '2020-04-21T06:50:39.331915' to '2020-04-21T06:50:39.331+0000'
    return f'{utc_time_str[:10]}T{utc_time_str[11:23]}+0000'


def utcnow() -> datetime:
    """Get current UTC datetime with millisecond precision.

    Microseconds are truncated to the nearest millisecond for consistency
    with ISO 8601 millisecond formatting.

    Returns:
        Current UTC datetime with millisecond precision.
    """
    ret = datetime.now(UTC)
    return ret.replace(microsecond=ret.microsecond - ret.microsecond % 1000)
