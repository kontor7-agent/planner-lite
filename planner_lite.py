#!/usr/bin/env python3
"""planner-lite: make a printable one-page Daily Planner and Weekly Overview as PDF.

Offline only (no network). Dry-run by default: nothing is written unless you pass --write.
It only ever creates ONE new file inside the output folder and never overwrites or deletes
anything unless you explicitly pass --force (overwrite of that same file only).
"""
import argparse
import datetime as dt
import sys
from pathlib import Path

try:
    from reportlab.lib.colors import HexColor, white
    from reportlab.lib.pagesizes import A4, letter
    from reportlab.lib.units import mm
    from reportlab.pdfgen import canvas
except ImportError:
    sys.exit("This tool needs reportlab:  python -m pip install reportlab")

INK = HexColor("#2B3440")
ACC = HexColor("#4F7A6A")
SOFT = HexColor("#E8EFEA")
LINE = HexColor("#B9C2BD")
GREY = HexColor("#7A858D")
WARM = HexColor("#F6F3EC")
M = 15 * mm
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
FOOT = "planner-lite  |  MIT licence  |  free version"


def header(c, W, H, title, sub):
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(M, H - M - 6 * mm, title)
    c.setFillColor(GREY)
    c.setFont("Helvetica", 9)
    c.drawString(M, H - M - 11 * mm, sub)
    c.setStrokeColor(ACC)
    c.setLineWidth(1.4)
    c.line(M, H - M - 14 * mm, W - M, H - M - 14 * mm)
    c.setFont("Helvetica", 7)
    c.drawCentredString(W / 2, 8 * mm, FOOT)


def rule(c, x1, x2, y, col=LINE, w=0.6):
    c.setStrokeColor(col)
    c.setLineWidth(w)
    c.line(x1, y, x2, y)


def section(c, x, y, text):
    c.setFillColor(ACC)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(x, y, text.upper())


def field(c, x, y, w, label, value=""):
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(x, y, label)
    lw = c.stringWidth(label, "Helvetica-Bold", 9) + 3 * mm
    rule(c, x + lw, x + w, y - 1)
    if value:
        c.setFont("Helvetica", 10)
        c.drawString(x + lw + 1 * mm, y + 0.5, value)


def checkbox(c, x, y, s=3.8 * mm):
    c.setStrokeColor(GREY)
    c.setLineWidth(0.8)
    c.setFillColor(white)
    c.roundRect(x, y, s, s, 0.8 * mm, stroke=1, fill=1)


def ruled(c, x, w, ytop, ybot, gap=8 * mm):
    y = ytop - gap
    while y >= ybot - 0.1:
        rule(c, x, x + w, y)
        y -= gap


def box(c, x, y, w, h, fill=None, r=2 * mm):
    c.setStrokeColor(LINE)
    c.setLineWidth(0.8)
    if fill:
        c.setFillColor(fill)
    c.roundRect(x, y, w, h, r, stroke=1, fill=1 if fill else 0)


def page_daily(c, W, H, date=None):
    header(c, W, H, "Daily Planner", "Three priorities. A few blocks. One win.")
    cw = W - 2 * M
    y = H - M - 22 * mm
    label = date.strftime("%A %d %B %Y") if date else ""
    field(c, M, y, cw, "Date", label)
    y -= 9 * mm
    section(c, M, y, "Top 3: what would make today a good day?")
    y -= 3 * mm
    for i in range(3):
        cy = y - 6.5 * mm
        c.setFillColor(ACC)
        c.circle(M + 5 * mm, cy, 4.2 * mm, stroke=0, fill=1)
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(M + 5 * mm, cy - 4, str(i + 1))
        rule(c, M + 13 * mm, M + cw, y - 10 * mm)
        y -= 13 * mm
    y -= 5 * mm
    yb = M + 24 * mm
    lw = cw * 0.57
    rx = M + lw + 6 * mm
    rw = cw - lw - 6 * mm
    section(c, M, y, "Time blocks")
    ytop = y - 3 * mm
    hours = list(range(7, 22))
    rh = (ytop - yb) / len(hours)
    for i, hh in enumerate(hours):
        yy = ytop - i * rh
        c.setFont("Helvetica", 8)
        c.setFillColor(GREY)
        c.drawString(M, yy - rh + 1.6 * mm, f"{hh:02d}:00")
        rule(c, M, M + lw, yy - rh)
    c.setStrokeColor(LINE)
    c.setLineWidth(0.6)
    c.line(M + 11 * mm, ytop, M + 11 * mm, yb)
    section(c, rx, y, "Small tasks")
    yy = y - 3 * mm
    for _ in range(7):
        checkbox(c, rx, yy - 7 * mm + 1.2 * mm)
        rule(c, rx + 6 * mm, rx + rw, yy - 7 * mm)
        yy -= 8 * mm
    yy -= 4 * mm
    section(c, rx, yy, "Notes")
    ruled(c, rx, rw, yy - 1 * mm, yb, 8 * mm)
    field(c, M, M + 14 * mm, cw, "One win today:")
    field(c, M, M + 6 * mm, cw, "First step for tomorrow:")
    c.showPage()


