# Cinema Ticketing System - Code Samples Design

## Purpose

Create a cohesive set of code samples for a 1-day Python bootcamp. All samples use a cinema ticketing system domain to demonstrate: Pydantic v2 (validators, constraints, serialization), context managers, decorators, dunder methods, caching, and unit testing with mockito.

## Package Structure

```
ticketing_system/
├── __init__.py
├── models/
│   ├── __init__.py
│   ├── movie.py          # Movie model
│   ├── customer.py       # Customer model
│   ├── ticket.py         # Ticket model
│   └── booking_request.py # BookingRequest model
├── services/
│   ├── __init__.py
│   ├── database_service.py   # In-memory DB
│   ├── payment_service.py    # Print-based payment
│   └── booking_service.py    # Orchestrator
├── decorators.py         # tenacity usage
├── context_managers.py   # TransactionContext, logging_context
└── cache.py              # lru_cache vs cachetools demos

tests/
├── __init__.py
└── test_booking_service.py   # Mockito-based unit tests

exercises/
├── pydantic_exercise.py          # Fill-in-the-blanks
└── pydantic_exercise_solution.py # Complete solution
```

## Pydantic Models

### Movie (`models/movie.py`)
- Fields: `name` (str), `genre` (Genre enum), `duration_minutes` (int, gt=0), `rating` (float, ge=0, le=10), `release_year` (int), `min_age` (int, ge=0, default=0)
- `field_validator('name')`: reject empty/whitespace-only names
- `model_validator(mode='after')`: validate release_year not more than 1 year in the future
- ConfigDict with example in json_schema_extra

### Customer (`models/customer.py`)
- Fields: `name` (str), `email` (str), `age` (int, gt=0)
- `field_validator('email')`: basic email format validation (contains @)
- `model_validator(mode='before')`: strip whitespace from name and email before parsing
- Demonstrate `model_dump()` and `model_dump_json()`

### Ticket (`models/ticket.py`)
- Fields: `movie` (Movie), `customer` (Customer), `price` (float, gt=0), `purchase_date` (datetime, default_factory=now), `seat_number` (str)
- `model_validator(mode='after')`: validate customer.age >= movie.min_age
- `Field()` with description on each field
- Demonstrate serialization to dict and json

### BookingRequest (`models/booking_request.py`)
- Fields: `customer_email` (str), `movie_name` (str), `num_tickets` (int, gt=0, le=10)
- `Field()` with descriptions for documentation

## Services

### DatabaseService (`services/database_service.py`)
- In-memory implementation using dicts
- Dunder methods: `__init__`, `__str__`, `__repr__`, `__len__`, `__contains__`
- Methods: `save_ticket(ticket)`, `get_tickets_by_customer(email)`, `get_movie_by_name(name)`, `add_movie(movie)`, `get_all_movies()`
- `__len__` returns total tickets stored
- `__contains__` checks if a movie exists by name

### PaymentService (`services/payment_service.py`)
- Methods: `process_payment(customer_name, amount)` -> bool, `refund(ticket_id, amount)` -> bool
- Implementation: prints the action and returns True

### BookingService (`services/booking_service.py`)
- Constructor takes `DatabaseService` and `PaymentService` (dependency injection)
- Method: `book_ticket(request: BookingRequest) -> Ticket`
- Flow: lookup movie -> validate -> process payment -> create ticket -> save -> return
- Uses `TransactionContext` context manager
- Uses `tenacity.retry` on payment call
- Primary target for unit testing

## Decorators (`decorators.py`)

- Tenacity usage example: `@retry(stop=stop_after_attempt(3), wait=wait_fixed(1), retry=retry_if_exception_type(ConnectionError))`

## Context Managers (`context_managers.py`)

- `TransactionContext` — class-based (`__enter__`/`__exit__`), logs transaction start/end, tracks success/failure, demonstrates proper exception handling in `__exit__`
- `logging_context(operation, **metadata)` — function-based with `@contextmanager`, sets up structured logging context with operation name and metadata

## Caching (`cache.py`)

- `get_movie_by_name_cached(db, name)` — `@lru_cache` example with explanation of limitations
- `get_available_movies_cached(db)` — `@cachetools.cached` with `TTLCache(maxsize=100, ttl=300)`, shows time-based expiration
- Helper to demonstrate cache stats and clearing

## Unit Tests (`tests/test_booking_service.py`)

Using `unittest.TestCase` + `mockito`:
- `BookingServiceTest` class
- `test_successful_booking` — mock DB returns movie, mock payment succeeds, assert ticket created
- `test_booking_movie_not_found` — mock DB returns None, assert raises appropriate error
- `test_booking_payment_fails` — mock payment returns False, assert raises appropriate error
- `test_booking_underage_customer` — validate age restriction logic
- All use `expect(..., times=N)` pattern, `# PREPARE/MOCK/ACT/ASSERT` structure

## Exercise (`exercises/pydantic_exercise.py`)

**Theme:** Create a `MoviePromotion` model for a cinema discount system.

**What participants fill in (marked with TODO comments):**
1. Add a `field_validator` for `discount_percent` (must be 0-100)
2. Add a `model_validator(mode='before')` to normalize the promo_code to uppercase
3. Add a `model_validator(mode='after')` to compute `final_price` from `base_price` and `discount_percent`
4. Add field constraints on `base_price` (gt=0) and `max_uses` (gt=0)
5. Dump the model to dict and json (in a `if __name__ == '__main__'` block)

**Solution:** Complete working implementation in `pydantic_exercise_solution.py`.

## Dependencies to Add

- `tenacity` — for retry decorator demonstrations

## Verification

1. `poetry install` succeeds
2. `poetry run pytest -v` — all tests pass
3. `python -m ticketing_system.models.movie` — model creation and serialization works
4. `python exercises/pydantic_exercise_solution.py` — exercise solution runs correctly
5. Each module can be imported independently for live demo during the course
