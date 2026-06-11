# pyre-ignore-all-errors[6,13,15,56]
"""
Exercise 3b: Mutable Default Parameters — SOLUTION
===================================================

This file contains the complete fixed versions of all three functions.
"""
from __future__ import annotations

from datetime import datetime


def add_to_favorites(title: str, favorites: list[str] | None = None) -> list[str]:
    """Add a movie title to the favorites list.

    Args:
        title: The movie title to add.
        favorites: The favorites list (default: None, creates new list).

    Returns:
        The updated favorites list.
    """
    # SOLUTION A: Use None as sentinel, create new list inside function body.
    # This ensures each call gets its own fresh list when no argument is provided.
    if favorites is None:
        favorites = []
    favorites.append(title)
    return favorites


def log_booking(booking_id: int, tags: dict[str, str] | None = None) -> dict[str, str]:
    """Log a booking with tags metadata.

    Args:
        booking_id: The booking ID.
        tags: Metadata tags (default: None, creates new dict).

    Returns:
        The tags dict with booking_id added.
    """
    # SOLUTION B: Use None as sentinel, create new dict inside function body.
    # This ensures each call gets its own fresh dict when no argument is provided.
    if tags is None:
        tags = {}
    tags['booking_id'] = str(booking_id)
    return tags


def stamp_ticket(movie: str, created_at: datetime | None = None) -> dict[str, str | datetime]:
    """Create a ticket with a timestamp.

    Args:
        movie: The movie title.
        created_at: The creation timestamp (default: None, captures now() at call time).

    Returns:
        A ticket dict with movie and timestamp.
    """
    # SOLUTION C: Use None as sentinel, call datetime.now() inside function body.
    # This ensures the timestamp is captured at call time, not at module import time.
    if created_at is None:
        created_at = datetime.now()
    return {'movie': movie, 'created_at': created_at}


if __name__ == '__main__':
    print('=== Testing add_to_favorites ===')
    fav1 = add_to_favorites('Inception')
    fav2 = add_to_favorites('Interstellar')
    print(f'First call: {fav1}')
    print(f'Second call: {fav2}')
    assert fav1 == ['Inception'], f'Expected [\'Inception\'], got {fav1}'
    assert fav2 == ['Interstellar'], f'Expected [\'Interstellar\'], got {fav2}'
    print('✓ Each call gets its own list')

    print('\n=== Testing log_booking ===')
    log1 = log_booking(123)
    log2 = log_booking(456)
    print(f'First call: {log1}')
    print(f'Second call: {log2}')
    assert log1 == {'booking_id': '123'}, f'Expected {{\'booking_id\': \'123\'}}, got {log1}'
    assert log2 == {'booking_id': '456'}, f'Expected {{\'booking_id\': \'456\'}}, got {log2}'
    print('✓ Each call gets its own dict')

    print('\n=== Testing stamp_ticket ===')
    ticket1 = stamp_ticket('Inception')
    import time
    time.sleep(0.01)
    ticket2 = stamp_ticket('Interstellar')
    print(f'First ticket: {ticket1}')
    print(f'Second ticket: {ticket2}')
    assert ticket1['created_at'] != ticket2['created_at'], 'Timestamps should be different'
    print('✓ Each call captures its own timestamp')

    print('\n=== All tests passed! ===')
