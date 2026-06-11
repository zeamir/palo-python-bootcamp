from __future__ import annotations

from contextlib import contextmanager
from typing import Generator

# --- Class-based context manager ---
# Use when you need to maintain state across __enter__ and __exit__,
# or when you want the context manager to be reusable as an object.


class TransactionContext:
    """Wraps a booking operation as a transaction.

    Logs the start and end of the transaction and handles rollback on failure.

    Usage:
        with TransactionContext('book_ticket', customer_email='jane@example.com') as tx:
            # perform booking steps
            ...
    """

    def __init__(self, operation: str, **metadata: str) -> None:
        self.operation = operation
        self.metadata = metadata
        self._success = False

    def __enter__(self) -> TransactionContext:
        print(f'[TX] Starting transaction: {self.operation} | metadata={self.metadata}')
        return self

    def __exit__(self, exc_type: type | None, exc_val: Exception | None, exc_tb: object) -> bool:
        if exc_type is None:
            self._success = True
            print(f'[TX] Transaction committed: {self.operation}')
        else:
            print(f'[TX] Transaction rolled back: {self.operation} | reason={exc_val}')
        # Returning False re-raises the exception; True suppresses it.
        return False

    @property
    def succeeded(self) -> bool:
        """Whether the transaction completed without errors."""
        return self._success


# --- Function-based context manager ---
# Use @contextmanager when the setup/teardown logic is simple enough to express
# as a single generator function. Less boilerplate than a full class.


@contextmanager
def logging_context(operation: str, **metadata: str) -> Generator[dict, None, None]:
    """Sets up a structured logging context for the duration of the block.

    Yields a dict that callers can populate with runtime context values.

    Args:
        operation: Name of the operation being performed.
        **metadata: Additional key-value pairs to include in log context.

    Yields:
        A mutable dict representing the active log context.
    """
    context: dict = {'operation': operation, **metadata}
    print(f'[CTX] Enter: {context}')
    try:
        yield context
    except Exception as exc:
        context['error'] = str(exc)
        print(f'[CTX] Error in {operation}: {exc}')
        raise
    finally:
        print(f'[CTX] Exit: {context}')


if __name__ == '__main__':
    # Demonstrate TransactionContext (success)
    with TransactionContext('book_ticket', customer='jane@example.com', movie='Inception') as tx:
        print('  Performing booking steps...')
    print(f'  Transaction succeeded: {tx.succeeded}\n')

    # Demonstrate TransactionContext (failure)
    try:
        with TransactionContext('book_ticket', customer='bob@example.com', movie='Unknown') as tx:
            print('  Performing booking steps...')
            raise ValueError('Movie not found')
    except ValueError:
        print(f'  Transaction succeeded: {tx.succeeded}\n')

    # Demonstrate logging_context
    with logging_context('payment', customer='jane@example.com', amount='15.50') as ctx:
        print(f'  Inside context: {ctx}')
        ctx['ticket_id'] = 'abc-123'
