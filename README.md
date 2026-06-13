# Python Bootcamp

1-day Python bootcamp course materials for CyberArk. All code samples use a **cinema ticketing
system** as a shared domain to teach modern Python patterns.

## Topics Covered

- **Core Python** — comprehensions, function arguments, mutable default pitfalls
- **Type hints & Pydantic v2** — validators, field constraints, serialization
- **Advanced patterns** — context managers, decorators, dunder methods
- **Caching** — `functools.lru_cache` vs `cachetools.TTLCache`
- **Testing** — `unittest.TestCase` with `mockito` (no `unittest.mock`)

## Project Structure

```
ticketing_system/   # Core code samples (models, services, caching, decorators)
exercises/          # Fill-in-the-blank exercises + complete solutions
tests/              # Unit tests (mockito-based)
course-agenda.md    # Full day schedule with timings
```

## Setup

> Requires access to CyberArk's JFrog Artifactory: `https://cyberark.jfrog.io/artifactory/api/pypi/pas-pypi-virtual/simple`

```bash
grep -qxF 'export PIPENV_VENV_IN_PROJECT=true' ~/.zshrc || echo 'export PIPENV_VENV_IN_PROJECT=true' >> ~/.zshrc && source ~/.zshrc
poetry install
```

## Running

```bash
# Run all tests
poetry run pytest -v

# Run a specific exercise solution
poetry run python exercises/exercise_comprehensions_solution.py
```
