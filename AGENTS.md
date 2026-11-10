# Project Guidelines

## Project structure

- `decoimpact/business/` contains the application and model workflow; `decoimpact/data/` handles input/output and parsing; `decoimpact/crosscutting/` contains shared services such as logging.
- Preserve the layered architecture and use the existing interfaces, factories, and builders. See [docs/api/application_overview.md](docs/api/application_overview.md) and [docs/api/architecture.md](docs/api/architecture.md).
- Keep tests alongside the corresponding area under `tests/`. End-to-end command-line acceptance tests and their input/reference data live under `tests_acceptance/`.

## Python conventions

- Follow PEP 8, use type hints where practical, avoid global state, and keep imports and public interfaces limited to what is needed.
- Add docstrings to public classes and methods.
- Format with Black and keep imports compatible with the project's isort Black profile (88-character line length).
- Manage dependencies with `uv`; update `pyproject.toml` and `uv.lock` through `uv add` or `uv add --dev`, not by editing dependency versions independently.

## Testing and validation

- Restore the environment with `uv sync`.
- Run unit tests with `uv run pytest tests`.
- Run command-line acceptance tests with `uv run pytest tests_acceptance`.
- For changes affecting both layers, run both test commands. Add or update tests for behavior changes; acceptance test inputs and expected NetCDF files should follow the conventions in [README.md](README.md).

## Documentation

- Update the relevant `docs/` pages when changing documented behavior, input formats, or user-facing workflows.
- Follow the development workflow and review agreements in [docs/development.md](docs/development.md).
