"""Exercise Solution: *args, **kwargs, and Argument Unpacking"""
# pyre-ignore-all-errors[6,13,15,56]
# pylint: disable=invalid-name,unused-variable
from __future__ import annotations

import functools
from typing import Any, Callable


def build_showtime_label(movie: str, *descriptors: str) -> str:
    """Build a showtime label from a movie title and optional descriptors.

    Args:
        movie: Movie title.
        *descriptors: Optional format descriptors (e.g., 'IMAX', '3D').

    Returns:
        Formatted label string.
    """
    if descriptors:
        return f'{movie} [{" | ".join(descriptors)}]'
    return movie


def merge_customer_profiles(*profiles: dict[str, Any]) -> dict[str, Any]:
    """Merge multiple customer profile dicts, later ones overriding earlier.

    Args:
        *profiles: Variable number of profile dictionaries.

    Returns:
        Single merged dictionary.
    """
    merged: dict[str, Any] = {}
    for profile in profiles:
        merged = {**merged, **profile}
    return merged


def _book_ticket(movie: str, seat: str, customer: str, vip: bool = False) -> dict[str, Any]:
    """Internal booking function (DO NOT MODIFY)."""
    return {
        'movie': movie,
        'seat': seat,
        'customer': customer,
        'vip': vip,
    }


def unpack_and_book(positional_args: tuple, keyword_args: dict[str, Any]) -> dict[str, Any]:
    """Call _book_ticket by unpacking the provided args and kwargs.

    Args:
        positional_args: Tuple of positional arguments for _book_ticket.
        keyword_args: Dict of keyword arguments for _book_ticket.

    Returns:
        The booking dict returned by _book_ticket.
    """
    return _book_ticket(*positional_args, **keyword_args)


def log_call(func: Callable) -> Callable:
    """Decorator that logs function calls and their results.

    Args:
        func: The function to wrap.

    Returns:
        Wrapped function that prints call info and result.
    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f'Calling {func.__name__} with args={args} kwargs={kwargs}')
        result = func(*args, **kwargs)
        print(f'Result: {result}')
        return result

    return wrapper


def _format_seat(row: str, number: int) -> str:
    """Format a single seat label (DO NOT MODIFY)."""
    return f'{row}{number}'


def build_seat_grid(rows: list[str], seat_numbers: list[int]) -> list[str]:
    """Build a grid of seat labels from rows and seat numbers.

    Args:
        rows: List of row letters (e.g., ['A', 'B']).
        seat_numbers: List of seat numbers (e.g., [1, 2, 3]).

    Returns:
        List of seat labels (e.g., ['A1', 'A2', 'A3', 'B1', 'B2', 'B3']).
    """
    pairs = [(row, num) for row in rows for num in seat_numbers]
    return [_format_seat(*pair) for pair in pairs]


def main() -> None:
    print('=== Task A: build_showtime_label ===')
    label1 = build_showtime_label('Inception')
    label2 = build_showtime_label('Inception', 'IMAX', '3D', 'Dolby Atmos')
    print(f'No descriptors: {label1}')
    print(f'With descriptors: {label2}')
    assert label1 == 'Inception'
    assert label2 == 'Inception [IMAX | 3D | Dolby Atmos]'
    print()

    print('=== Task B: merge_customer_profiles ===')
    base = {'name': 'Alice', 'email': 'alice@old.com', 'tier': 'silver'}
    update1 = {'email': 'alice@new.com', 'phone': '555-0123'}
    update2 = {'tier': 'gold', 'vip': True}
    merged = merge_customer_profiles(base, update1, update2)
    print(f'Merged: {merged}')
    assert merged == {'name': 'Alice', 'email': 'alice@new.com', 'tier': 'gold', 'phone': '555-0123', 'vip': True}
    print()

    print('=== Task C: unpack_and_book ===')
    args_tuple = ('The Matrix', 'B7')
    kwargs_dict = {'customer': 'Neo', 'vip': True}
    booking = unpack_and_book(args_tuple, kwargs_dict)
    print(f'Booking: {booking}')
    assert booking == {'movie': 'The Matrix', 'seat': 'B7', 'customer': 'Neo', 'vip': True}
    print()

    print('=== Task D: log_call ===')

    @log_call
    def add_tickets(a: int, b: int) -> int:
        return a + b

    result = add_tickets(3, 5)
    assert result == 8
    assert add_tickets.__name__ == 'add_tickets'
    print()

    print('=== Task E: build_seat_grid ===')
    grid = build_seat_grid(['A', 'B'], [1, 2, 3])
    print(f'Seat grid: {grid}')
    assert grid == ['A1', 'A2', 'A3', 'B1', 'B2', 'B3']

    print('\nAll assertions passed!')


if __name__ == '__main__':
    main()
