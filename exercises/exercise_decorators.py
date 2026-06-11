# pyre-ignore-all-errors[6,13,15,56]
from __future__ import annotations

"""
Exercise: Decorators
=====================

Goal: Implement two decorator patterns used in the cinema ticketing system.

Instructions:
    1. Implement the two decorator stubs below.
    2. Uncomment the demo functions and test calls in main() to verify your work.
    3. Run the file: poetry run python exercises/exercise_decorators.py

See exercise_decorators_solution.py if you get stuck.
Reference: ticketing_system/decorators.py
"""

from functools import wraps
from typing import Callable


# ============================================================================
# Task A: Simple Decorator
# ============================================================================

def log_call(func: Callable) -> Callable:
    """Decorator that observes every call to the wrapped function.

    Hint: Callers should see evidence that the function was called, including
    what arguments were passed — without changing what the function returns.

    Args:
        func: The function to decorate.

    Returns:
        A wrapper function that logs and then calls the original function.
    """
    # Hint: A decorator wraps the original function — preserve its identity
    raise NotImplementedError('Implement log_call')


# ============================================================================
# Task B: Parameterized Decorator
# ============================================================================

def require_role(role: str) -> Callable:
    """Decorator factory that restricts a function to a specific role.

    Hint: The decorated function should only run when the caller has the right
    role. Wrong or missing role should be denied with a clear error.

    Args:
        role: The role required to execute the decorated function.

    Returns:
        A decorator function that enforces the role requirement.
    """
    # Hint: The decorated functions receive user_role as a keyword argument
    raise NotImplementedError('Implement require_role')


# ============================================================================
# Demo / Test Code
# ============================================================================

# Uncomment these functions once you've implemented the decorators:

# @log_call
# def calculate_ticket_price(base_price: float, discount: float = 0.0) -> float:
#     """Calculate final ticket price with discount."""
#     return base_price * (1 - discount)


# @require_role('admin')
# def delete_booking(booking_id: str, *, user_role: str) -> str:
#     """Delete a booking (admin only).
#
#     Args:
#         booking_id: The booking to delete.
#         user_role: The role of the user making the request.
#
#     Returns:
#         Confirmation message.
#     """
#     return f'Deleted booking {booking_id}'


# @require_role('manager')
# def refund_ticket(ticket_id: str, amount: float, *, user_role: str) -> str:
#     """Process a refund (manager only).
#
#     Args:
#         ticket_id: The ticket to refund.
#         amount: The refund amount.
#         user_role: The role of the user making the request.
#
#     Returns:
#         Confirmation message.
#     """
#     return f'Refunded ${amount:.2f} for ticket {ticket_id}'


def main() -> None:
    """Demonstrate the decorators."""
    print('Once you implement the decorators, uncomment the test functions above.')
    print('Then run this script to see them in action.\n')

    # Uncomment these tests after implementing the decorators:

    # print('=== Testing @log_call ===')
    # price1 = calculate_ticket_price(15.0)
    # print(f'Result: ${price1:.2f}\n')
    #
    # price2 = calculate_ticket_price(15.0, discount=0.2)
    # print(f'Result: ${price2:.2f}\n')

    # print('=== Testing @require_role (success) ===')
    # result = delete_booking('booking-123', user_role='admin')
    # print(f'Result: {result}\n')

    # print('=== Testing @require_role (wrong role) ===')
    # try:
    #     delete_booking('booking-456', user_role='user')
    # except PermissionError as e:
    #     print(f'Error: {e}\n')

    # print('=== Testing @require_role (missing role) ===')
    # try:
    #     refund_ticket('ticket-789', 15.0)
    # except PermissionError as e:
    #     print(f'Error: {e}\n')

    # print('=== Testing multiple decorators ===')
    #
    # @log_call
    # @require_role('admin')
    # def critical_operation(action: str, *, user_role: str) -> str:
    #     return f'Executed: {action}'
    #
    # result = critical_operation('system_reset', user_role='admin')
    # print(f'Result: {result}')


if __name__ == '__main__':
    main()
