# planner-lite

**Generate a calm, printable one-page daily planner and weekly overview as a PDF, with one command and no network.**

## What it does

`planner_lite.py` creates a single PDF containing:

- **1 Weekly Overview page**: focus of the week, seven day rows, fixed appointments, "don't forget".
- **1 to 31 Daily Planner pages**: top 3 priorities, hourly time blocks 07:00-21:00, small tasks with tick boxes, notes, one win, first step for tomorrow.

Options: A4 or US Letter, Monday or Sunday week start, and an optional start date that pre-fills the dates.

Safe by design: it is **dry-run by default**, never touches the network, writes at most one new PDF into the folder you name, and never overwrites anything unless you add `--force` (and then only that one file).

## Quick start

```bash
python -m pip install reportlab

# 1. Preview what would happen (writes nothing)
python planner_lite.py --out . --paper a4 --start-date 2027-01-04 --days 5

# 2. Create the PDF
python planner_lite.py --out . --paper a4 --start-date 2027-01-04 --days 5 --write
```

Result: `planner-lite_a4_monday_2027-01-04.pdf`. Print at 100% ("Actual size"), not "Fit to page".

Leave out `--start-date` for blank dates you write by hand. Use `--paper letter` and `--week-start sunday` as needed.

## Requirements

- Python 3.9+
- `reportlab` (`pip install reportlab`)
- Any printer, or just use the PDF on a tablet

## Licence

MIT, see `LICENSE`.

Created with AI assistance by an automated system.

## Full version

This free tool makes two page types. The full **Printable Daily & Weekly Planner Bundle** is ready-made, with no Python needed, and adds:

- Ready-to-print PDFs for A4 and US Letter, Monday and Sunday start (4 planners, 20 pages each)
- Start-here page, weekly review, blank monthly calendar, brain dump with a sorting step
- Habit tracker (12 habits x 31 days) and project planner
- Dated monthly calendars for all of 2027
- Print instructions and a cover-to-cover consistent design

Get it here: https://kontor7-agent.github.io/p/adhd-friendly-planner-printable-pdf?s=github
