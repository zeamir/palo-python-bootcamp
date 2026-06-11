from __future__ import annotations

from collections.abc import Iterator

"""
Solution: Dunder Methods (Magic Methods)

This solution demonstrates how to implement common dunder methods to make
a custom class behave like a built-in Python collection.
"""


class MovieCollection:
    """A collection of movies with Pythonic interfaces via dunder methods.

    This class uses plain dictionaries for simplicity (no Pydantic models).
    Each movie is stored as a dict with keys like 'title', 'genre', 'year', etc.

    Examples:
        >>> collection = MovieCollection()
        >>> collection.add({'title': 'Inception', 'year': 2010})
        >>> len(collection)
        1
        >>> 'Inception' in collection
        True
        >>> for movie in collection:
        ...     print(movie['title'])
        Inception
    """

    def __init__(self) -> None:
        """Initialize an empty movie collection."""
        self._movies: list[dict] = []

    def add(self, movie: dict) -> None:
        """Add a movie to the collection.

        Args:
            movie: A dictionary containing movie information (e.g., title, year).
        """
        self._movies.append(movie)

    def __len__(self) -> int:
        """Return the number of movies in the collection.

        Returns:
            The number of movies.
        """
        return len(self._movies)

    def __contains__(self, title: str) -> bool:
        """Check if a movie with the given title exists in the collection.

        Args:
            title: The movie title to search for.

        Returns:
            True if the title exists, False otherwise.
        """
        return any(movie.get('title') == title for movie in self._movies)

    def __getitem__(self, index: int) -> dict:
        """Get a movie by its index in the collection.

        Args:
            index: The zero-based index of the movie.

        Returns:
            The movie dictionary at that index.

        Raises:
            IndexError: If the index is out of range.
        """
        return self._movies[index]

    def __iter__(self) -> Iterator[dict]:
        """Return an iterator over the movies in the collection.

        Returns:
            An iterator over movie dictionaries.
        """
        return iter(self._movies)

    def __str__(self) -> str:
        """Return a human-readable string representation.

        Returns:
            A user-friendly string representation.
        """
        return f'MovieCollection({len(self._movies)} movies)'

    def __repr__(self) -> str:
        """Return a developer-friendly string representation.

        Returns:
            A detailed string representation for debugging.
        """
        return f'MovieCollection({repr(self._movies)})'


# ============================================================================
# Demo / Test Code
# ============================================================================

def main() -> None:
    """Demonstrate the dunder methods."""
    print('=== Creating a MovieCollection ===')
    collection = MovieCollection()
    print(f'Empty collection: {collection}')
    print(f'repr: {repr(collection)}\n')

    print('=== Adding movies ===')
    collection.add({'title': 'Inception', 'year': 2010, 'genre': 'Sci-Fi'})
    collection.add({'title': 'The Matrix', 'year': 1999, 'genre': 'Sci-Fi'})
    collection.add({'title': 'Interstellar', 'year': 2014, 'genre': 'Sci-Fi'})
    print(f'Collection after adding 3 movies: {collection}\n')

    print('=== Testing __len__ ===')
    print(f'len(collection) = {len(collection)}\n')

    print('=== Testing __contains__ ===')
    print(f'"Inception" in collection: {"Inception" in collection}')
    print(f'"Avatar" in collection: {"Avatar" in collection}\n')

    print('=== Testing __getitem__ ===')
    print(f'collection[0]: {collection[0]}')
    print(f'collection[1]: {collection[1]}')
    print(f'collection[-1]: {collection[-1]}\n')

    print('=== Testing __iter__ ===')
    print('Iterating over all movies:')
    for movie in collection:
        print(f'  - {movie["title"]} ({movie["year"]})')
    print()

    print('=== Testing __repr__ ===')
    print(f'repr(collection):')
    print(f'{repr(collection)}\n')

    print('=== Testing error case ===')
    try:
        _ = collection[10]
    except IndexError as e:
        print(f'IndexError when accessing collection[10]: {e}')


if __name__ == '__main__':
    main()
