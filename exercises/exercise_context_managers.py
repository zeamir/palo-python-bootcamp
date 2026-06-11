from __future__ import annotations

# pyre-ignore-all-errors[6,13,15,56]

from contextlib import contextmanager
from typing import Generator

"""
Exercise: Context Managers

In this exercise, you'll implement two types of context managers commonly used
in production code: a class-based context manager for resource locking and
a function-based context manager for timing operations.

Reference: ticketing_system/context_managers.py
"""


# ============================================================================
# Task A: Class-based Context Manager
# ============================================================================

class SeatLockContext:
    """Context manager that acquires and releases a seat lock.

    Simulates locking a seat during a booking operation. The lock should be
    released properly even if an error occurs.

    Usage:
        with SeatLockContext('A5') as lock:
            # perform booking for seat A5
            ...
    """

    def __init__(self, seat_id: str) -> None:
        """Initialize the lock context for a specific seat.

        Args:
            seat_id: The seat identifier to lock (e.g., 'A5').
        """
        self.seat_id = seat_id
        self.locked = False

    def __enter__(self) -> SeatLockContext:
        """Acquire the seat lock when entering the context.

        Hint: Signal that the seat is now reserved and make the lock
        usable via the 'as' clause.

        Returns:
            self — the active lock context.
        """
        # Hint: Mark the seat as locked and announce it
        return self

    def __exit__(
        self,
        exc_type: type | None,
        exc_val: Exception | None,
        exc_tb: object,
    ) -> bool:
        """Release the seat lock when exiting the context.

        Hint: The seat must always be freed — whether the block
        succeeded or raised an exception. Distinguish the two cases
        in your output.

        Returns:
            False — let any exception propagate to the caller.
        """
        # Hint: Clean up regardless of success or failure
        return False


# ============================================================================
# Task B: Function-based Context Manager
# ============================================================================

@contextmanager
def timed_operation(name: str) -> Generator[None, None, None]:
    """Context manager that measures and reports the duration of an operation.

    Hint: Measure how long the block takes and report it after the block ends.

    Args:
        name: A descriptive name for the operation being timed.

    Yields:
        None.
    """
    # TODO: Implement this
    yield


# ============================================================================
# Demo / Test Code
# ============================================================================

def main() -> None:
    """Demonstrate the context managers."""
    print('=== Testing SeatLockContext (success case) ===')
    with SeatLockContext('A5') as lock:
        print(f'  Inside context, locked: {lock.locked}')
        print('  Booking seat A5...')
    print(f'  After context, locked: {lock.locked}\n')

    print('=== Testing SeatLockContext (error case) ===')
    try:
        with SeatLockContext('B7') as lock:
            print(f'  Inside context, locked: {lock.locked}')
            print('  Attempting to book seat B7...')
            raise ValueError('Payment failed')
    except ValueError:
        print(f'  After context (error), locked: {lock.locked}\n')

    print('=== Testing timed_operation ===')
    with timed_operation('database_query'):
        print('  Running query...')
        # Simulate some work
        import time
        time.sleep(0.1)
    print()

    print('=== Testing timed_operation (nested) ===')
    with timed_operation('full_booking'):
        print('  Step 1: validate request')
        with timed_operation('payment_processing'):
            print('    Processing payment...')
            import time
            time.sleep(0.05)
        print('  Step 2: save ticket')


if __name__ == '__main__':
    main()
