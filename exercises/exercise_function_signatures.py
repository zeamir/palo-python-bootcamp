"""
Exercise: Function Arguments
=============================

Goal: Practice using Python's function argument types in the cinema ticketing domain.

Instructions:
    1. Complete the four function stubs where marked with HINT comments.
    2. Run the file to test your functions: poetry run python exercises/exercise_function_signatures.py
    3. Compare with exercise_function_signatures_solution.py if you get stuck.

Tasks:
    A) format_ticket:
        - Parameters: movie, seat, price (all must be passed by name)
        - Hint: Callers shouldn't need to remember the argument order

    B) calculate_group_total:
        - Accept any number of ticket prices
        - Return the sum with a 10% group discount applied
        - Hint: Variable number of positional arguments

    C) create_event:
        - Required parameter: title (can be positional or keyword)
        - Accept any additional keyword details (e.g., venue='Theater 1', time='7pm')
        - Return a dict with all event details
        - Hint: Flexible keyword arguments

    D) process_booking:
        - booking_id must be positional-only
        - customer_email must be keyword-only
        - Accept any number of ticket_ids after booking_id
        - Accept any additional keyword metadata after customer_email
        - Return a dict with all booking details
        - Hint: Combine all techniques (/, *, *args, **kwargs)

    E) book_ticket:
        - customer_name can be passed positionally OR by name
        - movie and seat must be keyword-only (use bare * separator)
        - Return a string like: "Alice booked A1 for Inception"
        - Hint: Use a single * to separate positional-or-keyword from keyword-only
"""
# pyre-ignore-all-errors[6,13,15,56]
# pylint: disable=unnecessary-pass,unused-argument,no-self-use,unnecessary-ellipsis
from __future__ import annotations


def format_ticket(movie: str, seat: str, price: float) -> str:
    """Format a ticket string with movie, seat, and price (all args must be named).

    Hint: Callers shouldn't need to remember the argument order.

    Args:
        movie: Movie title.
        seat: Seat identifier.
        price: Ticket price in USD.

    Returns:
        Formatted ticket string.
    """
    # TODO A: Make all parameters keyword-only
    # Hint: Callers shouldn't be able to pass these arguments positionally
    return f'Ticket: {movie} | Seat {seat} | ${price:.2f}'


def calculate_group_total(*prices: float) -> float:
    """Calculate total price for a group of tickets with 10% discount.

    Hint: Variable number of positional arguments.

    Args:
        *prices: Variable number of ticket prices.

    Returns:
        Total price with 10% group discount applied.
    """
    # TODO B: Calculate discounted group total
    # Hint: Sum all the prices, then apply the group discount
    return 0.0


def create_event(title: str, **details: str | int) -> dict:
    """Create an event with title and flexible keyword details.

    Hint: Flexible keyword arguments for additional details.

    Args:
        title: Event title (required).
        **details: Additional event details (e.g., venue, time, duration).

    Returns:
        Event details dict including title and all additional details.
    """
    # TODO C: Return all event details
    # Hint: The returned dict should include the title AND all the extra keyword details
    return {'title': title}


def process_booking(booking_id: int, *ticket_ids: str, customer_email: str, **metadata: str | int) -> dict:
    """Process a booking with combined argument types.

    Hint: Combine positional-only, variable positional, keyword-only, and variable keyword args.

    Args:
        booking_id: Booking ID (positional-only).
        *ticket_ids: Variable number of ticket IDs.
        customer_email: Customer email (keyword-only).
        **metadata: Additional booking metadata.

    Returns:
        Booking details dict.
    """
    # TODO D: Make booking_id positional-only and return all booking details
    # Hint: booking_id should not be passable by name; return all booking details including ticket IDs and metadata
    return {
        'booking_id': booking_id,
        'customer_email': customer_email,
    }


def book_ticket(customer_name: str, movie: str, seat: str) -> str:
    """Book a ticket where movie and seat must be keyword-only.

    Hint: Use a bare * to make movie and seat keyword-only while allowing
    customer_name to be passed either way.

    Args:
        customer_name: Customer name (positional or keyword).
        movie: Movie title (keyword-only).
        seat: Seat identifier (keyword-only).

    Returns:
        Booking confirmation string.
    """
    # TODO E: Make movie and seat keyword-only
    # Hint: Add a bare * between customer_name and movie in the signature
    return f'{customer_name} booked {seat} for {movie}'


def main() -> None:
    print('=== Task A: format_ticket ===')
    ticket = format_ticket(movie='Inception', seat='A12', price=15.0)
    print(f'Formatted: {ticket}')
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
    booking2 = process_booking(102, 'TKT-001', 'TKT-002', customer_email='bob@example.com', payment='credit')
    print(f'Booking 1: {booking1}')
    print(f'Booking 2: {booking2}')
    print()

    print('=== Task E: book_ticket ===')
    # Both of these should work:
    result1 = book_ticket('Alice', movie='Inception', seat='A1')
    result2 = book_ticket(customer_name='Bob', movie='The Matrix', seat='B3')
    print(f'Result 1: {result1}')
    print(f'Result 2: {result2}')
    # This should fail (movie/seat are keyword-only):
    # book_ticket('Alice', 'Inception', 'A1')  # TypeError!


if __name__ == '__main__':
    main()
