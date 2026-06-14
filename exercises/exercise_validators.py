# pyre-ignore-all-errors[6,13,15,56]
"""
Exercise 2: Validators & Computed Fields
=========================================

Goal: Add validators and a computed field to a MoviePromotion model.

Instructions:
    1. Add the four validators/fields marked below so that the test cases at the bottom pass.
    2. Run the file to test your model: poetry run python exercises/exercise_validators.py

See exercise_validators_solution.py if you get stuck.
"""
from __future__ import annotations

from pydantic import BaseModel, Field, computed_field, field_validator, model_validator


class MoviePromotion(BaseModel):
    promo_code: str = Field(description='Promotion code (will be uppercased)')
    base_price: float = Field(gt=0, description='Original ticket price in USD')
    discount_percent: float = Field(description='Discount percentage (0-100)')
    min_tickets: int = Field(gt=0, description='Minimum tickets to qualify for promo')
    max_tickets: int = Field(gt=0, description='Maximum tickets allowed per purchase')

    @field_validator('discount_percent')
    @classmethod
    def validate_discount(cls, value: float) -> float:
        # TODO A: Reject invalid percentages
        # Hint: What's a valid percentage range?
        return value

    @model_validator(mode='before')
    @classmethod
    def normalize_promo_code(cls, data: dict) -> dict:
        # TODO B: Normalize the promo code
        # Hint: Normalize so 'summer20' and 'SUMMER20' are treated the same
        return data

    @computed_field
    @property
    def final_price(self) -> float:
        # TODO C: Calculate the discounted price
        # Hint: Calculate what the customer actually pays after the discount
        return 0.0

    @model_validator(mode='after')
    def validate_ticket_range(self) -> MoviePromotion:
        # TODO D: Ensure valid ticket range
        # Hint: The upper bound of a range can't be below the lower bound
        return self


def main() -> None:
    promo = MoviePromotion(promo_code='summer20', base_price=15.0, discount_percent=20, min_tickets=2, max_tickets=6)
    print('Promo:', promo.model_dump())
    print(f'Expected promo_code: SUMMER20, got: {promo.promo_code}')
    print(f'Expected final_price: 12.0, got: {promo.final_price}')
    print(f'Ticket range: {promo.min_tickets}-{promo.max_tickets}')

    # Uncomment to test validation errors:
    # MoviePromotion(promo_code='X', base_price=15.0, discount_percent=150, min_tickets=1, max_tickets=4)  # invalid discount
    # MoviePromotion(promo_code='X', base_price=15.0, discount_percent=10, min_tickets=5, max_tickets=2)   # invalid range


if __name__ == '__main__':
    main()
