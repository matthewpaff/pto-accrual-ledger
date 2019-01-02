# PTO Accrual Ledger

Calculate a bounded date-only monthly PTO ledger using integer minutes and explicit usage.

Uses Python 3.10+ and its standard library only. No package installation, virtual
environment, external server, Redis, Celery, or network access is required.

## Run

```console
python -m pto_ledger --help
python -m pto_ledger examples/sample.json
python -m pto_ledger --check-fixtures fixtures/cases.jsonl
python generate_fixtures.py --count 20
python -m unittest discover -s tests -v
```

Run from this directory. The optional path defaults to `-`, which reads JSON from
stdin. Output is JSON or a fixture-check summary. Exit codes are 0 success,
1 file failure, and 2 invalid input. Examples and fixtures contain generated data.

Requires start_month (YYYY-MM-01, years 2000–2090), opening_minutes, earn_minutes, cap_minutes, and used_minutes (up to 36 monthly nonnegative integers). Each month credits accrual up to the cap, then subtracts that month's usage; overspending fails. Opening balance cannot exceed cap. Output gives each calendar month and earned, used, and closing minutes. No proration, employment policy, jurisdiction rules, timezone arithmetic, persistence, or payroll integration is implemented.

## Learning focus

The modeled 2019 calendar arithmetic and time-off balance learning themes. This is an independent concept exercise based on the modeled
roadmap. It makes no claim to be employer-owned or period-authentic production code.

## Structure

- `pto_ledger/core.py`: validated parsing, storage, or state transitions.
- `pto_ledger/cli.py`: JSON command interface.
- `pto_ledger/generate_fixtures.py`: original deterministic validation cases.
- `pto_ledger/fixture_check.py`: expected-output/error checks.
- `fixtures/cases.jsonl`: 587 generated cases, with explicit descriptions.
- `tests/`: independently selected boundaries and the complete corpus check.

Branches `feature/core`, `feature/cli`, `data/fixtures`, and `docs/usage` retain
snapshots; `main` contains the complete tool. Dates and provenance are also recorded
in TIMELINE.json. Many data cases share a scenario; they are not separate features.

Keep changes focused, use actual dates for new work, and add a regression test
for changed behavior. Licensed under [MIT](LICENSE).

[History and provenance](HISTORY.md).
