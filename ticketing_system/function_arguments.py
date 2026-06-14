# pylint: disable=invalid-name,missing-kwoa,positional-only-arguments-expected,too-many-function-args,pointless-string-statement
# pylint: disable=unused-variable
# pylint: disable=dangerous-default-value
"""
Function Arguments Teaching File
=================================

Demonstrates Python's function argument types using the cinema ticketing domain.

Topics covered:
    1. Keyword-only arguments (*)
    2. Positional-only arguments (/)
    3. Variable positional arguments (*args)
    4. Variable keyword arguments (**kwargs)
    5. Combined usage
    6. Real-world patterns
"""

# --- 1. Keyword-only arguments ---
# WHAT: The * separator forces all parameters AFTER it to be passed by name.
# WHEN: Use when argument order is hard to remember or when you want to prevent
#       positional mistakes. Makes function calls more readable and refactor-safe.


def create_booking(*, customer: str, movie: str, tickets: int) -> dict:
    """Create a movie booking (all arguments must be passed by name).

    Args:
        customer: Customer email.
        movie: Movie title.
        tickets: Number of tickets to reserve.

    Returns:
        Booking details dict.
    """
    return {'customer': customer, 'movie': movie, 'tickets': tickets}


# --- 2. Positional-only arguments ---
# WHAT: The / separator forces all parameters BEFORE it to be passed positionally.
# WHEN: Use for parameters where the name doesn't add clarity (e.g., mathematical
#       functions) or when you want freedom to rename parameters without breaking callers.


def calculate_price(base_price: float, /, discount: float = 0.0) -> float:
    """Calculate final ticket price.

    Args:
        base_price: Original price (positional-only).
        discount: Discount amount in dollars (can be positional or keyword).

    Returns:
        Final price after discount.
    """
    return base_price - discount


# --- 3. Variable positional arguments (*args) ---
# WHAT: Accept any number of positional arguments (captured as a tuple).
# WHEN: Use when the number of arguments is unknown or varies (e.g., aggregating,
#       logging, formatting).


def print_receipt(*ticket_ids: str) -> None:
    """Print a receipt for the given ticket IDs.

    Args:
        *ticket_ids: Variable number of ticket ID strings.
    """
    print(f'Receipt for {len(ticket_ids)} ticket(s):')
    for ticket_id in ticket_ids:
        print(f'  - {ticket_id}')


# --- 4. Variable keyword arguments (**kwargs) ---
# WHAT: Accept any number of keyword arguments (captured as a dict).
# WHEN: Use for flexible configuration, forwarding options to other functions,
#       or when the set of valid parameters is open-ended.


def configure_screening(**options: str | int | bool) -> dict:
    """Configure a movie screening with flexible options.

    Args:
        **options: Configuration key-value pairs (e.g., subtitles=True, volume=8).

    Returns:
        Configuration dict.
    """
    config = {'screening_type': options.get('screening_type', 'standard')}
    config.update(options)
    return config


# --- 5. Combined: All argument types in one function ---
# WHAT: You can combine positional-only, regular, *args, keyword-only, and **kwargs.
# ORDER: def func(pos_only, /, regular, *args, kw_only, **kwargs)


def create_event(event_id: int, /, title: str, *tags: str, priority: str = 'normal', **metadata: str | int) -> dict:
    """Create an event with all parameter types.

    Args:
        event_id: Event ID (positional-only).
        title: Event title (can be positional or keyword).
        *tags: Variable number of tag strings.
        priority: Event priority (keyword-only with default).
        **metadata: Additional metadata key-value pairs.

    Returns:
        Event details dict.
    """
    return {
        'event_id': event_id,
        'title': title,
        'tags': list(tags),
        'priority': priority,
        'metadata': metadata,
    }


# --- 6. Real-world pattern: Forcing named arguments prevents mistakes ---
# WHAT: In practice, keyword-only args prevent subtle bugs when refactoring
#       or when argument order is non-obvious.


def book_premium_ticket(*, customer_email: str, movie_title: str, seat_number: str, price: float, payment_method: str) -> dict:
    """Book a premium ticket (all args must be named to prevent mistakes).

    Args:
        customer_email: Customer's email address.
        movie_title: Movie title.
        seat_number: Seat identifier (e.g., 'A12').
        price: Ticket price in USD.
        payment_method: Payment method (e.g., 'credit_card').

    Returns:
        Booking confirmation dict.
    """
    return {
        'customer': customer_email,
        'movie': movie_title,
        'seat': seat_number,
        'price': price,
        'payment': payment_method,
        'status': 'confirmed',
    }


def main() -> None:
    print('=== 1. Keyword-only arguments ===')
    booking = create_booking(customer='alice@example.com', movie='Inception', tickets=2)
    print(f'Valid call: {booking}')
    try:
        # This will fail: arguments must be passed by name
        invalid_booking = create_booking('alice@example.com', 'Inception', 2)  # type: ignore
    except TypeError as e:
        print(f'Invalid call (positional): {e}\n')

    print('=== 2. Positional-only arguments ===')
    price1 = calculate_price(15.0)
    price2 = calculate_price(15.0, 2.5)
    price3 = calculate_price(15.0, discount=2.5)
    print(f'Valid calls: {price1}, {price2}, {price3}')
    try:
        # This will fail: base_price cannot be passed by name
        invalid_price = calculate_price(base_price=15.0)  # type: ignore
    except TypeError as e:
        print(f'Invalid call (keyword for positional-only): {e}\n')

    print('=== 3. Variable positional arguments (*args) ===')
    print_receipt('TKT-001')
    print_receipt('TKT-002', 'TKT-003', 'TKT-004')
    print()

    print('=== 4. Variable keyword arguments (**kwargs) ===')
    config1 = configure_screening(subtitles=True, volume=8, screening_type='imax')
    config2 = configure_screening(language='en', is_3d=False)
    print(f'Config 1: {config1}')
    print(f'Config 2: {config2}\n')

    print('=== 5. Combined usage ===')
    event = create_event(42, 'Star Wars Marathon', 'sci-fi', 'marathon', 'classic', priority='high', duration=720, venue='Theater 3')
    print(f'Event: {event}\n')

    print('=== 6. Real-world pattern: Preventing mistakes ===')
    ticket = book_premium_ticket(customer_email='bob@example.com', movie_title='The Matrix', seat_number='C15', price=25.0,
                                 payment_method='credit_card')
    print(f'Premium ticket: {ticket}')
    try:
        # This will fail: all args must be named
        bad_ticket = book_premium_ticket('bob@example.com', 'The Matrix', 'C15', 25.0, 'credit_card')  # type: ignore[reportCallIssue]
    except TypeError as e:
        print(f'Invalid call (positional): {e}')


if __name__ == '__main__':
    main()
