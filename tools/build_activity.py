#!/usr/bin/env python3
"""Draws the activity card of the README from live GitHub data: the last 30
days of contributions as one bar per day, the totals behind them, and the
open-source totals so far. Writes activity-dark.svg and
activity-light.svg.

Usage: GITHUB_TOKEN=... PROFILE_USER=... python3 tools/build_activity.py <output dir>
Without PROFILE_USER the card is drawn for the owner of the repository.
"""
import json
import os
import sys
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from build_hero import SANS, THEMES

WIDTH, HEIGHT = 1200, 400
DAYS = 30
# One hue for the one series, stepped per surface so that it reads on both.
BAR = {"dark": "#9d7ae0", "light": "#8839ef"}
PLOT_LEFT, PLOT_RIGHT, PLOT_TOP, PLOT_BASE = 478, 1156, 70, 262
BAR_WIDTH = 16
DOT = "·"

QUERY = """
query($login: String!, $from: DateTime!, $to: DateTime!, $merged: String!, $reviewed: String!) {
  user(login: $login) {
    month: contributionsCollection(from: $from, to: $to) {
      totalCommitContributions
      totalPullRequestContributions
      totalPullRequestReviewContributions
      totalIssueContributions
      restrictedContributionsCount
      contributionCalendar { weeks { contributionDays { date contributionCount } } }
    }
    year: contributionsCollection {
      contributionCalendar { weeks { contributionDays { date contributionCount } } }
    }
  }
  merged: search(query: $merged, type: ISSUE) { issueCount }
  reviewed: search(query: $reviewed, type: ISSUE) { issueCount }
}
"""


def fetch(login: str, token: str, today: date) -> dict:
    start = datetime.combine(today - timedelta(days=DAYS - 1), datetime.min.time(), timezone.utc)
    variables = {
        "login": login,
        "from": start.isoformat().replace("+00:00", "Z"),
        "to": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "merged": f"author:{login} type:pr is:merged is:public",
        "reviewed": f"reviewed-by:{login} -author:{login} type:pr is:public",
    }
    request = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {token}", "User-Agent": "profile-activity-card"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        answer = json.load(response)
    if answer.get("errors") or not answer.get("data", {}).get("user"):
        raise SystemExit(f"GitHub did not answer the query: {answer.get('errors')}")
    return answer["data"]


def daily_counts(calendar: dict) -> dict:
    return {
        date.fromisoformat(day["date"]): day["contributionCount"]
        for week in calendar["weeks"]
        for day in week["contributionDays"]
    }


def weeks_in_a_row(calendar: dict) -> int:
    """How many weeks in a row, up to this one, had a contribution. A week that
    has only begun and is still empty does not break the row."""
    totals = [sum(day["contributionCount"] for day in week["contributionDays"]) for week in calendar["weeks"]]
    if totals and totals[-1] == 0:
        totals.pop()
    streak = 0
    for total in reversed(totals):
        if total == 0:
            break
        streak += 1
    return streak


