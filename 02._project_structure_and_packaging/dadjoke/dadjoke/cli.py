"""The command-line entry point.

`pyproject.toml` has:

    [project.scripts]
    dadjoke = "dadjoke.cli:main"

so after the package is installed, typing `dadjoke` in the terminal runs
`main()` below. This is the same mechanism that turns `vibe` into a command
in mistral-vibe (`vibe = "vibe.cli.entrypoint:main"`).
"""

import httpx

API_URL = "https://icanhazdadjoke.com/"


def fetch_joke() -> str:
    """Ask the API for a random dad joke and return it as text."""
    response = httpx.get(API_URL, headers={"Accept": "application/json"})
    response.raise_for_status()
    return response.json()["joke"]


def main() -> None:
    """Entry point: print one random dad joke."""
    print(fetch_joke())
