# pyre-ignore-all-errors[6,13,15,56]
from __future__ import annotations

from dataclasses import dataclass


class MoviePromotionNative:
    """
    Native Python class implementation of MoviePromotion.

    Demonstrates manual implementation with explicit __init__, validation,
    and property-based computed fields.

    Attributes:
        promo_code: Promotion code (uppercased).
        base_price: Original ticket price in USD (must be > 0).
        discount_percent: Discount percentage (0-100 inclusive).
        min_tickets: Minimum tickets to qualify for promo (must be > 0).
        max_tickets: Maximum tickets allowed per purchase (must be > 0 and >= min_tickets).
    """

    def __init__(
        self,
        promo_code: str,
        base_price: float,
        discount_percent: float,
        min_tickets: int,
        max_tickets: int,
    ) -> None:
        """
        Initialize a MoviePromotionNative instance with validation.

        Args:
            promo_code: Promotion code (will be uppercased).
            base_price: Original ticket price in USD.
            discount_percent: Discount percentage (0-100).
            min_tickets: Minimum tickets to qualify.
            max_tickets: Maximum tickets allowed per purchase.

        Raises:
            ValueError: If validation fails for any field.
        """
        # Validate base_price
        if base_price <= 0:
            raise ValueError(f'base_price must be > 0, got {base_price}')

        # Validate discount_percent
        if not 0 <= discount_percent <= 100:
            raise ValueError(
                f'discount_percent must be between 0 and 100, got {discount_percent}'
            )

        # Validate min_tickets
        if min_tickets <= 0:
            raise ValueError(f'min_tickets must be > 0, got {min_tickets}')

        # Validate max_tickets
        if max_tickets <= 0:
            raise ValueError(f'max_tickets must be > 0, got {max_tickets}')

        # Validate ticket range
        if max_tickets < min_tickets:
            raise ValueError(
                f'max_tickets ({max_tickets}) must be >= min_tickets ({min_tickets})'
            )

        # Assign values
        self.promo_code = promo_code.upper()
        self.base_price = base_price
        self.discount_percent = discount_percent
        self.min_tickets = min_tickets
        self.max_tickets = max_tickets

    @property
    def final_price(self) -> float:
        """Calculate the final price after discount."""
        return self.base_price * (1 - self.discount_percent / 100)

    def __repr__(self) -> str:
        """Return a developer-friendly representation."""
        return (f'MoviePromotionNative('
                f'promo_code={self.promo_code!r}, '
                f'base_price={self.base_price}, '
                f'discount_percent={self.discount_percent}, '
                f'min_tickets={self.min_tickets}, '
                f'max_tickets={self.max_tickets})')

    def __str__(self) -> str:
        """Return a user-friendly representation."""
        return (f'Promo {self.promo_code}: {self.discount_percent}% off '
                f'(${self.base_price} → ${self.final_price:.2f}) '
                f'for {self.min_tickets}-{self.max_tickets} tickets')


@dataclass
class MoviePromotionDataclass:
    """
    Dataclass implementation of MoviePromotion.

    Uses Python's @dataclass decorator for automatic __init__, __repr__, etc.
    Validation is performed in __post_init__.

    Attributes:
        promo_code: Promotion code (uppercased).
        base_price: Original ticket price in USD (must be > 0).
        discount_percent: Discount percentage (0-100 inclusive).
        min_tickets: Minimum tickets to qualify for promo (must be > 0).
        max_tickets: Maximum tickets allowed per purchase (must be > 0 and >= min_tickets).
    """

    promo_code: str
    base_price: float
    discount_percent: float
    min_tickets: int
    max_tickets: int

    def __post_init__(self) -> None:
        """
        Validate fields and normalize data after initialization.

        Raises:
            ValueError: If validation fails for any field.
        """
        # Validate base_price
        if self.base_price <= 0:
            raise ValueError(f'base_price must be > 0, got {self.base_price}')

        # Validate discount_percent
        if not 0 <= self.discount_percent <= 100:
            raise ValueError(
                f'discount_percent must be between 0 and 100, got {self.discount_percent}'
            )

        # Validate min_tickets
        if self.min_tickets <= 0:
            raise ValueError(
                f'min_tickets must be > 0, got {self.min_tickets}')

        # Validate max_tickets
        if self.max_tickets <= 0:
            raise ValueError(
                f'max_tickets must be > 0, got {self.max_tickets}')

        # Validate ticket range
        if self.max_tickets < self.min_tickets:
            raise ValueError(
                f'max_tickets ({self.max_tickets}) must be >= min_tickets ({self.min_tickets})'
            )

        # Normalize promo_code to uppercase
        self.promo_code = self.promo_code.upper()

    @property
    def final_price(self) -> float:
        """Calculate the final price after discount."""
        return self.base_price * (1 - self.discount_percent / 100)