def nice_scale(peak: int) -> tuple[int, int]:
    """The top of the value axis and the step of its grid lines: at most four."""
    for step in (1, 2, 5, 10, 20, 25, 50, 100, 200, 250, 500, 1000, 2000, 5000):
        if peak <= step * 4:
            return max(-(-peak // step), 1) * step, step
    return peak, peak


def counted(number: int, noun: str) -> tuple[str, str]:
    return f"{number:,}", f" {noun}" if number == 1 else f" {noun}s"


def bar_path(x: float, top: float, base: float) -> str:
    radius = min(4, (base - top) / 2)
    return (
        f"M{x:.1f} {base}V{top + radius:.1f}Q{x:.1f} {top:.1f} {x + radius:.1f} {top:.1f}"
        f"H{x + BAR_WIDTH - radius:.1f}Q{x + BAR_WIDTH:.1f} {top:.1f} {x + BAR_WIDTH:.1f} {top + radius:.1f}V{base}Z"
    )


def chart(days: list, theme: dict, name: str) -> str:
    peak = max(count for _, count in days)
    top_value, step = nice_scale(peak)
    slot = (PLOT_RIGHT - PLOT_LEFT) / len(days)
    height = PLOT_BASE - PLOT_TOP
    out = []
    for value in range(step, top_value + 1, step):
        y = PLOT_BASE - value / top_value * height
        out.append(
            f'<line x1="{PLOT_LEFT}" x2="{PLOT_RIGHT}" y1="{y:.1f}" y2="{y:.1f}" stroke="{theme["surface0"]}"/>'
            f'<text class="axis" x="{PLOT_LEFT - 12}" y="{y + 4.5:.1f}" text-anchor="end">{value}</text>'
        )
    labelled_peak = False
    for index, (day, count) in enumerate(days):
        x = PLOT_LEFT + index * slot + (slot - BAR_WIDTH) / 2
        if count:
            top = min(PLOT_BASE - count / top_value * height, PLOT_BASE - 3)
            out.append(
                f'<path class="bar" d="{bar_path(x, top, PLOT_BASE)}" fill="{BAR[name]}" '
                f'style="animation-delay:{0.15 + index * 0.025:.3f}s">'
                f"<title>{day:%b} {day.day}: {count}</title></path>"
            )
            if count == peak and not labelled_peak:
                labelled_peak = True
                out.append(
                    f'<text class="peak" x="{x + BAR_WIDTH / 2:.1f}" y="{top - 9:.1f}" text-anchor="middle">{count}</text>'
                )
        # A date under every seventh day, counted back from today.
        if (len(days) - 1 - index) % 7 == 0:
            out.append(
                f'<text class="axis" x="{x + BAR_WIDTH / 2:.1f}" y="{PLOT_BASE + 24}" text-anchor="middle">'
                f"{day:%b} {day.day}</text>"
            )
    out.append(
        f'<line x1="{PLOT_LEFT}" x2="{PLOT_RIGHT}" y1="{PLOT_BASE}" y2="{PLOT_BASE}" stroke="{theme["surface1"]}" stroke-width="1.5"/>'
    )
    return "".join(out)


def figure(pairs: list, x: int, y: int) -> str:
    spans = "".join(f'<tspan class="num">{number}</tspan><tspan>{label}</tspan>' for number, label in pairs)
    return f'<text class="stat" x="{x}" y="{y}">{spans}</text>'


def build(name: str, data: dict, today: date) -> str:
    theme = THEMES[name]
    month = data["user"]["month"]
    counts = daily_counts(month["contributionCalendar"])
    days = [(today - timedelta(days=offset), 0) for offset in range(DAYS - 1, -1, -1)]
    days = [(day, counts.get(day, 0)) for day, _ in days]
    total = sum(count for _, count in days)
    active = sum(1 for _, count in days if count)
    streak = weeks_in_a_row(data["user"]["year"]["contributionCalendar"])
    busiest = max(days, key=lambda item: item[1])

    rows = [
        [counted(month["totalCommitContributions"], "commit")],
        [counted(month["totalPullRequestContributions"], "pull request")],
        [counted(month["totalPullRequestReviewContributions"], "review")],
        [counted(month["totalIssueContributions"], "issue")],
    ]
    left = "".join(
        figure(row, 44 + (index % 2) * 200, 226 + (index // 2) * 32) for index, row in enumerate(rows)
    )
    if month["restrictedContributionsCount"]:
        number, _ = counted(month["restrictedContributionsCount"], "")
        left += figure([(number, " more in private repositories")], 44, 290)
    rhythm = [(f"{active}", f" of {DAYS} days active")]
    if streak > 1:
        rhythm.append((f"  {DOT}  {streak}", " weeks in a row"))
    footer = [
        counted(data["merged"]["issueCount"], "pull request")[0:1] + (" pull requests merged",),
        (f"  {DOT}  {data['reviewed']['issueCount']:,}", " pull requests reviewed"),
    ]
    summary = (
        f"{total:,} contributions from {days[0][0]:%b} {days[0][0].day} to {today:%b} {today.day}: "
        f"{month['totalCommitContributions']} commits, {month['totalPullRequestContributions']} pull requests, "
        f"{month['totalPullRequestReviewContributions']} reviews, {month['totalIssueContributions']} issues. "
        f"Busiest day: {busiest[0]:%b} {busiest[0].day} with {busiest[1]}. Active on {active} of {DAYS} days."
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="activity-title activity-desc">
<title id="activity-title">dec0iiyy on GitHub: the last {DAYS} days</title>
<desc id="activity-desc">{summary}</desc>
<style>
text {{ font-family: {SANS}; fill: {theme["subtext"]}; }}
.eyebrow {{ font-size: 14px; font-weight: 600; letter-spacing: 1.6px; }}
.hero {{ font-size: 76px; font-weight: 700; fill: {theme["text"]}; }}
.unit {{ font-size: 20px; }}
.stat {{ font-size: 17px; }}
.num {{ font-weight: 700; fill: {theme["text"]}; }}
.axis {{ font-size: 13px; fill: {theme["overlay2"]}; }}
.peak {{ font-size: 14px; font-weight: 700; fill: {theme["text"]}; }}
.bar {{ transform-box: fill-box; transform-origin: 50% 100%;
  animation: grow 0.7s cubic-bezier(0.2, 0.8, 0.2, 1) backwards; }}
@keyframes grow {{ from {{ transform: scaleY(0); }} to {{ transform: scaleY(1); }} }}
@media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
</style>
<rect x="1" y="1" width="{WIDTH - 2}" height="{HEIGHT - 2}" rx="20" fill="{theme["base"]}" stroke="{theme["surface0"]}" stroke-width="1.5"/>
<text class="eyebrow" x="44" y="64">LAST {DAYS} DAYS</text>
<text class="hero" x="40" y="148">{total:,}</text>
<text class="unit" x="44" y="182">contributions in the open</text>
{left}
<text class="eyebrow" x="{PLOT_LEFT}" y="44">PER DAY</text>
{chart(days, theme, name)}
<line x1="44" x2="{WIDTH - 44}" y1="{HEIGHT - 70}" y2="{HEIGHT - 70}" stroke="{theme["surface0"]}"/>
{figure(rhythm, 44, HEIGHT - 32)}
<text class="stat" x="{WIDTH - 44}" y="{HEIGHT - 32}" text-anchor="end"><tspan>Open source so far:  </tspan>{"".join(f'<tspan class="num">{number}</tspan><tspan>{label}</tspan>' for number, label in footer)}</text>
</svg>
'''


def main() -> None:
    token = os.environ["GITHUB_TOKEN"]
    login = os.environ.get("PROFILE_USER") or os.environ["GITHUB_REPOSITORY_OWNER"]
    target = Path(sys.argv[1])
    target.mkdir(parents=True, exist_ok=True)
    today = datetime.now(timezone.utc).date()
    data = fetch(login, token, today)
    for name in THEMES:
        (target / f"activity-{name}.svg").write_text(build(name, data, today), encoding="utf-8")
        print(f"wrote {target / f'activity-{name}.svg'}")


if __name__ == "__main__":
    main()
