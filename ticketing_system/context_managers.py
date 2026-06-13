from contextlib import contextmanager
from typing import Generator

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


def main() -> None:
    with logging_context('payment', customer='jane@example.com', amount='15.50') as ctx:
        print(f'  Inside context: {ctx}')
        ctx['ticket_id'] = 'abc-123'


if __name__ == '__main__':
    main()
