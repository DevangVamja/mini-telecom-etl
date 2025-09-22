# Contributing

Thanks for considering a contribution!

## Dev setup
1. Create a venv and install your preferred versions of Airflow, dbt, and Great Expectations.
2. Copy `.env.example` to `.env` and set any needed variables.
3. (Optional) Use `docker-compose up` to spin up a local Airflow UI on http://localhost:8080.

## Code style
- Keep the repo cloud-agnostic and production-focused.
- Prefer small, composable scripts and clear task boundaries.
- Include tests for idempotency, edge cases (late/duplicate events), and schema evolution.

## Pull requests
- Include a diagram or short description in the PR body when you change the data flow.
- Add/adjust README sections if behavior or commands change.
