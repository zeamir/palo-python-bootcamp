# pyre-ignore-all-errors[6,13,15,56]
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from ticketing_system.exceptions import InvalidEmailError


class Customer(BaseModel):
    """Represents a cinema customer."""

    model_config = ConfigDict(json_schema_extra={'example': {
        'name': 'Jane Doe',
        'email': 'jane@example.com',
        'age': 30,
    }})

    name: str = Field(description='Full name of the customer')
    email: str = Field(description='Customer email address')
    age: int = Field(gt=0, description='Customer age in years')

    @field_validator('email')
    @classmethod
    def email_must_be_valid(cls, value: str) -> str:
        """Basic email format validation."""
        if '@' not in value or '.' not in value.split('@')[-1]:
            raise InvalidEmailError(f'Invalid email address: {value}')
        return value.lower()

    @model_validator(mode='before')
    @classmethod
    def strip_whitespace(cls, data: dict) -> dict:
        """Normalize input by stripping whitespace from string fields before parsing."""
        if isinstance(data, dict):
            if 'name' in data and isinstance(data['name'], str):
                data['name'] = data['name'].strip()
            if 'email' in data and isinstance(data['email'], str):
                data['email'] = data['email'].strip()
        return data


def main() -> None:
    customer = Customer(name='  Jane Doe  ', email='  JANE@example.com  ', age=30)

    print('--- model_dump() ---')
    print(customer.model_dump())

    print('\n--- model_dump_json(indent=2) ---')
    print(customer.model_dump_json(indent=2))

    print('\n--- model_dump(exclude={"age"}) ---')
    print(customer.model_dump(exclude={'age'}))


if __name__ == '__main__':
    main()
