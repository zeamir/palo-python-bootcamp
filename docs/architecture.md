# Ticketing System Architecture

Visual reference for the cinema ticket booking demo used throughout the Python bootcamp.

---

## 1. Service Architecture

How the service layer is structured and how dependencies flow at runtime vs. in tests.

```mermaid
graph LR
    Client["Client<br/>(BookingRequest DTO)"]

    subgraph Orchestration
        BS["BookingService<br/>(booking_service)"]
    end

    subgraph Domain
        MS["MoviesService<br/>(movies_service)"]
        Cache["TTLCache<br/>(5-min in-memory)"]
    end

    subgraph Infrastructure
        DB["DatabaseService<br/>(database_service)"]
        PS["PaymentService<br/>(payment_service)"]
    end

    Client -->|book_ticket| BS
    BS -->|get_movie_by_name| MS
    BS -->|save_ticket| DB
    BS -->|process_payment| PS
    MS -->|cache miss| DB
    MS -->|read/write| Cache

    style Cache fill:#fffbe6,stroke:#d4a017
    style BS fill:#e8f0fe,stroke:#4a86e8
    style MS fill:#e8f0fe,stroke:#4a86e8
    style DB fill:#e8f0fe,stroke:#4a86e8
    style PS fill:#e8f0fe,stroke:#4a86e8
```

> **Singleton pattern**: Each service class is underscore-prefixed (`_BookingService`) with a public
> module-level instance (`booking_service`). Never instantiate directly.
>
> **Setter DI for tests**: `booking_service.set_movies(mock)`, `.set_db(mock)`, `.set_payment(mock)`
> allow injecting test doubles. Reset with `unstub()` in `tearDown`.

---

## 2. Booking Flow

Step-by-step sequence of `BookingService.book_ticket()`, including all error paths.

```mermaid
sequenceDiagram
    participant C as Client
    participant BS as BookingService
    participant MS as MoviesService
    participant DB as DatabaseService
    participant PS as PaymentService

    C->>BS: book_ticket(request)

    BS->>MS: get_movie_by_name(movie_name)
    MS-->>BS: Movie | None

    alt Movie not found
        BS-->>C: raise ValueError("Movie not found")
    end

    BS->>BS: check customer_age >= movie.min_age

    alt Customer underage
        BS-->>C: raise ValueError("minimum age requirement")
    end

    BS->>BS: total_price = $15.00 × num_tickets
    BS->>PS: process_payment(customer_name, total_price)
    PS-->>BS: True | False

    alt Payment failed
        BS-->>C: raise RuntimeError("Payment failed")
    end

    BS->>BS: Ticket(...) — Pydantic validates all fields including min_age constraint
    BS->>DB: save_ticket(ticket)
    BS-->>C: return Ticket
```

> **Note on MoviesService cache**: On a cache hit, `MoviesService` returns the movie directly
> without calling `DatabaseService`. On a cache miss it fetches from DB and caches the result
> for 5 minutes (TTLCache).

---

## 3. Model Relationships

Pydantic models used across the system and how they compose.

```mermaid
classDiagram
    class BookingRequest {
        +str customer_name
        +str customer_email
        +int customer_age
        +str movie_name
        +int num_tickets
        +str seat_number
        <<DTO — input only>>
    }

    class Customer {
        +str name
        +str email
        +int age
        +field_validator: email format
        +model_validator: strip whitespace
    }

    class Genre {
        <<Enum>>
        ACTION
        COMEDY
        DRAMA
        HORROR
        SCI_FI
    }

    class Movie {
        +str name
        +Genre genre
        +int duration_minutes
        +float rating
        +int release_year
        +int min_age
        +field_validator: name not blank
        +model_validator: release_year not future
    }

    class Ticket {
        +str id
        +Movie movie
        +Customer customer
        +float price
        +datetime purchase_date
        +str seat_number
        +model_validator: customer_age >= movie.min_age
        <<frozen — immutable>>
    }

    Movie --> Genre : genre
    Ticket --> Movie : movie
    Ticket --> Customer : customer
    BookingRequest ..> Customer : creates
    BookingRequest ..> Ticket : produces (via BookingService)
```
