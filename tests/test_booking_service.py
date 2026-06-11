import unittest

from mockito import expect, mock, unstub

from ticketing_system.models.booking_request import BookingRequest
from ticketing_system.models.movie import Genre, Movie
from ticketing_system.services.booking_service import BookingService
from ticketing_system.services.database_service import DatabaseService
from ticketing_system.services.payment_service import PaymentService


def _make_movie(min_age: int = 0) -> Movie:
    return Movie(name='Inception', genre=Genre.SCI_FI, duration_minutes=148, rating=8.8, release_year=2010, min_age=min_age)


def _make_request(**overrides) -> BookingRequest:
    defaults = {
        'customer_name': 'Jane Doe',
        'customer_email': 'jane@example.com',
        'customer_age': 30,
        'movie_name': 'Inception',
        'num_tickets': 2,
        'seat_number': 'B7',
    }
    return BookingRequest(**{**defaults, **overrides})


class BookingServiceTest(unittest.TestCase):

    def setUp(self) -> None:
        self._db = mock(DatabaseService)
        self._payment = mock(PaymentService)
        self._service = BookingService(self._db, self._payment)

    def tearDown(self) -> None:
        unstub()

    def test_successful_booking(self) -> None:
        """Test that a valid booking request creates and persists a ticket."""
        # PREPARE
        request = _make_request()
        movie = _make_movie()

        # MOCK
        expect(self._db, times=1).get_movie_by_name('Inception').thenReturn(movie)
        expect(self._payment, times=1).process_payment('Jane Doe', 30.0).thenReturn(True)
        expect(self._db, times=1).save_ticket(...).thenReturn(None)

        # ACT
        ticket = self._service.book_ticket(request)

        # ASSERT
        assert ticket.movie.name == 'Inception'
        assert ticket.customer.email == 'jane@example.com'
        assert ticket.price == 30.0

    def test_booking_movie_not_found(self) -> None:
        """Test that a ValueError is raised when the requested movie does not exist."""
        # PREPARE
        request = _make_request(movie_name='Unknown Movie')

        # MOCK
        expect(self._db, times=1).get_movie_by_name('Unknown Movie').thenReturn(None)

        # ACT / ASSERT
        with self.assertRaises(ValueError) as ctx:
            self._service.book_ticket(request)

        assert 'Movie not found' in str(ctx.exception)

    def test_booking_payment_fails(self) -> None:
        """Test that a RuntimeError is raised when the payment service fails."""
        # PREPARE
        request = _make_request()
        movie = _make_movie()

        # MOCK
        expect(self._db, times=1).get_movie_by_name('Inception').thenReturn(movie)
        expect(self._payment, times=1).process_payment('Jane Doe', 30.0).thenReturn(False)

        # ACT / ASSERT
        with self.assertRaises(RuntimeError) as ctx:
            self._service.book_ticket(request)

        assert 'Payment failed' in str(ctx.exception)

    def test_booking_underage_customer(self) -> None:
        """Test that a ValueError is raised when the customer does not meet the age requirement."""
        # PREPARE
        request = _make_request(customer_age=10)
        movie = _make_movie(min_age=18)

        # MOCK
        expect(self._db, times=1).get_movie_by_name('Inception').thenReturn(movie)
        expect(self._payment, times=1).process_payment('Jane Doe', 30.0).thenReturn(True)

        # ACT / ASSERT
        with self.assertRaises(ValueError) as ctx:
            self._service.book_ticket(request)

        assert 'minimum age' in str(ctx.exception)


if __name__ == '__main__':
    unittest.main()
