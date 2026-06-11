from functools import lru_cache

from cachetools import TTLCache, cached

from ticketing_system.models.movie import Genre, Movie

# Seed data for demonstration
_MOVIE_DB: dict[str, Movie] = {
    'Inception': Movie(name='Inception', genre=Genre.SCI_FI, duration_minutes=148, rating=8.8, release_year=2010),
    'The Dark Knight': Movie(name='The Dark Knight', genre=Genre.ACTION, duration_minutes=152, rating=9.0, release_year=2008),
    'Interstellar': Movie(name='Interstellar', genre=Genre.SCI_FI, duration_minutes=169, rating=8.6, release_year=2014),
}

# --- stdlib: functools.lru_cache ---
# Simple in-process cache with no expiration.
# Cached by argument value — works best with immutable (hashable) arguments.
# maxsize=None means unlimited cache entries.


@lru_cache(maxsize=128)
def get_movie_by_name_cached(name: str) -> Movie | None:
    """Look up a movie by name, caching the result in memory.

    Args:
        name: The movie title to look up.

    Returns:
        The Movie if found, None otherwise.
    """
    print(f'[CACHE MISS] Fetching movie from DB: {name}')
    return _MOVIE_DB.get(name)


# --- cachetools: TTLCache ---
# Cache entries automatically expire after `ttl` seconds.
# Good for data that goes stale (e.g. showtimes, availability).

_available_movies_cache: TTLCache = TTLCache(maxsize=100, ttl=300)


@cached(cache=_available_movies_cache)
def get_available_movies_cached() -> list[Movie]:
    """Return all available movies, caching the list for 5 minutes.

    Returns:
        List of all Movie objects.
    """
    print('[CACHE MISS] Fetching all movies from DB')
    return list(_MOVIE_DB.values())


if __name__ == '__main__':
    print('=== lru_cache demo ===')
    m1 = get_movie_by_name_cached('Inception')
    m2 = get_movie_by_name_cached('Inception')  # cache hit — no print
    m3 = get_movie_by_name_cached('Interstellar')
    print(f'Cache info: {get_movie_by_name_cached.cache_info()}')

    print('\nClearing lru_cache...')
    get_movie_by_name_cached.cache_clear()
    print(f'Cache info after clear: {get_movie_by_name_cached.cache_info()}')

    print('\n=== TTLCache demo ===')
    movies1 = get_available_movies_cached()
    movies2 = get_available_movies_cached()  # cache hit — no print
    print(f'TTLCache size: {len(_available_movies_cache)} / {_available_movies_cache.maxsize}')
    print(f'Movies cached: {[m.name for m in movies1]}')
