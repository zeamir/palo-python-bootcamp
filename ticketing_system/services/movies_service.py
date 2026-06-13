from cachetools import TTLCache, cached

from ticketing_system.models.movie import Genre, Movie
from ticketing_system.services.database_service import _DatabaseService, database_service

_movie_by_name_cache: TTLCache = TTLCache(maxsize=100, ttl=300)
_all_movies_cache: TTLCache = TTLCache(maxsize=1, ttl=300)


class _MoviesService:
    """Provides cached movie lookups backed by a _DatabaseService.

    Access via the module-level `movies_service` singleton. Use `set_db` to
    inject a custom _DatabaseService (e.g. in tests).
    """

    def __init__(self) -> None:
        self._db_instance: _DatabaseService | None = None

    @property
    def _db(self) -> _DatabaseService:
        if self._db_instance is None:
            self._db_instance = database_service
        return self._db_instance

    def set_db(self, db: _DatabaseService) -> None:
        """Inject a _DatabaseService instance (useful for testing).

        Args:
            db: The _DatabaseService to use for movie lookups.
        """
        self._db_instance = db

    @cached(cache=_movie_by_name_cache)
    def get_movie_by_name(self, name: str) -> Movie | None:
        """Return the full Movie for a given title, caching the result.

        Args:
            name: The movie title to look up.

        Returns:
            The Movie if found, None otherwise.
        """
        print(f'[CACHE MISS] Fetching movie from DB: {name}')
        return self._db.get_movie_by_name(name)

    @cached(cache=_all_movies_cache)
    def get_all_movies(self) -> list[str]:
        """Return the names of all movies, caching the list for 5 minutes.

        Returns:
            List of movie title strings.
        """
        print('[CACHE MISS] Fetching all movies from DB')
        return [movie.name for movie in self._db.get_all_movies()]


movies_service: _MoviesService = _MoviesService()


def main() -> None:
    database_service.add_movie(Movie(name='Inception', genre=Genre.SCI_FI, duration_minutes=148, rating=8.8, release_year=2010))
    database_service.add_movie(Movie(name='The Dark Knight', genre=Genre.ACTION, duration_minutes=152, rating=9.0, release_year=2008))
    database_service.add_movie(Movie(name='Interstellar', genre=Genre.SCI_FI, duration_minutes=169, rating=8.6, release_year=2014))

    print('=== get_movie_by_name ===')
    m1 = movies_service.get_movie_by_name('Inception')
    m2 = movies_service.get_movie_by_name('Inception')  # cache hit — no print
    print(f'Movie: {m1}')
    print(f'Same object from cache: {m1 is m2}')

    print('\n=== get_all_movies ===')
    names1 = movies_service.get_all_movies()
    names2 = movies_service.get_all_movies()  # cache hit — no print
    print(f'Movies: {names1}')
    print(f'Same list from cache: {names1 is names2}')


if __name__ == '__main__':
    main()
