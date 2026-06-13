# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Important Instructions

1. **Understand first** - Thoroughly read the problem and investigate relevant files before acting
2. **Verify major changes** - Check in before making significant modifications
3. **Explain changes** - Provide high-level explanations at each step
4. **Prioritize simplicity** - Make changes as simple as possible, impacting minimal code
5. **Never speculate** - Always read files before making claims about code; if the user references a file, you MUST read it first
6. **Use todo lists** - Track progress on complex tasks to stay organized

## Project

Python bootcamp course materials covering: comprehensions, type hints, Pydantic, context managers, decorators, dunder methods, caching (`lru_cache` / `cachetools`), and testing with `pytest` + `mockito`. See `course-agenda.md` for the full schedule.

## Package Source

Dependencies are pulled from CyberArk's JFrog Artifactory. Ensure you have access to `https://cyberark.jfrog.io/artifactory/api/pypi/pas-pypi-virtual/simple` before installing.

## Commands

```bash
# Install dependencies
poetry install

# Run all tests
poetry run pytest -v

# Run a single test file
poetry run pytest path/to/test_file.py

# Run a single test by name
poetry run pytest -k "test_name"
```

### Linting & Static Analysis
```bash
cybr pylint            # Run pylint
cybr pyre              # Run pyre type checker
cybr yapf check-diff   # Check code formatting
cybr pre-commit        # Run pre-commit hooks
cybr sort              # Run isort import sorting
```

## Code Style

- **Python 3.13**, managed with Poetry
- **Imports**: Top-level only — never inside functions or `if __name__ == '__main__'` blocks; absolute imports, sorted with `cybr sort`
- **Type hints**: Required on all function signatures. Use `T | None` (not `Optional[T]`), lowercase `dict`/`list`/`set`
- **Docstrings**: Google Style with `Args:`/`Returns:`/`Raises:` sections
- **String quotes**: Single quotes (`'text'`) not double quotes
- **Pydantic**: Use `model_validator` (v2), `ConfigDict`, `Field()` for descriptions

## Testing Conventions

- **Framework**: `unittest.TestCase` (NOT pytest test functions)
- **File naming**: `test_*.py`
- **Class naming**: `*Test` (e.g., `CacheTest`)
- **Method naming**: `test_*`
- **Test structure**: Use PREPARE/MOCK/ACT/ASSERT comments with descriptive docstrings
- **Docstring format**: Use Given/When/Then style for test docstrings
- **Assertions**: Use `assert expected == actual` not `self.assertEqual()`
- **Static methods**: Use `@staticmethod` for test methods that don't use `self`

**Mocking Rules (NON-NEGOTIABLE):**
- **Always use `expect(..., times=N)`** - never `when()` or `verify()`
- **Always call `verifyExpectedInteractions()`** after `expect()` - ensures all interactions are expected
- **NEVER use `unittest.mock`** - no `patch`, `Mock`, or `MagicMock`
- **Match parameter style** - if code uses named params, mock must too
- **Always include `times` parameter** in every expectation
- **Specify exact function parameters** in expectations whenever possible

Example test:
```python
def test_example(self) -> None:
    """
    Given: A valid input and a mocked dependency
    When: function_under_test is called
    Then: It returns the expected result
    """
    # PREPARE
    mock_obj = mock()

    # MOCK
    expect(mock_obj, times=1).method('param').thenReturn('value')

    # ACT
    result = function_under_test(mock_obj)

    # ASSERT
    assert result == 'expected'
    verifyExpectedInteractions()

@staticmethod
def test_without_self() -> None:
    """
    Given: A plain input value
    When: pure_function is called
    Then: It returns the expected result
    """
    # PREPARE
    value = 'test'

    # ACT
    result = pure_function(value)

    # ASSERT
    assert result == 'expected'
```

## Architecture

- **`pydantic` v2** for data validation and settings
- **`cachetools`** for caching utilities (alongside stdlib `functools.lru_cache`)
- **`tenacity`** for retry decorators (see `ticketing_system/decorators.py`)
- **`mockito`** for test mocking (not `unittest.mock`)
- **`infra-logging-cyberark`** for structured logging
- Code samples are organized as self-contained modules per topic

## Directory Structure

```
ticketing_system/       # Demo domain (cinema booking) — primary teaching reference
  models/               # Pydantic models: Movie, Customer, Ticket, BookingRequest
  services/             # Service layer: BookingService, MoviesService, DatabaseService, PaymentService
  *.py                  # Standalone topic demos: cache.py, comprehensions.py, decorators.py, etc.
exercises/              # Fill-in-the-blank exercises; each topic has exercise_*.py + exercise_*_solution.py
tests/unit/             # Unit tests using mockito; mirrors services in ticketing_system/
```

## Key Conventions

- **Singleton services**: Each service class is underscore-prefixed (`_BookingService`) with a public
  module-level instance (`booking_service`). Never instantiate directly.
- **Setter DI for tests**: Services expose `set_db()`, `set_payment()`, `set_movies()` for injecting
  mocks. Always reset with `unstub()` in `tearDown`.
- **Exercises**: Stubs have `# TODO` + `pass` bodies; solutions use `assert` statements in `main()`.
  Exercises do not import from `ticketing_system` — they use the cinema domain thematically only.
