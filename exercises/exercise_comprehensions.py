"""
Exercise 3: Comprehensions
===========================

Goal: Practice using Python comprehensions to transform data efficiently.

Instructions:
    1. Complete the five functions where marked TODO.
    2. Run the file to test your solutions: poetry run python exercises/exercise_comprehensions.py

Each function demonstrates a different type of comprehension:
    A) List comprehension with filtering
    B) Dict comprehension for key-value mapping
    C) Set comprehension for unique values
    D) Generator expression for memory-efficient iteration
    E) Nested comprehension for multi-dimensional data

See exercise_comprehensions_solution.py if you get stuck.
"""
# pyre-ignore-all-errors[6,13,15,56]
# pylint: disable=unnecessary-pass,unused-argument,no-self-use,unnecessary-ellipsis

from __future__ import annotations

from collections.abc import Generator

# Sample movie data for testing
MOVIES = [
    {
        'title': 'Inception',
        'genre': 'sci_fi',
        'rating': 8.8,
        'duration': 148
    },
    {
        'title': 'The Dark Knight',
        'genre': 'action',
        'rating': 9.0,
        'duration': 152
    },
    {
        'title': 'Interstellar',
        'genre': 'sci_fi',
        'rating': 8.6,
        'duration': 169
    },
    {
        'title': 'The Notebook',
        'genre': 'romance',
        'rating': 7.9,
        'duration': 123
    },
    {
        'title': 'Get Out',
        'genre': 'horror',
        'rating': 7.7,
        'duration': 104
    },
    {
        'title': 'Parasite',
        'genre': 'thriller',
        'rating': 8.6,
        'duration': 132
    },
]


def get_highly_rated_titles(movies: list[dict]) -> list[str]:
    """
    Return a list of movie titles with rating > 8.0.

    Hint: You only need the titles, not the full movie dicts.
    Hint: Use a condition to filter movies by rating.

    Args:
        movies: List of movie dictionaries with 'title' and 'rating' keys.

    Returns:
        List of movie titles with rating > 8.0.
    """
    # TODO A: Return titles of movies rated above 8.0
    return []


def build_title_to_rating_map(movies: list[dict]) -> dict[str, float]:
    """
    Build a dictionary mapping movie title to its rating.

    Hint: Think about what should be the key and what should be the value.

    Args:
        movies: List of movie dictionaries with 'title' and 'rating' keys.

    Returns:
        Dictionary mapping title (str) to rating (float).
    """
    # TODO B: Map each title to its rating
    return {}


def extract_unique_genres(movies: list[dict]) -> set[str]:
    """
    Extract a set of unique genres from the movie list.

    Hint: A set automatically removes duplicates for you.

    Args:
        movies: List of movie dictionaries with 'genre' key.

    Returns:
        Set of unique genre strings.
    """
    # TODO C: Collect unique genres
    return set()


def apply_tax_to_prices(prices: list[float], tax_rate: float = 0.05) -> Generator[float, None, None]:
    """
    Return a generator that yields each ticket price with tax applied.

    Hint: Don't create a list — use a generator expression for memory efficiency.
    Hint: Formula is: price * (1 + tax_rate).

    Args:
        prices: List of ticket prices.
        tax_rate: Tax rate to apply (default 0.05 = 5%).

    Returns:
        Generator yielding prices with tax applied.
    """
    # TODO D: Yield each price with tax applied
    return (p for p in [])  # Replace this placeholder


def generate_seat_labels(rows: list[str], seats_per_row: int) -> list[str]:
    """
    Generate seat labels for a cinema seating chart.

    Example: rows=['A', 'B'], seats_per_row=3 → ['A1', 'A2', 'A3', 'B1', 'B2', 'B3']

    Hint: You need to combine each row with each seat number (1 to seats_per_row).
    Hint: The outer loop is the rows, the inner loop is the seat numbers.

    Args:
        rows: List of row labels (e.g., ['A', 'B', 'C']).
        seats_per_row: Number of seats per row.

    Returns:
        Flat list of seat labels (e.g., ['A1', 'A2', ...]).
    """
    # TODO E: Generate all seat labels
    return []


def main() -> None:
    print('=== Testing Comprehensions ===\n')

    # Test A: List comprehension
    print('A) Highly rated titles (>8.0):')
    titles = get_highly_rated_titles(MOVIES)
    print(f'   {titles}')
    print('   Expected: 4 titles\n')

    # Test B: Dict comprehension
    print('B) Title → Rating mapping:')
    rating_map = build_title_to_rating_map(MOVIES)
    print(f'   {rating_map}')
    print('   Expected: 6 entries\n')

    # Test C: Set comprehension
    print('C) Unique genres:')
    genres = extract_unique_genres(MOVIES)
    print(f'   {sorted(genres)}')
    print('   Expected: 5 unique genres\n')

    # Test D: Generator expression
    print('D) Ticket prices with 5% tax:')
    prices = [12.50, 15.00, 18.50]
    taxed_prices = apply_tax_to_prices(prices)
    print(f'   Type: {type(taxed_prices)}')
    taxed_list = list(taxed_prices)
    print(f'   {taxed_list}')
    print('   Expected: [13.125, 15.75, 19.425]\n')

    # Test E: Nested comprehension
    print('E) Seat labels (rows A-C, 5 seats per row):')
    rows = ['A', 'B', 'C']
    seats = generate_seat_labels(rows, 5)
    print(f'   {seats}')
    print('   Expected: 15 labels total\n')


if __name__ == '__main__':
    main()
