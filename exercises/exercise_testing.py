"""
Exercise: Unit Testing with Mockito

In this exercise, you'll write unit tests for a CancellationService using
the mockito library for mocking dependencies. This demonstrates how to test
business logic in isolation without depending on real database or payment
services.

Key Testing Concepts:
- PREPARE: Set up test data and mock objects
- MOCK: Define expectations for how mocks should be called
- ACT: Call the method being tested
- ASSERT: Verify the result

Mockito Pattern:
- Always use: expect(mock_obj, times=N).method(args).thenReturn(value)
- NEVER use unittest.mock (patch, Mock, MagicMock)
- Always specify times parameter for every expectation
"""
# pyre-ignore-all-errors[6,13,15,56]
# pylint: disable=unnecessary-pass,unused-argument,no-self-use,unnecessary-ellipsis
from __future__ import annotations

import unittest

# ============================================================================
# Code Under Test (provided for you)
# ============================================================================


class DatabaseService:
    """Simple database service interface (stub for testing)."""

    def get_ticket(self, ticket_id: str) -> dict | None:
        """Retrieve a ticket by ID.

        Args:
            ticket_id: The ticket identifier.

        Returns:
            Ticket dict if found, None otherwise.
        """
        ...

    def delete_ticket(self, ticket_id: str) -> None:
        """Delete a ticket from the database.

        Args:
            ticket_id: The ticket identifier.
        """
        ...


class PaymentService:
    """Simple payment service interface (stub for testing)."""

    def process_refund(self, email: str, amount: float) -> bool:
        """Process a refund to a customer.

        Args:
            email: Customer's email address.
            amount: Refund amount.

        Returns:
            True if refund succeeded, False otherwise.
        """
        ...


class CancellationService:
    """Service for cancelling tickets and processing refunds."""

    def __init__(self, db: DatabaseService, payment: PaymentService) -> None:
        """Initialize the cancellation service.

        Args:
            db: Database service for ticket operations.
            payment: Payment service for refund processing.
        """
        self._db = db
        self._payment = payment

    def cancel_ticket(self, ticket_id: str, customer_email: str) -> str:
        """Cancel a ticket and process a refund.

        Args:
            ticket_id: The ticket to cancel.
            customer_email: The customer's email for refund processing.

        Returns:
            Confirmation message.

        Raises:
            ValueError: If the ticket is not found.
            RuntimeError: If the refund fails.
        """
        # Step 1: Look up the ticket
        ticket = self._db.get_ticket(ticket_id)
        if ticket is None:
            raise ValueError(f'Ticket not found: {ticket_id!r}')

        # Step 2: Process the refund
        refund_ok = self._payment.process_refund(customer_email, ticket['price'])
        if not refund_ok:
            raise RuntimeError('Refund failed')

        # Step 3: Delete the ticket from the database
        self._db.delete_ticket(ticket_id)

        return f'Cancelled ticket {ticket_id}'


# ============================================================================
# Your Tests Go Here
# ============================================================================


class CancellationServiceTest(unittest.TestCase):
    """Tests for CancellationService."""

    def setUp(self) -> None:
        """Set up test fixtures before each test method.

        TODO: Implement this method.
        - Create mock objects for DatabaseService and PaymentService
        - Create a CancellationService instance with the mocks
        - Store them as instance variables (self._db, self._payment, self._service)

        Hint: Use mock() from mockito to create mock objects.
        """
        # TODO: Set up mocks and service
        pass

    def tearDown(self) -> None:
        """Clean up after each test method.

        TODO: Implement this method.
        - Call unstub() to reset all mockito expectations

        Hint: This ensures that mock expectations don't leak between tests.
        tearDown is called after every test method, whether it passes or fails.
        """
        # TODO: Clean up mocks
        pass

    def test_successful_cancellation(self) -> None:
        """Test that a valid cancellation completes successfully.

        TODO: Implement this test.
        PREPARE:
        - Create a sample ticket dict with keys: 'ticket_id', 'price', 'seat'
          Example: {'ticket_id': 'T123', 'price': 25.0, 'seat': 'A5'}

        MOCK:
        - Expect self._db.get_ticket to be called once with 'T123'
          and return the ticket dict
        - Expect self._payment.process_refund to be called once with
          the customer email and ticket price, and return True
        - Expect self._db.delete_ticket to be called once with 'T123'

        ACT:
        - Call self._service.cancel_ticket('T123', 'customer@example.com')

        ASSERT:
        - Verify the result contains 'Cancelled ticket T123'

        Hint: Use the pattern expect(mock_obj, times=1).method(args).thenReturn(value)
        For methods with no return value (like delete_ticket), use .thenReturn(None)
        or just don't chain thenReturn at all.
        """
        # TODO: Implement this test
        pass

    def test_ticket_not_found(self) -> None:
        """Test that a ValueError is raised when the ticket doesn't exist.

        TODO: Implement this test.
        PREPARE:
        - No additional preparation needed

        MOCK:
        - Expect self._db.get_ticket to be called once with 'INVALID'
          and return None (ticket not found)

        ACT / ASSERT:
        - Use self.assertRaises(ValueError) to verify that calling
          self._service.cancel_ticket('INVALID', 'customer@example.com')
          raises a ValueError
        - Check that the exception message contains 'Ticket not found'

        Hint: Use the pattern:
        with self.assertRaises(ValueError) as ctx:
            self._service.cancel_ticket(...)
        assert 'Ticket not found' in str(ctx.exception)
        """
        # TODO: Implement this test
        pass

    def test_refund_fails(self) -> None:
        """Test that a RuntimeError is raised when the refund fails.

        TODO: Implement this test.
        PREPARE:
        - Create a sample ticket dict

        MOCK:
        - Expect self._db.get_ticket to be called once and return the ticket
        - Expect self._payment.process_refund to be called once and return False

        ACT / ASSERT:
        - Use self.assertRaises(RuntimeError) to verify that the method
          raises a RuntimeError
        - Check that the exception message contains 'Refund failed'
        - Note: delete_ticket should NOT be called when refund fails

        Hint: When a test expects an exception to be raised, the code after
        the failing operation won't execute. So delete_ticket won't be called
        and doesn't need a mock expectation.
        """
        # TODO: Implement this test
        pass


# ============================================================================
# Run Tests
# ============================================================================

if __name__ == '__main__':
    unittest.main()
