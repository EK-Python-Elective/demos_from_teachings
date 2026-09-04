"""The command-line entry point.

`pyproject.toml` has:

    [project.scripts]
    milspend = "milspend.cli:main"

so after the package is installed, typing `milspend` in the terminal runs
`main()` below. This is the same mechanism that turns `vibe` into a command
in mistral-vibe (`vibe = "vibe.cli.entrypoint:main"`).
"""

import sys

import httpx

# World Bank Open Data, indicator MS.MIL.XPND.GD.ZS = "Military expenditure (% of GDP)".
# Underlying source: Stockholm International Peace Research Institute (SIPRI).
# Public, no API key required.
API_URL = "https://api.worldbank.org/v2/country/{code}/indicator/MS.MIL.XPND.GD.ZS"


def fetch_expenditure(code: str) -> tuple[str, list[tuple[str, float]]]:
    """Return (country name, [(year, percent_of_gdp), ...]) for an ISO-3 country code."""
    response = httpx.get(
        API_URL.format(code=code),
        params={"format": "json", "per_page": "100"},
    )
    response.raise_for_status()
    payload = response.json()

    if not isinstance(payload, list) or len(payload) < 2 or payload[1] is None:
        raise SystemExit(f"No data for country code {code!r} (try an ISO-3 code like UKR, USA, DNK)")

    rows = [(row["date"], row["value"]) for row in payload[1] if row["value"] is not None]
    country = payload[1][0]["country"]["value"]
    return country, sorted(rows)


def main() -> None:
    """Print military expenditure as a share of GDP for a country (default: Ukraine)."""
    code = sys.argv[1] if len(sys.argv) > 1 else "UKR"
    country, rows = fetch_expenditure(code)

    print(f"Military expenditure (% of GDP) — {country}")
    for year, percent in rows[-10:]:
        print(f"  {year}  {percent:5.1f}%")
