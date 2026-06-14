from ticketing_system.models.movie import Genre, Movie
from ticketing_system.models.ticket import Ticket


class _DatabaseService:
    """In-memory database for movies and tickets.

    Demonstrates dunder methods: __init__, __str__, __repr__, __len__, __contains__.
    """

    def __init__(self) -> None:
        self._movies: dict[str, Movie] = {}
        self._tickets: dict[str, list[Ticket]] = {}

    def __str__(self) -> str:
        return f'DatabaseService(movies={len(self._movies)}, tickets={sum(len(t) for t in self._tickets.values())})'

    def __repr__(self) -> str:
        return f'DatabaseService(_movies={list(self._movies.keys())!r})'

    def __len__(self) -> int:
        """Returns the total number of tickets stored."""
        return sum(len(tickets) for tickets in self._tickets.values())

    def __contains__(self, movie_name: str) -> bool:
        """Supports: 'Inception' in db"""
        return movie_name in self._movies

    def add_movie(self, movie: Movie) -> None:
        """Add a movie to the database.

        Args:
            movie: The movie to add.
        """
        self._movies[movie.name] = movie

    def get_movie_by_name(self, name: str) -> Movie | None:
        """Look up a movie by its title.

        Args:
            name: The movie title to search for.

        Returns:
            The Movie if found, None otherwise.
        """
        return self._movies.get(name)

    def get_all_movies(self) -> list[Movie]:
        """Return all movies in the database.

        Returns:
            List of all Movie objects.
        """
        return list(self._movies.values())

    def save_ticket(self, ticket: Ticket) -> None:
        """Persist a ticket for a customer.

        Args:
            ticket: The ticket to save.
        """
        email = ticket.customer.email
        if email not in self._tickets:
            self._tickets[email] = []
        self._tickets[email].append(ticket)

    def get_tickets_by_customer(self, email: str) -> list[Ticket]:
        """Retrieve all tickets purchased by a customer.

        Args:
            email: The customer's email address.

        Returns:
            List of tickets for the customer.
        """
        return self._tickets.get(email, [])


database_service: _DatabaseService = _DatabaseService()


def main() -> None:
    movie = Movie(name='Inception', genre=Genre.SCI_FI, duration_minutes=148, rating=8.8, release_year=2010)
    database_service.add_movie(movie)

    print(f'str(db): {database_service}')
    print(f'repr(db): {repr(database_service)}')
    print(f'len(db): {len(database_service)} tickets')
    print(f'"Inception" in db: {"Inception" in database_service}')
    print(f'"Avatar" in db: {"Avatar" in database_service}')


if __name__ == '__main__':
    main()
