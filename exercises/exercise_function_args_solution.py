# pyre-ignore-all-errors[6,13,15,56]
"""Exercise Solution: Function Arguments"""
from __future__ import annotations


def format_ticket(*, movie: str, seat: str, price: float) -> str:
    """Format a ticket string with movie, seat, and price (all args must be named).

    Args:
        movie: Movie title.
        seat: Seat identifier.
        price: Ticket price in USD.

    Returns:
        Formatted ticket string.
    """
    return f'Ticket: {movie} | Seat {seat} | ${price:.2f}'


def calculate_group_total(*prices: float) -> float:
    """Calculate total price for a group of tickets with 10% discount.

    Args:
        *prices: Variable number of ticket prices.

    Returns:
        Total price with 10% group discount applied.
    """
    total = sum(prices)
    discount = total * 0.10
    return total - discount


def create_event(title: str, **details: str | int) -> dict:
    """Create an event with title and flexible keyword details.

    Args:
        title: Event title (required).
        **details: Additional event details (e.g., venue, time, duration).

    Returns:
        Event details dict including title and all additional details.
    """
    return {'title': title, **details}


def process_booking(
    booking_id: int,
    /,
    *ticket_ids: str,
    customer_email: str,
    **metadata: str | int
) -> dict:
    """Process a booking with combined argument types.

    Args:
        booking_id: Booking ID (positional-only).
        *ticket_ids: Variable number of ticket IDs.
        customer_email: Customer email (keyword-only).
        **metadata: Additional booking metadata.

    Returns:
        Booking details dict.
    """
    return {
        'booking_id': booking_id,
        'customer_email': customer_email,
        'ticket_ids': list(ticket_ids),
        'metadata': metadata,
    }


if __name__ == '__main__':
    print('=== Task A: format_ticket ===')
    ticket = format_ticket(movie='Inception', seat='A12', price=15.0)
    print(f'Formatted: {ticket}')
    # Test that positional fails:
    try:
        bad_ticket = format_ticket('Inception', 'A12', 15.0)  # type: ignore
    except TypeError as e:
        print(f'Positional call correctly rejected: {e}')
    print()

    print('=== Task B: calculate_group_total ===')
    total1 = calculate_group_total(15.0, 15.0, 12.0)
    total2 = calculate_group_total(20.0, 20.0, 20.0, 18.0)
    print(f'Group of 3 tickets: ${total1:.2f} (expected: $37.80)')
    print(f'Group of 4 tickets: ${total2:.2f} (expected: $70.20)')
    print()

    print('=== Task C: create_event ===')
    event1 = create_event('Star Wars Marathon')
    event2 = create_event('Star Wars Marathon', venue='Theater 3', time='7pm', duration=420)
    print(f'Event 1: {event1}')
    print(f'Event 2: {event2}')
    print()

    print('=== Task D: process_booking ===')
    booking1 = process_booking(101, customer_email='alice@example.com')
    booking2 = process_booking(
        102,
        'TKT-001', 'TKT-002',
        customer_email='bob@example.com',
        payment_method='credit_card',
        total=42
    )
    print(f'Booking 1: {booking1}')
    print(f'Booking 2: {booking2}')
    # Test that keyword booking_id fails:
    try:
        bad_booking = process_booking(booking_id=103, customer_email='test@example.com')  # type: ignore
    except TypeError as e:
        print(f'Keyword booking_id correctly rejected: {e}')
