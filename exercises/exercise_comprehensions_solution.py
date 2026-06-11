# pyre-ignore-all-errors[6,13,15,56]
"""
Exercise 3: Comprehensions - SOLUTION
======================================

Complete solutions for the comprehensions exercise.
"""
from __future__ import annotations

from collections.abc import Generator

# Sample movie data for testing
MOVIES = [
    {'title': 'Inception', 'genre': 'sci_fi', 'rating': 8.8, 'duration': 148},
    {'title': 'The Dark Knight', 'genre': 'action', 'rating': 9.0, 'duration': 152},
    {'title': 'Interstellar', 'genre': 'sci_fi', 'rating': 8.6, 'duration': 169},
    {'title': 'The Notebook', 'genre': 'romance', 'rating': 7.9, 'duration': 123},
    {'title': 'Get Out', 'genre': 'horror', 'rating': 7.7, 'duration': 104},
    {'title': 'Parasite', 'genre': 'thriller', 'rating': 8.6, 'duration': 132},
]


def get_highly_rated_titles(movies: list[dict]) -> list[str]:
    """
    Return a list of movie titles with rating > 8.0.

    Args:
        movies: List of movie dictionaries with 'title' and 'rating' keys.

    Returns:
        List of movie titles with rating > 8.0.
    """
    return [movie['title'] for movie in movies if movie['rating'] > 8.0]


def build_title_to_rating_map(movies: list[dict]) -> dict[str, float]:
    """
    Build a dictionary mapping movie title to its rating.

    Args:
        movies: List of movie dictionaries with 'title' and 'rating' keys.

    Returns:
        Dictionary mapping title (str) to rating (float).
    """
    return {movie['title']: movie['rating'] for movie in movies}


def extract_unique_genres(movies: list[dict]) -> set[str]:
    """
    Extract a set of unique genres from the movie list.

    Args:
        movies: List of movie dictionaries with 'genre' key.

    Returns:
        Set of unique genre strings.
    """
    return {movie['genre'] for movie in movies}


def apply_tax_to_prices(prices: list[float], tax_rate: float = 0.05) -> Generator[float, None, None]:
    """
    Return a generator that yields each ticket price with tax applied.

    Args:
        prices: List of ticket prices.
        tax_rate: Tax rate to apply (default 0.05 = 5%).

    Returns:
        Generator yielding prices with tax applied.
    """
    return (price * (1 + tax_rate) for price in prices)


def generate_seat_labels(rows: list[str], seats_per_row: int) -> list[str]:
    """
    Generate seat labels for a cinema seating chart.

    Example: rows=['A', 'B'], seats_per_row=3 → ['A1', 'A2', 'A3', 'B1', 'B2', 'B3']

    Args:
        rows: List of row labels (e.g., ['A', 'B', 'C']).
        seats_per_row: Number of seats per row.

    Returns:
        Flat list of seat labels (e.g., ['A1', 'A2', ...]).
    """
    return [f'{row}{seat}' for row in rows for seat in range(1, seats_per_row + 1)]


if __name__ == '__main__':
    print('=== Testing Comprehensions (SOLUTION) ===\n')

    # Test A: List comprehension
    print('A) Highly rated titles (>8.0):')
    titles = get_highly_rated_titles(MOVIES)
    print(f'   {titles}')
    assert len(titles) == 4
    assert 'Inception' in titles
    assert 'The Notebook' not in titles
    print('   ✓ Pass\n')

    # Test B: Dict comprehension
    print('B) Title → Rating mapping:')
    rating_map = build_title_to_rating_map(MOVIES)
    print(f'   {rating_map}')
    assert len(rating_map) == 6
    assert rating_map['The Dark Knight'] == 9.0
    print('   ✓ Pass\n')

    # Test C: Set comprehension
    print('C) Unique genres:')
    genres = extract_unique_genres(MOVIES)
    print(f'   {sorted(genres)}')
    assert len(genres) == 5  # 5 unique genres (sci_fi appears twice but counted once)
    assert 'sci_fi' in genres
    print('   ✓ Pass\n')

    # Test D: Generator expression
    print('D) Ticket prices with 5% tax:')
    prices = [12.50, 15.00, 18.50]
    taxed_prices = apply_tax_to_prices(prices)
    print(f'   Type: {type(taxed_prices)}')
    taxed_list = list(taxed_prices)
    print(f'   {taxed_list}')
    assert abs(taxed_list[0] - 13.125) < 0.01
    assert abs(taxed_list[1] - 15.75) < 0.01
    print('   ✓ Pass\n')

    # Test E: Nested comprehension
    print('E) Seat labels (rows A-C, 5 seats per row):')
    rows = ['A', 'B', 'C']
    seats = generate_seat_labels(rows, 5)
    print(f'   {seats}')
    assert len(seats) == 15
    assert seats[0] == 'A1'
    assert seats[4] == 'A5'
    assert seats[5] == 'B1'
    assert seats[-1] == 'C5'
    print('   ✓ Pass\n')

    print('All tests passed! ✓')
