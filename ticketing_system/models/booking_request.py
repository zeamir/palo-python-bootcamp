# pyre-ignore-all-errors[6,13,15,56]
from pydantic import BaseModel, Field


class BookingRequest(BaseModel):
    """Represents a request to book cinema tickets."""

    customer_name: str = Field(description='Full name of the customer')
    customer_email: str = Field(description='Email address of the customer')
    customer_age: int = Field(gt=0, description='Age of the customer')
    movie_name: str = Field(description='Name of the movie to book')
    num_tickets: int = Field(gt=0, le=10, description='Number of tickets to purchase (1-10)')
    seat_number: str = Field(description='Requested seat number (e.g. A12)')
