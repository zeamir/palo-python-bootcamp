from __future__ import annotations

from functools import wraps
from typing import Any, Callable

"""
Solution: Decorators

This solution demonstrates:
1. Simple decorator using @wraps to preserve function metadata
2. Parameterized decorator (decorator factory) for role-based access control
"""


# ============================================================================
# Task A: Simple Decorator
# ============================================================================

def log_call(func: Callable) -> Callable:
    """Decorator that logs function calls with their arguments.

    Args:
        func: The function to decorate.

    Returns:
        A wrapper function that logs and then calls the original function.
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        """Log the call and invoke the original function."""
        print(f'[CALL] {func.__name__}({args}, {kwargs})')
        return func(*args, **kwargs)

    return wrapper


# ============================================================================
# Task B: Parameterized Decorator
# ============================================================================

def require_role(role: str) -> Callable:
    """Decorator factory that enforces role-based access control.

    Args:
        role: The role required to execute the decorated function.

    Returns:
        A decorator function that enforces the role requirement.
    """

    def decorator(func: Callable) -> Callable:
        """Decorator that wraps the target function with role checking.

        Args:
            func: The function to decorate.

        Returns:
            A wrapper function that enforces role requirements.
        """

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """Check user role before calling the function.

            Raises:
                PermissionError: If user_role is missing or doesn't match.
            """
            if 'user_role' not in kwargs:
                raise PermissionError('user_role parameter is required')

            user_role = kwargs['user_role']
            if user_role != role:
                raise PermissionError(f'Requires role: {role}')

            return func(*args, **kwargs)

        return wrapper

    return decorator


# ============================================================================
# Demo / Test Code
# ============================================================================

@log_call
def calculate_ticket_price(base_price: float, discount: float = 0.0) -> float:
    """Calculate final ticket price with discount.

    Args:
        base_price: The base ticket price.
        discount: Discount as a decimal (0.0 to 1.0).

    Returns:
        The final price after discount.
    """
    return base_price * (1 - discount)


@require_role('admin')
def delete_booking(booking_id: str, *, user_role: str) -> str:
    """Delete a booking (admin only).

    Args:
        booking_id: The booking to delete.
        user_role: The role of the user making the request.

    Returns:
        Confirmation message.
    """
    return f'Deleted booking {booking_id}'


@require_role('manager')
def refund_ticket(ticket_id: str, amount: float, *, user_role: str) -> str:
    """Process a refund (manager only).

    Args:
        ticket_id: The ticket to refund.
        amount: The refund amount.
        user_role: The role of the user making the request.

    Returns:
        Confirmation message.
    """
    return f'Refunded ${amount:.2f} for ticket {ticket_id}'


def main() -> None:
    """Demonstrate the decorators."""
    print('=== Testing @log_call ===')
    price1 = calculate_ticket_price(15.0)
    print(f'Result: ${price1:.2f}\n')

    price2 = calculate_ticket_price(15.0, discount=0.2)
    print(f'Result: ${price2:.2f}\n')

    print('=== Testing @require_role (success) ===')
    result = delete_booking('booking-123', user_role='admin')
    print(f'Result: {result}\n')

    print('=== Testing @require_role (wrong role) ===')
    try:
        delete_booking('booking-456', user_role='user')
    except PermissionError as e:
        print(f'Error: {e}\n')

    print('=== Testing @require_role (missing role) ===')
    try:
        refund_ticket('ticket-789', 15.0)  # type: ignore[call-arg]
    except PermissionError as e:
        print(f'Error: {e}\n')

    print('=== Testing multiple decorators ===')

    @log_call
    @require_role('admin')
    def critical_operation(action: str, *, user_role: str) -> str:
        """Perform a critical system operation.

        Args:
            action: The action to perform.
            user_role: The role of the user making the request.

        Returns:
            Confirmation message.
        """
        return f'Executed: {action}'

    result = critical_operation('system_reset', user_role='admin')
    print(f'Result: {result}')


if __name__ == '__main__':
    main()
