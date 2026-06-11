# pyre-ignore-all-errors[6,13,15,56]
"""Exercise 2 Solution: Validators & Computed Fields"""
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
        if not 0 <= value <= 100:
            raise ValueError(f'Discount must be between 0 and 100, got {value}')
        return value

    @model_validator(mode='before')
    @classmethod
    def normalize_promo_code(cls, data: dict) -> dict:
        if 'promo_code' in data and isinstance(data['promo_code'], str):
            data['promo_code'] = data['promo_code'].upper()
        return data

    @computed_field
    @property
    def final_price(self) -> float:
        return self.base_price * (1 - self.discount_percent / 100)

    @model_validator(mode='after')
    def validate_ticket_range(self) -> MoviePromotion:
        if self.max_tickets < self.min_tickets:
            raise ValueError(
                f'max_tickets ({self.max_tickets}) must be >= min_tickets ({self.min_tickets})'
            )
        return self


if __name__ == '__main__':
    promo = MoviePromotion(promo_code='summer20', base_price=15.0, discount_percent=20, min_tickets=2, max_tickets=6)
    print('Promo:', promo.model_dump())
    print(f'promo_code: {promo.promo_code}')  # SUMMER20
    print(f'final_price: {promo.final_price}')  # 12.0
    print(f'Ticket range: {promo.min_tickets}-{promo.max_tickets}')
    print('JSON:', promo.model_dump_json(indent=2))
