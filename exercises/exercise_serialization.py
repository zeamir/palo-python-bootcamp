# pyre-ignore-all-errors[6,13,15,56]
"""
Exercise 3: Serialization
==========================

Goal: Practice serializing Pydantic models to dict and JSON with different options.

Instructions:
    1. Complete the TODOs below in the __main__ block.
    2. Run the file: poetry run python exercises/exercise_serialization.py

Tasks:
    A) Convert the receipt to a plain Python dict and print it
    B) Serialize the receipt but exclude the timestamp field
    C) Produce a pretty-printed JSON string of the receipt
    D) Serialize using the aliases defined on the model fields (customer_name -> buyer, title -> film)

See exercise_serialization_solution.py if you get stuck.
"""

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


if __name__ == '__main__':
    receipt = BookingReceipt(
        receipt_id='R-001',
        buyer='Jane Doe',
        movie=MovieSummary(film='Inception', genre='sci_fi'),
        total_price=30.0,
    )

    # A) Convert the receipt to a plain Python dict and print it

    # B) Serialize the receipt but exclude the timestamp field

    # C) Produce a pretty-printed JSON string of the receipt

    # D) Serialize using the aliases defined on the model fields
