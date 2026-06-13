# pyre-ignore-all-errors[6,13,15,56]
"""Exercise 1 Solution: Field Constraints"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class SnackOrder(BaseModel):
    model_config = ConfigDict(frozen=True)

    item_name: str = Field(min_length=1, description='Name of the snack item')
    price: float = Field(gt=0, description='Price per unit in USD')
    quantity: int = Field(gt=0, le=20, description='Number of units ordered (1-20)')
    category: Literal['drinks', 'snacks', 'meals'] = Field(description='Snack category')


def main() -> None:
    order = SnackOrder(item_name='Popcorn', price=6.50, quantity=2, category='snacks')
    print('Valid order:', order.model_dump())
    print('JSON:', order.model_dump_json(indent=2))


if __name__ == '__main__':
    main()
