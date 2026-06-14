# pyre-ignore-all-errors[6,13,15,56]
# pylint: disable=dangerous-default-value,kwarg-superseded-by-positional-arg,no-value-for-parameter
"""
Exercise 3b: Mutable Default Parameters
========================================

Goal: Fix three common bugs caused by mutable default parameters in Python.

Background:
    Default parameter values are evaluated ONCE when the function is defined,
    not each time the function is called. This means mutable defaults (lists, dicts)
    are shared across all calls that don't provide an explicit value.

Instructions:
    1. Fix the three buggy functions below using the None-sentinel pattern.
    2. Run the file to test your fixes: poetry run python exercises/exercise_mutable_defaults.py
    3. Compare your solution with exercise_mutable_defaults_solution.py

Bugs to fix:
    A) add_to_favorites: Shared list default causes all calls to mutate the same list.
    B) log_booking: Shared dict default causes all calls to mutate the same dict.
    C) stamp_ticket: datetime.now() is captured at module import time, not call time.

See exercise_mutable_defaults_solution.py if you get stuck.
"""
from __future__ import annotations

import time
from datetime import datetime


def add_to_favorites(title: str, favorites: list[str] = []) -> list[str]:
    """Add a movie title to the favorites list.

    Args:
        title: The movie title to add.
        favorites: The favorites list (default: empty list).

    Returns:
        The updated favorites list.
    """
    # TODO A: Fix the shared-list bug
    # Hint: Use None as the default and create a new list inside the function.
    favorites.append(title)
    return favorites


def log_booking(booking_id: int, tags: dict[str, str] = {}) -> dict[str, str]:
    """Log a booking with tags metadata.

    Args:
        booking_id: The booking ID.
        tags: Metadata tags (default: empty dict).

    Returns:
        The tags dict with booking_id added.
    """
    # TODO B: Fix the shared-dict bug
    # Hint: Use None as the default and create a new dict inside the function.
    tags['booking_id'] = str(booking_id)
    return tags


def stamp_ticket(movie: str, created_at: datetime = datetime.now()) -> dict[str, str | datetime]:
    """Create a ticket with a timestamp.

    Args:
        movie: The movie title.
        created_at: The creation timestamp (default: now).

    Returns:
        A ticket dict with movie and timestamp.
    """
    # TODO C: Fix the stale-timestamp bug
    # Hint: Use None as the default and call datetime.now() inside the function.
    return {'movie': movie, 'created_at': created_at}


def main() -> None:
    print('=== Testing add_to_favorites ===')
    fav1 = add_to_favorites('Inception')
    fav2 = add_to_favorites('Interstellar')
    print(f'First call: {fav1}')
    print(f'Second call: {fav2}')
    print('Expected: [\'Inception\'] and [\'Interstellar\']')
    print('If both are [\'Inception\', \'Interstellar\'], the bug is still present!')

    print('\n=== Testing log_booking ===')
    log1 = log_booking(123)
    log2 = log_booking(456)
    print(f'First call: {log1}')
    print(f'Second call: {log2}')
    print('Expected: {\'booking_id\': \'123\'} and {\'booking_id\': \'456\'}')
    print('If both have multiple booking_ids, the bug is still present!')

    print('\n=== Testing stamp_ticket ===')
    ticket1 = stamp_ticket('Inception')
    time.sleep(0.01)
    ticket2 = stamp_ticket('Interstellar')
    print(f'First ticket: {ticket1}')
    print(f'Second ticket: {ticket2}')
    print('Expected: Different timestamps for each ticket')
    print('If timestamps are identical, the bug is still present!')


if __name__ == '__main__':
    main()