# ==============================================================================
# COMPARISON: Pydantic vs Native Class vs Dataclass
# ==============================================================================
#
# **Pydantic (MoviePromotion in exercises/exercise_validators_solution.py):**
# - Pros:
#   * Automatic validation with Field constraints (gt=0, etc.)
#   * Built-in JSON serialization/deserialization
#   * Declarative syntax with @field_validator, @model_validator, @computed_field
#   * Excellent for APIs, configs, and data interchange
#   * Type coercion (e.g., "15" → 15.0)
#   * Rich ecosystem and IDE support
# - Cons:
#   * External dependency (adds weight to your project)
#   * Learning curve for validators and model_validator modes
#   * Slight runtime overhead vs native Python
# - When to use: REST APIs, configuration files, data pipelines, anything
#   involving JSON or external data.
#
# **Native Class (MoviePromotionNative):**
# - Pros:
#   * No dependencies - pure Python
#   * Full control over initialization and validation logic
#   * Clear and explicit - easy to understand
#   * Maximum flexibility
# - Cons:
#   * Verbose - lots of boilerplate
#   * Manual serialization/deserialization
#   * No automatic type coercion
#   * Easy to forget validation or normalization
# - When to use: Small internal classes, educational purposes, when you need
#   complete control or cannot add dependencies.
#
# **Dataclass (MoviePromotionDataclass):**
# - Pros:
#   * Built into Python (3.7+) - no external deps
#   * Reduces boilerplate (__init__, __repr__, etc. auto-generated)
#   * Clean declarative syntax
#   * Good balance between convenience and control
# - Cons:
#   * No automatic validation - must write __post_init__
#   * No built-in JSON serialization (though dataclasses.asdict helps)
#   * Validation in __post_init__ runs *after* assignment, so invalid state
#     exists momentarily
#   * No type coercion
# - When to use: Internal data structures, DTOs within your application, when
#   you want cleaner code than native classes but don't need Pydantic's features.
#
# **Rule of Thumb:**
# - Use **Pydantic** for external data (APIs, configs, user input)
# - Use **dataclasses** for internal data structures
# - Use **native classes** when you need special behavior or zero dependencies
# ==============================================================================

if __name__ == '__main__':
    print('=' * 70)
    print('NATIVE CLASS EXAMPLES')
    print('=' * 70)

    # Valid example
    print('\n1. Valid promotion (Native):')
    promo_native = MoviePromotionNative(
        promo_code='summer20',
        base_price=15.0,
        discount_percent=20,
        min_tickets=2,
        max_tickets=6,
    )
    print(f'   repr: {promo_native!r}')
    print(f'   str:  {promo_native}')
    print(f'   final_price: ${promo_native.final_price:.2f}')

    # Invalid examples - demonstrate validation errors
    print('\n2. Invalid: negative base_price (Native):')
    try:
        MoviePromotionNative(
            promo_code='invalid',
            base_price=-10.0,
            discount_percent=20,
            min_tickets=2,
            max_tickets=6,
        )
    except ValueError as e:
        print(f'   ✓ Caught: {e}')

    print('\n3. Invalid: discount_percent > 100 (Native):')
    try:
        MoviePromotionNative(
            promo_code='invalid',
            base_price=15.0,
            discount_percent=150,
            min_tickets=2,
            max_tickets=6,
        )
    except ValueError as e:
        print(f'   ✓ Caught: {e}')

    print('\n4. Invalid: max_tickets < min_tickets (Native):')
    try:
        MoviePromotionNative(
            promo_code='invalid',
            base_price=15.0,
            discount_percent=20,
            min_tickets=6,
            max_tickets=2,
        )
    except ValueError as e:
        print(f'   ✓ Caught: {e}')

    print('\n' + '=' * 70)
    print('DATACLASS EXAMPLES')
    print('=' * 70)

    # Valid example
    print('\n5. Valid promotion (Dataclass):')
    promo_dataclass = MoviePromotionDataclass(
        promo_code='winter25',
        base_price=20.0,
        discount_percent=25,
        min_tickets=1,
        max_tickets=4,
    )
    print(f'   repr: {promo_dataclass!r}')
    print(f'   final_price: ${promo_dataclass.final_price:.2f}')
    print(f'   promo_code (uppercased): {promo_dataclass.promo_code}')

    # Invalid examples
    print('\n6. Invalid: zero min_tickets (Dataclass):')
    try:
        MoviePromotionDataclass(
            promo_code='invalid',
            base_price=15.0,
            discount_percent=20,
            min_tickets=0,
            max_tickets=6,
        )
    except ValueError as e:
        print(f'   ✓ Caught: {e}')

    print('\n7. Invalid: negative discount_percent (Dataclass):')
    try:
        MoviePromotionDataclass(
            promo_code='invalid',
            base_price=15.0,
            discount_percent=-10,
            min_tickets=2,
            max_tickets=6,
        )
    except ValueError as e:
        print(f'   ✓ Caught: {e}')

    print('\n' + '=' * 70)
    print('COMPARISON')
    print('=' * 70)
    print('\nBoth implementations produce the same validation behavior:')
    print(
        f'  Native:    {promo_native.promo_code} → ${promo_native.final_price:.2f}'
    )
    print(
        f'  Dataclass: {promo_dataclass.promo_code} → ${promo_dataclass.final_price:.2f}'
    )
    print(
        '\nSee the comparison comment block above for when to use each approach.'
    )
