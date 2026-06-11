from __future__ import annotations

from collections.abc import Generator

"""
Comprehensions: Concise Syntax for Data Transformation
=======================================================

This module demonstrates Python's comprehension syntax using the cinema ticketing domain.
Comprehensions provide a readable, expressive way to build sequences from existing data.

Types covered:
  - List comprehensions: filter and transform sequences into a new list
  - Dict comprehensions: build key-value mappings from iterables
  - Set comprehensions: extract unique values
  - Generator expressions: lazy evaluation for memory-efficient iteration
  - Nested comprehensions: multi-dimensional data structures
"""

# Sample movie data for demonstration
MOVIES = [
    {'title': 'Inception', 'genre': 'sci_fi', 'rating': 8.8, 'duration': 148},
    {'title': 'The Dark Knight', 'genre': 'action', 'rating': 9.0, 'duration': 152},
    {'title': 'Interstellar', 'genre': 'sci_fi', 'rating': 8.6, 'duration': 169},
    {'title': 'The Notebook', 'genre': 'romance', 'rating': 7.9, 'duration': 123},
    {'title': 'Get Out', 'genre': 'horror', 'rating': 7.7, 'duration': 104},
    {'title': 'Parasite', 'genre': 'thriller', 'rating': 8.6, 'duration': 132},
]

TICKET_PRICES = [12.50, 15.00, 18.50, 20.00, 22.00]


def demo_list_comprehension() -> None:
    """
    List Comprehension: [expression for item in iterable if condition]

    WHAT: Creates a new list by applying an expression to each item that meets a condition.
    WHEN: Use when you need to filter and/or transform a sequence into a new list.
    WHY: More readable than a for-loop with append(), and often faster.
    """
    print('=== List Comprehension ===')

    # Filter movies with rating > 8.0
    highly_rated_titles = [movie['title'] for movie in MOVIES if movie['rating'] > 8.0]

    print(f'Highly rated movies (>8.0): {highly_rated_titles}')
    print(f'Count: {len(highly_rated_titles)}')


def demo_dict_comprehension() -> None:
    """
    Dict Comprehension: {key_expr: value_expr for item in iterable if condition}

    WHAT: Creates a new dictionary by mapping keys to values from an iterable.
    WHEN: Use when you need to build a lookup table or transform a sequence into key-value pairs.
    WHY: More concise than a for-loop with dict assignment, makes intent clear.
    """
    print('\n=== Dict Comprehension ===')

    # Build a mapping from movie title to genre
    movie_genres = {movie['title']: movie['genre'] for movie in MOVIES}

    print('Movie → Genre mapping:')
    for title, genre in movie_genres.items():
        print(f'  {title}: {genre}')


def demo_set_comprehension() -> None:
    """
    Set Comprehension: {expression for item in iterable if condition}

    WHAT: Creates a new set (unordered collection of unique values).
    WHEN: Use when you need to extract distinct values from a sequence.
    WHY: Automatic deduplication, O(1) membership testing.
    """
    print('\n=== Set Comprehension ===')

    # Extract unique genres from all movies
    unique_genres = {movie['genre'] for movie in MOVIES}

    print(f'Unique genres: {sorted(unique_genres)}')
    print(f'Count: {len(unique_genres)}')


def demo_generator_expression() -> None:
    """
    Generator Expression: (expression for item in iterable if condition)

    WHAT: Creates a generator that yields values lazily (one at a time on demand).
    WHEN: Use when processing large datasets or when you only need to iterate once.
    WHY: Memory-efficient — doesn't build the entire list in memory upfront.

    Note: Use parentheses () instead of square brackets [].
    """
    print('\n=== Generator Expression ===')

    # Compute total revenue from ticket prices (with tax applied)
    TAX_RATE = 0.05

    # Generator expression: values are computed on-the-fly
    prices_with_tax = (price * (1 + TAX_RATE) for price in TICKET_PRICES)

    print(f'Ticket prices (before tax): {TICKET_PRICES}')
    print(f'Type: {type(prices_with_tax)}')

    # Consume the generator to compute total revenue
    total_revenue = sum(prices_with_tax)
    print(f'Total revenue (after {TAX_RATE*100}% tax): ${total_revenue:.2f}')

    # Note: generator is now exhausted — can't iterate again
    print(f'Attempting to sum again: ${sum(prices_with_tax):.2f}')  # returns 0


def demo_nested_comprehension() -> None:
    """
    Nested Comprehension: [expr for outer in iter1 for inner in iter2]

    WHAT: Flattens nested loops into a single list comprehension.
    WHEN: Use for creating multi-dimensional data structures (e.g., seat maps, grids).
    WHY: Compact syntax for cartesian products and nested iteration.

    Structure: outer loop first, inner loop second (reads left to right).
    """
    print('\n=== Nested Comprehension ===')

    # Generate seat labels: rows A-E, seats 1-10
    ROWS = ['A', 'B', 'C', 'D', 'E']
    SEATS_PER_ROW = 10

    # Nested comprehension: for each row, generate all seats
    seat_map = [f'{row}{seat}' for row in ROWS for seat in range(1, SEATS_PER_ROW + 1)]

    print(f'Total seats: {len(seat_map)}')
    print(f'First 10 seats: {seat_map[:10]}')
    print(f'Last 10 seats: {seat_map[-10:]}')


if __name__ == '__main__':
    demo_list_comprehension()
    demo_dict_comprehension()
    demo_set_comprehension()
    demo_generator_expression()
    demo_nested_comprehension()