def page_week(c, W, H, wk, monday=None):
    header(c, W, H, "Weekly Overview", "See the whole week. Protect what matters.")
    cw = W - 2 * M
    y = H - M - 22 * mm
    field(c, M, y, cw * 0.5, "Week of", monday.isoformat() if monday else "")
    y -= 7 * mm
    box(c, M, y - 20 * mm, cw, 20 * mm, SOFT)
    section(c, M + 3 * mm, y - 5 * mm, "Focus of the week (one sentence)")
    rule(c, M + 3 * mm, M + cw - 3 * mm, y - 14 * mm)
    y -= 26 * mm
    yb = M + 28 * mm
    days = DAYS[wk:] + DAYS[:wk]
    rh = (y - yb) / 7
    for i, d in enumerate(days):
        yy = y - i * rh
        weekend = d in ("Saturday", "Sunday")
        box(c, M, yy - rh, 26 * mm, rh, WARM if weekend else SOFT, r=0.1)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(M + 3 * mm, yy - 6 * mm, d)
        c.setFont("Helvetica", 7.5)
        c.setFillColor(GREY)
        if monday:
            offset = (DAYS.index(d) - monday.weekday()) % 7
            c.drawString(M + 3 * mm, yy - 11 * mm, (monday + dt.timedelta(days=offset)).isoformat())
        else:
            c.drawString(M + 3 * mm, yy - 11 * mm, "date: ____")
        box(c, M + 26 * mm, yy - rh, cw - 26 * mm, rh, None, r=0.1)
        rule(c, M + 30 * mm, M + cw - 4 * mm, yy - rh * 0.5)
        rule(c, M + 30 * mm, M + cw - 4 * mm, yy - rh * 0.8)
    section(c, M, yb - 6 * mm, "Fixed appointments")
    section(c, M + cw / 2 + 3 * mm, yb - 6 * mm, "Don't forget")
    ruled(c, M, cw / 2 - 3 * mm, yb - 6 * mm, M + 12 * mm, 7 * mm)
    ruled(c, M + cw / 2 + 3 * mm, cw / 2 - 3 * mm, yb - 6 * mm, M + 12 * mm, 7 * mm)
    c.showPage()


def parse_date(s):
    try:
        return dt.date.fromisoformat(s)
    except ValueError:
        raise argparse.ArgumentTypeError("use YYYY-MM-DD, e.g. 2027-01-04")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Make a printable Daily Planner + Weekly Overview PDF (offline).")
    ap.add_argument("--out", default=".", help="output folder (must exist; default: current folder)")
    ap.add_argument("--paper", choices=["a4", "letter"], default="a4")
    ap.add_argument("--week-start", choices=["monday", "sunday"], default="monday")
    ap.add_argument("--start-date", type=parse_date, help="optional first date; daily pages get dated, "
                    "the weekly page shows that week's dates")
    ap.add_argument("--days", type=int, default=5, help="number of daily pages (1-31, default 5)")
    ap.add_argument("--write", action="store_true", help="actually write the PDF (default is dry-run)")
    ap.add_argument("--force", action="store_true", help="allow overwriting the same output file")
    a = ap.parse_args(argv)

    if not 1 <= a.days <= 31:
        ap.error("--days must be between 1 and 31")
    out = Path(a.out)
    if not out.is_dir():
        sys.exit(f"Output folder does not exist: {out}")
    name = f"planner-lite_{a.paper}_{a.week_start}"
    if a.start_date:
        name += f"_{a.start_date.isoformat()}"
    target = out / f"{name}.pdf"
    pages = a.days + 1
    print(f"Plan: {a.days} daily page(s) + 1 weekly overview = {pages} page(s), {a.paper.upper()}")
    print(f"Target: {target.resolve()}")
    if not a.write:
        print("Dry-run: nothing written. Add --write to create the PDF.")
        return 0
    if target.exists() and not a.force:
        sys.exit("Target exists. Use --force to overwrite this one file, or choose another --out folder.")

    size = A4 if a.paper == "a4" else letter
    W, H = size
    wk = 0 if a.week_start == "monday" else 6
    monday = None
    if a.start_date:
        # first day of the week that contains start-date
        shift = (a.start_date.weekday() - wk) % 7
        monday = a.start_date - dt.timedelta(days=shift)
    c = canvas.Canvas(str(target), pagesize=size)
    c.setTitle("planner-lite")
    c.setAuthor("Blixwerk")
    page_week(c, W, H, wk, monday)
    for i in range(a.days):
        page_daily(c, W, H, a.start_date + dt.timedelta(days=i) if a.start_date else None)
    c.save()
    print(f"Written: {target}")
    print("Print at 100% / 'Actual size', not 'Fit to page'.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
