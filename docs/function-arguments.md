# Function Arguments in Python

A guide to Python's function argument mechanics — keyword-only, positional-only,
`*args`, `**kwargs`, and argument unpacking.

---

## The Basics: `*args` and `**kwargs`

```python
def foo(required, *args, **kwargs):
    print(required)
    if args:
        print(args)
    if kwargs:
        print(kwargs)
```

This function requires one argument but accepts any extras: `*args` collects additional
positional arguments as a **tuple**, `**kwargs` collects additional keyword arguments as a
**dictionary**. Both are empty if no extras are passed.

```python
>>> foo()
TypeError: "foo() missing 1 required positional arg: 'required'"

>>> foo('hello')
hello

>>> foo('hello', 1, 2, 3)
hello
(1, 2, 3)

>>> foo('hello', 1, 2, 3, key1='value', key2=999)
hello
(1, 2, 3)
{'key1': 'value', 'key2': 999}
```

The names `args` and `kwargs` are just convention — `*parms` and `**argv` would work identically.
The actual syntax is the `*` / `**` prefix. Stick with the convention for clarity.

---

## 1. Keyword-Only Arguments (`*` separator)

Place a bare `*` in the signature. Everything **after** it must be passed by name:

```python
def format_ticket(*, movie: str, seat: str, price: float) -> str:
    return f'Ticket: {movie} | Seat {seat} | ${price:.2f}'

# Valid
format_ticket(movie='Inception', seat='A12', price=15.0)

# Invalid — all params are keyword-only
format_ticket('Inception', 'A12', 15.0)  # TypeError!
```

---

## 2. The `*` Separator Nuance

Parameters **before** `*` can be passed positionally *or* by name.
Only parameters **after** `*` are forced keyword-only:

```python
def book_ticket(customer_name: str, *, movie: str, seat: str) -> str:
    return f'{customer_name} booked {seat} for {movie}'

# Valid — customer_name positionally, movie/seat by name
book_ticket('Alice', movie='Inception', seat='A1')

# Also valid — customer_name by name (it's before *, so either works)
book_ticket(customer_name='Alice', movie='Inception', seat='A1')

# Invalid — movie and seat cannot be positional (they're after *)
book_ticket('Alice', 'Inception', 'A1')  # TypeError!
```

Key insight: `*` doesn't make preceding params positional-only — it only makes
following params keyword-only.

---

## 3. Positional-Only Arguments (`/` separator)

Place `/` in the signature. Everything **before** it must be passed positionally:

```python
def process_booking(booking_id: int, /, *ticket_ids: str, customer_email: str) -> dict:
    return {
        'booking_id': booking_id,
        'customer_email': customer_email,
        'ticket_ids': list(ticket_ids),
    }

# Valid
process_booking(101, 'TKT-001', 'TKT-002', customer_email='bob@example.com')

# Invalid — booking_id cannot be passed by name
process_booking(booking_id=101, customer_email='bob@example.com')  # TypeError!
```

---

## 4. `*args` — Variable Positional Arguments

Collects any number of extra positional arguments into a **tuple**:

```python
def calculate_group_total(*prices: float) -> float:
    total = sum(prices)
    discount = total * 0.10
    return total - discount

calculate_group_total(15.0, 15.0, 12.0)  # 37.80
calculate_group_total(20.0)              # 18.0
calculate_group_total()                  # 0.0
```

---

## 5. `**kwargs` — Variable Keyword Arguments

Collects any number of extra keyword arguments into a **dict**:

```python
def create_event(title: str, **details: str | int) -> dict:
    return {'title': title, **details}

create_event('Star Wars Marathon', venue='Theater 3', time='7pm', duration=420)
# {'title': 'Star Wars Marathon', 'venue': 'Theater 3', 'time': '7pm', 'duration': 420}
```

---

## 6. Combining All Argument Types

The full ordering: positional-only `/` regular `*args` keyword-only `**kwargs`

```python
def process_booking(
    booking_id: int, /,        # positional-only
    *ticket_ids: str,          # variable positional
    customer_email: str,       # keyword-only (after *args)
    **metadata: str | int,     # variable keyword
) -> dict:
    return {
        'booking_id': booking_id,
        'customer_email': customer_email,
        'ticket_ids': list(ticket_ids),
        'metadata': metadata,
    }

process_booking(102, 'TKT-001', 'TKT-002',
                customer_email='bob@example.com',
                payment_method='credit_card', total=42)
```

---

## See Also

For argument unpacking at call sites, `*args`/`**kwargs` in decorators, and dict
merging with `**` — see [argument-unpacking.md](argument-unpacking.md).

---

## Quick Reference

| Syntax | Position | Effect |
|--------|----------|--------|
| `*` (bare) | In signature | Params after are keyword-only |
| `/` | In signature | Params before are positional-only |
| `*args` | In signature | Collects extra positional args as tuple |
| `**kwargs` | In signature | Collects extra keyword args as dict |
