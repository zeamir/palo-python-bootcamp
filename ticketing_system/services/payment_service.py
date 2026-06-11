# pylint: disable=no-self-use


class PaymentService:
    """Handles payment processing for cinema tickets.

    This is a demonstration implementation that prints actions rather than
    integrating with a real payment provider.
    """

    def process_payment(self, customer_name: str, amount: float) -> bool:
        """Process a payment for a customer.

        Args:
            customer_name: The name of the paying customer.
            amount: The amount to charge in USD.

        Returns:
            True if payment succeeded.
        """
        print(f'[PaymentService] Processing payment of ${amount:.2f} for {customer_name}')
        return True

    def refund(self, ticket_id: str, amount: float) -> bool:
        """Issue a refund for a ticket.

        Args:
            ticket_id: The ID of the ticket to refund.
            amount: The refund amount in USD.

        Returns:
            True if refund succeeded.
        """
        print(f'[PaymentService] Issuing refund of ${amount:.2f} for ticket {ticket_id}')
        return True
