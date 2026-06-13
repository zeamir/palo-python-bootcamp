# pyre-ignore-all-errors[6,13,15,56]
"""Exercise 3 Solution: Serialization"""

from datetime import datetime

from pydantic import BaseModel, Field


class MovieSummary(BaseModel):
    title: str = Field(alias='film', description='Movie title')
    genre: str

    model_config = {'populate_by_name': True}


class BookingReceipt(BaseModel):
    receipt_id: str
    customer_name: str = Field(alias='buyer', description='Customer full name')
    movie: MovieSummary
    total_price: float
    purchase_date: datetime = Field(default_factory=datetime.now)

    model_config = {'populate_by_name': True}


def main() -> None:
    receipt = BookingReceipt(
        receipt_id='R-001',
        buyer='Jane Doe',
        movie=MovieSummary(film='Inception', genre='sci_fi'),
        total_price=30.0,
    )

    print('=== A: model_dump() ===')
    print(receipt.model_dump())

    print('\n=== B: model_dump(exclude={"purchase_date"}) ===')
    print(receipt.model_dump(exclude={'purchase_date'}))

    print('\n=== C: model_dump_json(indent=2) ===')
    print(receipt.model_dump_json(indent=2))

    print('\n=== D: model_dump(by_alias=True) ===')
    print(receipt.model_dump(by_alias=True))


if __name__ == '__main__':
    main()
