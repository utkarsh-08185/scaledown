# Contributing to ScaleDown

Thanks for your interest in contributing to **ScaleDown**.

## Development setup

1. Fork and clone the repository.
2. Create and activate a virtual environment.
3. Install project dependencies.

```bash
git clone https://github.com/scaledown-team/scaledown.git
cd scaledown
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -e ".[haste,semantic]"
```

## Running checks locally

Run tests:

```bash
pytest -q
```

If you are modifying optional optimizers, ensure related extras are installed before testing.

## Branching and pull requests

- Create a focused branch for each change.
- Keep commits small and descriptive.
- Include tests for behavior changes when possible.
- Open a pull request with:
  - clear summary,
  - testing evidence,
  - any migration notes (if applicable).

## Code style

- Follow existing Python style and naming conventions.
- Prefer small, composable functions.
- Keep public interfaces backward-compatible when possible.
- Update docs/examples when behavior changes.

## Reporting issues

Please use GitHub Issues and provide:

- expected vs actual behavior,
- reproducible steps,
- environment details (OS, Python version, package version).

Thanks for helping improve ScaleDown.
