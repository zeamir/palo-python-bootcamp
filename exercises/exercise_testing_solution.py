from __future__ import annotations

import unittest

from mockito import expect, mock, unstub

"""
Solution: Unit Testing with Mockito

This solution demonstrates proper unit testing with mockito:
- Mocking external dependencies
- Setting up expectations with times parameter
- Testing both success and failure paths
- Using PREPARE/MOCK/ACT/ASSERT structure
"""


# ============================================================================
# Code Under Test
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
# Tests
# ============================================================================

class CancellationServiceTest(unittest.TestCase):
    """Tests for CancellationService."""

    def setUp(self) -> None:
        """Set up test fixtures before each test method."""
        self._db = mock(DatabaseService)
        self._payment = mock(PaymentService)
        self._service = CancellationService(self._db, self._payment)

    def tearDown(self) -> None:
        """Clean up after each test method."""
        unstub()

    def test_successful_cancellation(self) -> None:
        """Test that a valid cancellation completes successfully."""
        # PREPARE
        ticket = {'ticket_id': 'T123', 'price': 25.0, 'seat': 'A5'}

        # MOCK
        expect(self._db, times=1).get_ticket('T123').thenReturn(ticket)
        expect(self._payment, times=1).process_refund('customer@example.com', 25.0).thenReturn(True)
        expect(self._db, times=1).delete_ticket('T123').thenReturn(None)

        # ACT
        result = self._service.cancel_ticket('T123', 'customer@example.com')

        # ASSERT
        assert 'Cancelled ticket T123' in result

    def test_ticket_not_found(self) -> None:
        """Test that a ValueError is raised when the ticket doesn't exist."""
        # PREPARE
        # (no additional preparation needed)

        # MOCK
        expect(self._db, times=1).get_ticket('INVALID').thenReturn(None)

        # ACT / ASSERT
        with self.assertRaises(ValueError) as ctx:
            self._service.cancel_ticket('INVALID', 'customer@example.com')

        assert 'Ticket not found' in str(ctx.exception)

    def test_refund_fails(self) -> None:
        """Test that a RuntimeError is raised when the refund fails."""
        # PREPARE
        ticket = {'ticket_id': 'T456', 'price': 30.0, 'seat': 'B2'}

        # MOCK
        expect(self._db, times=1).get_ticket('T456').thenReturn(ticket)
        expect(self._payment, times=1).process_refund('customer@example.com', 30.0).thenReturn(False)

        # ACT / ASSERT
        with self.assertRaises(RuntimeError) as ctx:
            self._service.cancel_ticket('T456', 'customer@example.com')

        assert 'Refund failed' in str(ctx.exception)


# ============================================================================
# Run Tests
# ============================================================================

if __name__ == '__main__':
    unittest.main()
