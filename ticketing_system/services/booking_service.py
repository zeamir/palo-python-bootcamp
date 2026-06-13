from ticketing_system.exceptions import AgeRequirementError, MovieNotFoundError, PaymentFailedError
from ticketing_system.models.booking_request import BookingRequest
from ticketing_system.models.customer import Customer
from ticketing_system.models.ticket import Ticket
from ticketing_system.services.database_service import _DatabaseService, database_service
from ticketing_system.services.movies_service import _MoviesService, movies_service
from ticketing_system.services.payment_service import _PaymentService, payment_service


class _BookingService:
    """Orchestrates the cinema ticket booking flow.

    Coordinates _MoviesService, _DatabaseService, and _PaymentService to complete a booking.
    Access via the module-level `booking_service` singleton. Use `set_movies`, `set_db`, and
    `set_payment` to inject dependencies (e.g. in tests).
    """

    def __init__(self) -> None:
        self._movies_instance: _MoviesService | None = None
        self._db_instance: _DatabaseService | None = None
        self._payment_instance: _PaymentService | None = None

    @property
    def _movies(self) -> _MoviesService:
        if self._movies_instance is None:
            self._movies_instance = movies_service
        return self._movies_instance

    @property
    def _db(self) -> _DatabaseService:
        if self._db_instance is None:
            self._db_instance = database_service
        return self._db_instance

    @property
    def _payment(self) -> _PaymentService:
        if self._payment_instance is None:
            self._payment_instance = payment_service
        return self._payment_instance

    def set_movies(self, movies: _MoviesService) -> None:
        """Inject a _MoviesService instance (useful for testing).

        Args:
            movies: The _MoviesService to use.
        """
        self._movies_instance = movies

    def set_db(self, db: _DatabaseService) -> None:
        """Inject a _DatabaseService instance (useful for testing).

        Args:
            db: The _DatabaseService to use.
        """
        self._db_instance = db

    def set_payment(self, payment: _PaymentService) -> None:
        """Inject a _PaymentService instance (useful for testing).

        Args:
            payment: The _PaymentService to use.
        """
        self._payment_instance = payment

    def book_ticket(self, request: BookingRequest) -> Ticket:
        """Book a cinema ticket for a customer.

        Args:
            request: The booking details.

        Returns:
            The purchased Ticket.

        Raises:
            MovieNotFoundError: If the requested movie does not exist.
            AgeRequirementError: If the customer is underage for the movie.
            PaymentFailedError: If the payment processor declines the transaction.
        """
        movie = self._movies.get_movie_by_name(request.movie_name)
        if movie is None:
            raise MovieNotFoundError(f'Movie not found: {request.movie_name!r}')

        if request.customer_age < movie.min_age:
            raise AgeRequirementError(f'Customer age {request.customer_age} does not meet the minimum age '
                                      f'requirement of {movie.min_age} for "{movie.name}"')

        customer = Customer(
            name=request.customer_name,
            email=request.customer_email,
            age=request.customer_age,
        )

        total_price = 15.00 * request.num_tickets

        payment_ok = self._payment.process_payment(customer.name, total_price)
        if not payment_ok:
            raise PaymentFailedError(f'Payment failed for customer {customer.email!r}')

        ticket = Ticket(
            movie=movie,
            customer=customer,
            price=total_price,
            seat_number=request.seat_number,
        )

        self._db.save_ticket(ticket)
        return ticket


booking_service: _BookingService = _BookingService()
