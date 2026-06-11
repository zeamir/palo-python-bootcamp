from ticketing_system.context_managers import TransactionContext
from ticketing_system.models.booking_request import BookingRequest
from ticketing_system.models.customer import Customer
from ticketing_system.models.ticket import Ticket
from ticketing_system.services.database_service import DatabaseService
from ticketing_system.services.payment_service import PaymentService


class BookingService:
    """Orchestrates the cinema ticket booking flow.

    Coordinates DatabaseService and PaymentService to complete a booking.
    Uses constructor injection so dependencies can be mocked in tests.
    """

    def __init__(self, db: DatabaseService, payment: PaymentService) -> None:
        self._db = db
        self._payment = payment

    def book_ticket(self, request: BookingRequest) -> Ticket:
        """Book a cinema ticket for a customer.

        Args:
            request: The booking details.

        Returns:
            The purchased Ticket.

        Raises:
            ValueError: If the movie is not found or the customer is underage.
            RuntimeError: If the payment fails.
        """
        with TransactionContext('book_ticket', movie=request.movie_name, customer=request.customer_email):
            movie = self._db.get_movie_by_name(request.movie_name)
            if movie is None:
                raise ValueError(f'Movie not found: {request.movie_name!r}')

            customer = Customer(
                name=request.customer_name,
                email=request.customer_email,
                age=request.customer_age,
            )

            total_price = 15.00 * request.num_tickets

            payment_ok = self._payment.process_payment(customer.name, total_price)
            if not payment_ok:
                raise RuntimeError(f'Payment failed for customer {customer.email!r}')

            ticket = Ticket(
                movie=movie,
                customer=customer,
                price=total_price,
                seat_number=request.seat_number,
            )

            self._db.save_ticket(ticket)
            return ticket
