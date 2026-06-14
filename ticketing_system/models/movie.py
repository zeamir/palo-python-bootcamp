# pyre-ignore-all-errors[6,13,15,56]
from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from ticketing_system.exceptions import BlankMovieNameError, InvalidReleaseYearError


class Genre(str, Enum):
    ACTION = 'action'
    COMEDY = 'comedy'
    DRAMA = 'drama'
    HORROR = 'horror'
    SCI_FI = 'sci_fi'


class Movie(BaseModel):
    """Represents a movie showing at the cinema."""

    model_config = ConfigDict(json_schema_extra={
        'example': {
            'name': 'Inception',
            'genre': 'sci_fi',
            'duration_minutes': 148,
            'rating': 8.8,
            'release_year': 2010,
            'min_age': 13,
        }
    })

    name: str = Field(description='The movie title')
    genre: Genre = Field(description='The movie genre')
    duration_minutes: int = Field(gt=0, description='Runtime in minutes')
    rating: float = Field(ge=0.0, le=10.0, description='Rating from 0 to 10')
    release_year: int = Field(description='Year the movie was released')
    min_age: int = Field(ge=0, default=0, description='Minimum viewer age requirement')

    @field_validator('name')
    @classmethod
    def name_must_not_be_blank(cls, value: str) -> str:
        """Reject empty or whitespace-only movie names."""
        if not value.strip():
            raise BlankMovieNameError('Movie name cannot be blank')
        return value.strip()

    @model_validator(mode='after')
    def release_year_not_in_far_future(self) -> Movie:
        """Ensure the release year is not more than one year in the future."""
        current_year = datetime.now().year
        if self.release_year > current_year + 1:
            raise InvalidReleaseYearError(f'Release year {self.release_year} is too far in the future')
        return self


def main() -> None:
    movie = Movie(
        name='Inception',
        genre=Genre.SCI_FI,
        duration_minutes=148,
        rating=8.8,
        release_year=2010,
        min_age=13,
    )

    print('--- model_dump() ---')
    print(movie.model_dump())

    print('\n--- model_dump_json(indent=2) ---')
    print(movie.model_dump_json(indent=2))


if __name__ == '__main__':
    main()
