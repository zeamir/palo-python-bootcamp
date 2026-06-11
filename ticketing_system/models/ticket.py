# pyre-ignore-all-errors[6,13,15]
from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

from ticketing_system.models.customer import Customer
from ticketing_system.models.movie import Movie


class Ticket(BaseModel):
    """Represents a purchased cinema ticket."""

    model_config = ConfigDict(frozen=True)

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description='Unique ticket identifier')
    movie: Movie = Field(description='The movie this ticket is for')
    customer: Customer = Field(description='The customer who purchased the ticket')
    price: float = Field(gt=0, description='Ticket price in USD')
    purchase_date: datetime = Field(
        default_factory=datetime.now,
        description='Date and time of purchase',
    )
    seat_number: str = Field(description='Assigned seat (e.g. A12)')

    @model_validator(mode='after')
    def validate_age_requirement(self) -> Ticket:
        """Ensure the customer meets the movie's minimum age requirement."""
        if self.customer.age < self.movie.min_age:
            raise ValueError(f'Customer age {self.customer.age} does not meet the minimum age '
                             f'requirement of {self.movie.min_age} for "{self.movie.name}"')
        return self


if __name__ == '__main__':
    from ticketing_system.models.movie import Genre

    movie = Movie(name='Inception', genre=Genre.SCI_FI, duration_minutes=148, rating=8.8, release_year=2010)
    customer = Customer(name='Jane Doe', email='jane@example.com', age=30)
    ticket = Ticket(movie=movie, customer=customer, price=15.50, seat_number='B7')

    print('--- model_dump() ---')
    print(ticket.model_dump())

    print('\n--- model_dump_json(indent=2) ---')
    print(ticket.model_dump_json(indent=2))

    print('\n--- model_dump(include={"id", "seat_number", "price"}) ---')
    print(ticket.model_dump(include={'id', 'seat_number', 'price'}))
