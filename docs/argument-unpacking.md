# Argument Unpacking in Python

Using `*` and `**` operators to unpack arguments at call sites, pass through
in decorators, and merge dictionaries.

---

## 1. Argument Unpacking at Call Sites

Use `*` to unpack a sequence and `**` to unpack a dict into function arguments:

```python
def print_vector(x: int, y: int, z: int) -> None:
    print(f'<{x}, {y}, {z}>')

# Unpack a tuple with *
tuple_vector = (1, 0, 1)
list_vector = [1, 2, 3]
range_vector = range(1, 4)
print_vector(*tuple_vector)  # <1, 0, 1>
print_vector(*list_vector)  # <1, 2, 3>
print_vector(*range_vector)        # <1, 2, 3>

```

Practical example — calling a function with pre-packaged args:

```python
def book_ticket(movie: str, seat: str, customer: str, vip: bool = False) -> dict:
    return {'movie': movie, 'seat': seat, 'customer': customer, 'vip': vip}

positional_args = ('The Matrix', 'B7')
keyword_args = {'customer': 'Neo', 'vip': True}

booking = book_ticket(*positional_args, **keyword_args)
# {'movie': 'The Matrix', 'seat': 'B7', 'customer': 'Neo', 'vip': True}
```

---

## 2. `*args`/`**kwargs` in Decorators

Decorators accept arbitrary arguments to pass through to the wrapped function:

```python
import functools

def log_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f'Calling {func.__name__} with args={args} kwargs={kwargs}')
        result = func(*args, **kwargs)
        print(f'Result: {result}')
        return result
    return wrapper

@log_call
def add_tickets(a: int, b: int) -> int:
    return a + b

add_tickets(3, 5)
# Calling add_tickets with args=(3, 5) kwargs={}
# Result: 8
```

`functools.wraps` preserves the original function's `__name__` and `__doc__`.

---

## 3. Dict Merging with `**` Unpacking

Use `**` inside a dict literal to merge dictionaries (later keys override earlier):

```python
base = {'name': 'Alice', 'email': 'alice@old.com', 'tier': 'silver'}
update = {'email': 'alice@new.com', 'tier': 'gold'}

merged = {**base, **update}
# {'name': 'Alice', 'email': 'alice@new.com', 'tier': 'gold'}
```

Merging variadic dicts:

```python
def merge_profiles(*profiles: dict) -> dict:
    merged = {}
    for profile in profiles:
        merged = {**merged, **profile}
    return merged
```

---

## Quick Reference

| Syntax | Position | Effect |
|--------|----------|--------|
| `*iterable` | At call site | Unpacks sequence into positional args |
| `**mapping` | At call site | Unpacks dict into keyword args |
| `*args`/`**kwargs` | In wrapper | Captures args for pass-through |
| `{**d1, **d2}` | In dict literal | Merges dicts (right wins) |
