from __future__ import annotations

# pyre-ignore-all-errors[6,13,15,56]

from collections.abc import Iterator

"""
Exercise: Dunder Methods (Magic Methods)

In this exercise, you'll implement a MovieCollection class that demonstrates
common dunder methods used to make custom classes behave like built-in types.

Dunder methods (double underscore, aka "magic methods") allow you to customize
how your objects interact with Python's built-in operations and syntax.

Reference: ticketing_system/services/database_service.py
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
        # Hint: You'll need an internal container to store movie dicts
        pass

    def add(self, movie: dict) -> None:
        """Add a movie to the collection.

        Args:
            movie: A dictionary containing movie information (e.g., title, year).
        """
        # Hint: Append to your internal container
        pass

    def __len__(self) -> int:
        """Return the number of movies in the collection.

        Hint: Enables len(collection). How many movies are stored?

        Returns:
            The number of movies.
        """
        # Hint: How many items are in your container?
        return 0

    def __contains__(self, title: str) -> bool:
        """Check if a movie with the given title is in the collection.

        Hint: Enables 'Inception' in collection. Search by title.

        Args:
            title: The movie title to search for.

        Returns:
            True if a movie with that title exists, False otherwise.
        """
        # Hint: Check if any stored movie has a matching 'title'
        return False

    def __getitem__(self, index: int) -> dict:
        """Get a movie by its position in the collection.

        Hint: Enables collection[0] and collection[-1] syntax.

        Args:
            index: The zero-based index of the movie.

        Returns:
            The movie dictionary at that index.

        Raises:
            IndexError: If the index is out of range.
        """
        # Hint: Delegate to your internal container's indexing
        return {}

    def __iter__(self) -> Iterator[dict]:
        """Iterate over the movies in the collection.

        Hint: Enables 'for movie in collection' syntax.

        Returns:
            An iterator over movie dictionaries.
        """
        # Hint: Delegate to your internal container's iterator
        return iter([])

    def __str__(self) -> str:
        """Return a human-readable description of the collection.

        Hint: Called by print(). Should be useful to an end user.

        Returns:
            A concise, user-friendly string.
        """
        # Hint: Show the number of movies in a readable way
        return 'MovieCollection(0 movies)'

    def __repr__(self) -> str:
        """Return a developer-friendly representation showing internal state.

        Hint: Called by repr() and in the REPL. Should show enough detail
        for a developer to understand the object's current state.

        Returns:
            A detailed string representation.
        """
        # Hint: Show the actual contents of your internal container
        return 'MovieCollection([])'


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
