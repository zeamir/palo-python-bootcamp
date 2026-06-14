"""
Mutable Default Parameters — A Common Python Pitfall
=====================================================

Default parameter values in Python are evaluated ONCE when the function is defined,
not each time the function is called. This means that mutable defaults (lists, dicts,
custom objects) are shared across all calls that don't provide an explicit value.

This file demonstrates the bug in action and shows the correct fix.
"""
# pylint: disable=dangerous-default-value
from __future__ import annotations

import time
from datetime import datetime

# ============================================================================
# Section 1: The List Default Bug
# ============================================================================


def add_to_watchlist_buggy(movie: str, watchlist: list[str] = []) -> list[str]:
    """Add a movie to a watchlist. BUGGY VERSION — default list is shared.

    Args:
        movie: The movie title to add.
        watchlist: The watchlist to add to (default: empty list).

    Returns:
        The updated watchlist.
    """
    watchlist.append(movie)
    return watchlist


def add_to_watchlist_fixed(movie: str, watchlist: list[str] | None = None) -> list[str]:
    """Add a movie to a watchlist. FIXED VERSION — creates a new list each time.

    Args:
        movie: The movie title to add.
        watchlist: The watchlist to add to (default: None, creates new list).

    Returns:
        The updated watchlist.
    """
    # The fix: use None as sentinel, then create a new list inside the function body.
    if watchlist is None:
        watchlist = []
    watchlist.append(movie)
    return watchlist


# ============================================================================
# Section 2: The Dict Default Bug
# ============================================================================


def register_customer_buggy(name: str, preferences: dict[str, str] = {}) -> dict[str, str]:
    """Register a customer with preferences. BUGGY VERSION — default dict is shared.

    Args:
        name: Customer name.
        preferences: Customer preferences (default: empty dict).

    Returns:
        The customer preferences dict.
    """
    preferences['name'] = name
    return preferences


def register_customer_fixed(name: str, preferences: dict[str, str] | None = None) -> dict[str, str]:
    """Register a customer with preferences. FIXED VERSION — creates new dict each time.

    Args:
        name: Customer name.
        preferences: Customer preferences (default: None, creates new dict).

    Returns:
        The customer preferences dict.
    """
    # The fix: use None as sentinel, then create a new dict inside the function body.
    if preferences is None:
        preferences = {}
    preferences['name'] = name
    return preferences


# ============================================================================
# Section 3: The Timestamp Default Bug
# ============================================================================


def create_ticket_buggy(movie: str, booked_at: datetime = datetime.now()) -> dict[str, str | datetime]:
    """Create a ticket with booking timestamp. BUGGY VERSION — timestamp captured at import time.

    Args:
        movie: The movie title.
        booked_at: The booking timestamp (default: datetime.now() evaluated at module load).

    Returns:
        A ticket dict with movie and timestamp.

    The bug: datetime.now() is evaluated ONCE when the function is defined (at module import),
    not each time the function is called. All tickets will have the same timestamp!
    """
    return {'movie': movie, 'booked_at': booked_at}


def create_ticket_fixed(movie: str, booked_at: datetime | None = None) -> dict[str, str | datetime]:
    """Create a ticket with booking timestamp. FIXED VERSION — timestamp captured at call time.

    Args:
        movie: The movie title.
        booked_at: The booking timestamp (default: None, captures now() at call time).

    Returns:
        A ticket dict with movie and timestamp.
    """
    # The fix: use None as sentinel, then call datetime.now() inside the function body.
    if booked_at is None:
        booked_at = datetime.now()
    return {'movie': movie, 'booked_at': booked_at}


# ============================================================================
# Demonstrations
# ============================================================================


def main() -> None:
    print('=== Section 1: List Default Bug ===')
    print('\nBUGGY VERSION:')
    # Call the buggy function twice without providing a watchlist.
    # Both calls share the SAME default list!
    result1 = add_to_watchlist_buggy('Inception')
    result2 = add_to_watchlist_buggy('Interstellar')
    print(f'First call result: {result1}')
    print(f'Second call result: {result2}')
    print('^ BUG: Both calls see BOTH movies because they share the same default list!')

    print('\nFIXED VERSION:')
    result3 = add_to_watchlist_fixed('Inception')
    result4 = add_to_watchlist_fixed('Interstellar')
    print(f'First call result: {result3}')
    print(f'Second call result: {result4}')
    print('^ CORRECT: Each call gets its own fresh list.')

    print('\n=== Section 2: Dict Default Bug ===')
    print('\nBUGGY VERSION:')
    # Both calls mutate the same default dict.
    cust1 = register_customer_buggy('Alice')
    cust2 = register_customer_buggy('Bob')
    print(f'First customer: {cust1}')
    print(f'Second customer: {cust2}')
    print('^ BUG: Both customers share the same dict — Bob overwrote Alice!')

    print('\nFIXED VERSION:')
    cust3 = register_customer_fixed('Alice')
    cust4 = register_customer_fixed('Bob')
    print(f'First customer: {cust3}')
    print(f'Second customer: {cust4}')
    print('^ CORRECT: Each customer gets their own dict.')

    print('\n=== Section 3: Timestamp Default Bug ===')
    print('\nBUGGY VERSION:')
    # The timestamp is captured once when the function is defined, not when it's called.
    ticket1 = create_ticket_buggy('Inception')
    print('Waiting 0.001 seconds...')
    time.sleep(0.001)
    ticket2 = create_ticket_buggy('Interstellar')
    print(f'First ticket: {ticket1}')
    print(f'Second ticket: {ticket2}')
    print('^ BUG: Both tickets have the SAME timestamp (or very close) because datetime.now() was evaluated once at import time.')

    print('\nFIXED VERSION:')
    ticket3 = create_ticket_fixed('Inception')
    time.sleep(0.001)
    ticket4 = create_ticket_fixed('Interstellar')
    print(f'First ticket: {ticket3}')
    print(f'Second ticket: {ticket4}')
    print('^ CORRECT: Each ticket captures the current time at call time.')

    print('\n=== Summary ===')
    print('Rule of thumb: NEVER use mutable defaults (list, dict, set, custom objects).')
    print('Always use None as the sentinel and create the mutable object inside the function body.')


if __name__ == '__main__':
    main()
