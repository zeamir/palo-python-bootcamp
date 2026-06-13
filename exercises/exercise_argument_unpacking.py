"""
Exercise: *args, **kwargs, and Argument Unpacking
===================================================

Goal: Practice using *args/**kwargs to build flexible APIs and using
      * / ** operators to unpack arguments when calling functions.

Instructions:
    1. Complete the function stubs where marked with TODO.
    2. Run the file to test: poetry run python exercises/exercise_argument_unpacking.py
    3. Compare with exercise_argument_unpacking_solution.py if you get stuck.

Tasks:
    A) build_showtime_label:
        - Accept a movie title (required), then any number of extra descriptors
          (e.g., 'IMAX', '3D', 'Dolby Atmos')
        - Return a label like: "Inception [IMAX | 3D | Dolby Atmos]"
        - If no extra descriptors, return just the title: "Inception"

    B) merge_customer_profiles:
        - Accept any number of dicts (profiles) via *args
        - Merge them left-to-right (later dicts override earlier keys)
        - Return the merged dict

    C) unpack_and_book:
        - You are given a tuple of positional args and a dict of keyword args
        - Call the provided _book_ticket function by unpacking them
        - Hint: Use * and ** to unpack when calling

    D) log_call (decorator):
        - Write a decorator that prints the function name, args, and kwargs
          before calling the wrapped function, then prints the result
        - The decorator must preserve the original function's signature
        - Hint: Use functools.wraps and accept *args, **kwargs

    E) build_seat_grid:
        - Given a list of rows ['A', 'B'] and a list of seat numbers [1, 2, 3]
        - Use argument unpacking with a helper to generate all seat labels
        - Return: ['A1', 'A2', 'A3', 'B1', 'B2', 'B3']
"""
# pyre-ignore-all-errors[6,13,15,56]
# pylint: disable=unnecessary-pass,unused-argument,no-self-use,unnecessary-ellipsis,assignment-from-no-return
from __future__ import annotations

from typing import Any, Callable


def build_showtime_label(movie: str, *descriptors: str) -> str:
    """Build a showtime label from a movie title and optional descriptors.

    Args:
        movie: Movie title.
        *descriptors: Optional format descriptors (e.g., 'IMAX', '3D').

    Returns:
        Formatted label string.
    """
    # TODO A: Build the showtime label
    pass


def merge_customer_profiles(*profiles: dict[str, Any]) -> dict[str, Any]:
    """Merge multiple customer profile dicts, later ones overriding earlier.

    Args:
        *profiles: Variable number of profile dictionaries.

    Returns:
        Single merged dictionary.
    """
    # TODO B: Merge all profiles into one dict
    pass


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
    # TODO C: Call _book_ticket with the provided arguments
    pass


def log_call(func: Callable) -> Callable:
    """Decorator that logs function calls and their results.

    Args:
        func: The function to wrap.

    Returns:
        Wrapped function that prints call info and result.
    """
    # TODO D: Implement the decorator
    pass


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
    # TODO E: Generate all seat labels
    # Hint: Think about how to unpack pairs into _format_seat
    pass


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
