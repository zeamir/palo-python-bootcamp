# pyre-ignore-all-errors[6,13,15,56]
"""
Exercise 1: Field Constraints
==============================

Goal: Define a SnackOrder model for the cinema snack bar using Pydantic Field() constraints.

Instructions:
    1. Complete the SnackOrder model by adding appropriate constraints to each field.
    2. The validation cases at the bottom should behave correctly when you're done.
    3. Run the file to test your model: poetry run python exercises/exercise_field_constraints.py

See exercise_field_constraints_solution.py if you get stuck.
"""

from pydantic import BaseModel, ConfigDict, Field


class SnackOrder(BaseModel):
    model_config = ConfigDict(frozen=True)

    item_name: str = Field()  # Hint: Prevent empty item names
    price: float = Field()  # Hint: Prices must be positive
    quantity: int = Field()  # Hint: Reasonable quantity bounds for a single order
    category: str = Field()  # Hint: Only specific categories are valid


if __name__ == '__main__':
    # These should all succeed
    order = SnackOrder(item_name='Popcorn', price=6.50, quantity=2, category='snacks')
    print('Valid order:', order.model_dump())

    # Uncomment to test constraint violations:
    # SnackOrder(item_name='', price=6.50, quantity=2, category='snacks')     # empty name
    # SnackOrder(item_name='Cola', price=-1.0, quantity=1, category='drinks') # negative price
    # SnackOrder(item_name='Cola', price=3.0, quantity=25, category='drinks') # quantity too high
    # SnackOrder(item_name='Cola', price=3.0, quantity=1, category='candy')   # invalid category
