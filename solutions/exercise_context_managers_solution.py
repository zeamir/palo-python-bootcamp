"""
Solution: Context Managers

This solution demonstrates:
1. Class-based context manager with __enter__ and __exit__
2. Function-based context manager using @contextmanager decorator
"""
from __future__ import annotations

import time
from contextlib import contextmanager
from typing import Generator

# ============================================================================
# Task A: Class-based Context Manager
# ============================================================================


class SeatLockContext:
    """Context manager that acquires and releases a seat lock."""

    def __init__(self, seat_id: str) -> None:
        """Initialize the lock context for a specific seat.

        Args:
            seat_id: The seat identifier to lock (e.g., 'A5').
        """
        self.seat_id = seat_id
        self.locked = False

    def __enter__(self) -> SeatLockContext:
        """Acquire the seat lock when entering the context.

        Returns:
            Self, so the context manager can be used with 'as'.
        """
        print(f'[LOCK] Locking seat {self.seat_id}')
        self.locked = True
        return self

    def __exit__(
        self,
        exc_type: type | None,
        exc_val: Exception | None,
        exc_tb: object,
    ) -> bool:
        """Release the seat lock when exiting the context.

        Args:
            exc_type: Exception type if an error occurred, None otherwise.
            exc_val: Exception instance if an error occurred, None otherwise.
            exc_tb: Exception traceback.

        Returns:
            False to re-raise any exception that occurred.
        """
        if exc_type is None:
            print(f'[LOCK] Released seat {self.seat_id}')
        else:
            print(f'[LOCK] Releasing seat {self.seat_id} after error: {exc_val}')

        self.locked = False
        return False


# ============================================================================
# Task B: Function-based Context Manager
# ============================================================================


@contextmanager
def timed_operation(name: str) -> Generator[None, None, None]:
    """Context manager that measures and reports the duration of an operation.

    Args:
        name: A descriptive name for the operation being timed.

    Yields:
        None (the context manager doesn't provide a value to 'as').
    """
    start_time = time.time()
    try:
        yield
    finally:
        elapsed = time.time() - start_time
        print(f'[TIMER] {name} completed in {elapsed:.3f}s')


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
        time.sleep(0.1)
    print()

    print('=== Testing timed_operation (nested) ===')
    with timed_operation('full_booking'):
        print('  Step 1: validate request')
        with timed_operation('payment_processing'):
            print('    Processing payment...')
            time.sleep(0.05)
        print('  Step 2: save ticket')


if __name__ == '__main__':
    main()
