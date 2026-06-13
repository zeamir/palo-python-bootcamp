import unittest
from datetime import datetime

from mockito import expect, mock, unstub, verifyExpectedInteractions

from ticketing_system.exceptions import AgeRequirementError, MovieNotFoundError
from ticketing_system.models import ticket as ticket_module
from ticketing_system.models.booking_request import BookingRequest
from ticketing_system.models.customer import Customer
from ticketing_system.models.movie import Genre, Movie
from ticketing_system.models.ticket import Ticket
from ticketing_system.services.booking_service import booking_service
from ticketing_system.services.database_service import _DatabaseService
from ticketing_system.services.movies_service import _MoviesService
from ticketing_system.services.payment_service import _PaymentService

_FIXED_TICKET_ID = 'test-ticket-id-123'
_FIXED_PURCHASE_DATE = datetime(2025, 1, 1, 12, 0, 0)


def _make_movie(min_age: int = 0) -> Movie:
    return Movie(name='Inception', genre=Genre.SCI_FI, duration_minutes=148, rating=8.8, release_year=2010, min_age=min_age)


def _make_request(movie_name: str, num_tickets: int, **overrides) -> BookingRequest:
    defaults = {
        'customer_name': 'Jane Doe',
        'customer_email': 'jane@example.com',
        'customer_age': 30,
        'movie_name': movie_name,
        'num_tickets': num_tickets,
        'seat_number': 'B7',
    }
    return BookingRequest(**{**defaults, **overrides})


class BookingServiceTest(unittest.TestCase):

    def setUp(self) -> None:
        self._movies = mock(_MoviesService)
        self._db = mock(_DatabaseService)
        self._payment = mock(_PaymentService)
        booking_service.set_movies(self._movies)
        booking_service.set_db(self._db)
        booking_service.set_payment(self._payment)

    def tearDown(self) -> None:
        unstub()

    def test_successful_booking(self) -> None:
        """
        Given: A valid booking request for an existing movie with no age restriction
        When: book_ticket is called
        Then: A ticket is returned with the correct movie, customer, and price
        """
        # PREPARE
        request = _make_request(movie_name='Inception', num_tickets=2)
        movie = _make_movie()
        expected_ticket = Ticket(
            id=_FIXED_TICKET_ID,
            movie=movie,
            customer=Customer(name='Jane Doe', email='jane@example.com', age=30),
            price=30.0,
            purchase_date=_FIXED_PURCHASE_DATE,
            seat_number='B7',
        )

        # MOCK
        expect(ticket_module, times=1).generate_ticket_id().thenReturn(_FIXED_TICKET_ID)
        expect(ticket_module, times=1).generate_purchase_date().thenReturn(_FIXED_PURCHASE_DATE)
        expect(self._movies, times=1).get_movie_by_name('Inception').thenReturn(movie)
        expect(self._payment, times=1).process_payment('Jane Doe', 30.0).thenReturn(True)
        expect(self._db, times=1).save_ticket(expected_ticket).thenReturn(None)

        # ACT
        ticket = booking_service.book_ticket(request)

        # ASSERT
        assert ticket.movie.name == 'Inception'
        assert ticket.customer.email == 'jane@example.com'
        assert ticket.price == 30.0
        verifyExpectedInteractions()

    def test_booking_movie_not_found(self) -> None:
        """
        Given: A booking request for a movie that does not exist
        When: book_ticket is called
        Then: A ValueError is raised with a message indicating the movie was not found
        """
        # PREPARE
        request = _make_request(movie_name='Unknown Movie', num_tickets=2)

        # MOCK
        expect(self._movies, times=1).get_movie_by_name('Unknown Movie').thenReturn(None)

        # ACT / ASSERT
        with self.assertRaises(MovieNotFoundError) as ctx:
            booking_service.book_ticket(request)

        assert 'Movie not found' in str(ctx.exception)
        verifyExpectedInteractions()

    def test_booking_payment_fails(self) -> None:
        """
        Given: A valid booking request and a payment service that declines the charge
        When: book_ticket is called
        Then: A RuntimeError is raised with a message indicating payment failure
        """
        # PREPARE
        request = _make_request(movie_name='Inception', num_tickets=2)
        movie = _make_movie()

        # MOCK
        expect(self._movies, times=1).get_movie_by_name('Inception').thenReturn(movie)
        expect(self._payment, times=1).process_payment('Jane Doe', 30.0).thenReturn(False)

        # ACT / ASSERT
        with self.assertRaises(RuntimeError) as ctx:
            booking_service.book_ticket(request)

        assert 'Payment failed' in str(ctx.exception)
        verifyExpectedInteractions()

    def test_booking_underage_customer(self) -> None:
        """
        Given: A booking request where the customer's age is below the movie's minimum age
        When: book_ticket is called
        Then: A ValueError is raised before payment is attempted
        """
        # PREPARE
        request = _make_request(movie_name='Inception', num_tickets=2, customer_age=10)
        movie = _make_movie(min_age=18)

        # MOCK — payment must NOT be called; age check happens before it
        expect(self._movies, times=1).get_movie_by_name('Inception').thenReturn(movie)

        # ACT / ASSERT
        with self.assertRaises(AgeRequirementError) as ctx:
            booking_service.book_ticket(request)

        assert 'minimum age' in str(ctx.exception)
        verifyExpectedInteractions()

    def test_booking_customer_at_exact_min_age(self) -> None:
        """
        Given: A booking request where the customer's age exactly equals the movie's minimum age
        When: book_ticket is called
        Then: The booking succeeds — the boundary is inclusive
        """
        # PREPARE
        request = _make_request(movie_name='Inception', num_tickets=2, customer_age=18)
        movie = _make_movie(min_age=18)
        expected_ticket = Ticket(
            id=_FIXED_TICKET_ID,
            movie=movie,
            customer=Customer(name='Jane Doe', email='jane@example.com', age=18),
            price=30.0,
            purchase_date=_FIXED_PURCHASE_DATE,
            seat_number='B7',
        )

        # MOCK
        expect(ticket_module, times=1).generate_ticket_id().thenReturn(_FIXED_TICKET_ID)
        expect(ticket_module, times=1).generate_purchase_date().thenReturn(_FIXED_PURCHASE_DATE)
        expect(self._movies, times=1).get_movie_by_name('Inception').thenReturn(movie)
        expect(self._payment, times=1).process_payment('Jane Doe', 30.0).thenReturn(True)
        expect(self._db, times=1).save_ticket(expected_ticket).thenReturn(None)

        # ACT
        ticket = booking_service.book_ticket(request)

        # ASSERT
        assert ticket.customer.name == 'Jane Doe'
        assert ticket.movie.name == 'Inception'
        verifyExpectedInteractions()


if __name__ == '__main__':
    unittest.main()
