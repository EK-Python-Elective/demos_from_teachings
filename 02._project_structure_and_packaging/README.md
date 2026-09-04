# Session 2 — Demo: Build a Python project from scratch

Teaching demo for [session 2 of the curriculum](https://github.com/EK-Python-Elective/EK_DAT_Python_Elective_2026_fall/tree/main/02._project_structure_and_packaging)
(Project Structure & Python Packaging).

Session 2 is about *reading* a real `pyproject.toml` in the mistral-vibe fork.
This demo builds the smaller version first: a project with **one dependency and
one entry point**, created live in front of the class, so that every field in
mistral-vibe's `pyproject.toml` has already been seen in miniature.

The finished project is in [`milspend/`](milspend/). What follows is the script
for building it from an empty folder.

---

## What we're building

`milspend` — a one-command CLI that reports a country's **military expenditure
as a share of GDP**, pulled live from the World Bank's open-data API
(underlying source: SIPRI):

```console
$ uv run milspend UKR
Military expenditure (% of GDP) — Ukraine
  2020    4.4%
  2021    3.4%
  2022   25.6%
  2023   36.5%
  2024   34.5%
```

The data isn't the point (though it makes for a real conversation — try `DNK`,
`SWE`, `USA`, `RUS`). The point is the four things around it:

| Piece | Where it ends up |
|---|---|
| Project metadata | `[project]` in `pyproject.toml` |
| A third-party dependency (`httpx`) | `[project].dependencies` + `uv.lock` |
| A terminal command | `[project.scripts]` |
| A build backend | `[build-system]` |

Why this API: it's public with **no API key**, it's stable, and the JSON is
small. `MS.MIL.XPND.GD.ZS` is the World Bank indicator code for "Military
expenditure (% of GDP)".

---

## Build it live

### 1. Start from nothing

```console
uv init --python 3.12 milspend
cd milspend
```

Look at what `uv init` made: `pyproject.toml`, `README.md`, `.python-version`,
and a `src/milspend/` package with a `main()` in `__init__.py`. Modern `uv`
(0.12+) scaffolds a **src layout** with its own `uv_build` backend and even
pre-fills `[project.scripts]`.

**Talking point:** mistral-vibe uses a **flat layout** (`vibe/` sits next to
`pyproject.toml`, no `src/`) and the **hatchling** backend. Both layouts are
everywhere in the wild. We'll convert to the flat + hatchling shape so the demo
matches what students are about to read in their fork.

### 2. Reshape to a flat layout

```console
rm -r src
mkdir milspend
```

Create the package files (see `milspend/` in this repo for the final content):

- `milspend/__init__.py` — just a version string
- `milspend/cli.py` — `fetch_expenditure()` and `main()`
- `milspend/__main__.py` — so `python -m milspend` also works

`main()` in `cli.py` is deliberately small:

```python
import sys
import httpx

API_URL = "https://api.worldbank.org/v2/country/{code}/indicator/MS.MIL.XPND.GD.ZS"

def fetch_expenditure(code: str) -> tuple[str, list[tuple[str, float]]]:
    response = httpx.get(API_URL.format(code=code), params={"format": "json", "per_page": "100"})
    response.raise_for_status()
    payload = response.json()
    rows = [(r["date"], r["value"]) for r in payload[1] if r["value"] is not None]
    return payload[1][0]["country"]["value"], sorted(rows)

def main() -> None:
    code = sys.argv[1] if len(sys.argv) > 1 else "UKR"
    country, rows = fetch_expenditure(code)
    print(f"Military expenditure (% of GDP) — {country}")
    for year, percent in rows[-10:]:
        print(f"  {year}  {percent:5.1f}%")
```

(Small teachable quirk: the World Bank returns a **two-element list** —
`[metadata, data]` — so the rows live in `payload[1]`, not `payload`.)

### 3. Wire up `pyproject.toml` by hand

Edit it to the shape mistral-vibe uses:

```toml
[project]
name = "milspend"
version = "0.1.0"
description = "Report a country's military expenditure (% of GDP) from World Bank / SIPRI data"
readme = "README.md"
requires-python = ">=3.12"
dependencies = ["httpx>=0.28"]

[project.scripts]
milspend = "milspend.cli:main"     # <command> = "<module>:<function>"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
include = ["milspend/"]
```

**Talking point — the entry point.** `milspend = "milspend.cli:main"` is the
whole trick behind "why does typing a word run Python?". At install time the
build backend writes a small launcher script named `milspend` onto the `PATH`;
that script imports `milspend.cli` and calls `main()`. Same line, same
mechanism as `vibe = "vibe.cli.entrypoint:main"`.

### 4. Add the dependency with uv

```console
uv add httpx
```

Show the diff live:

- `pyproject.toml` — `httpx>=0.28` was already in our `dependencies`; `uv add`
  confirms it and pins nothing there.
- `uv.lock` — **new file**, ~8 packages: `httpx` plus everything it needs
  (`httpcore`, `h11`, `anyio`, `certifi`, `idna`, …), each with an exact
  version and a hash. Nobody writes this by hand.
- `.venv/` — created automatically, `httpx` installed into it.

**Talking point — uv vs pip.** With `pip` this would have been:
`python -m venv .venv`, `source .venv/bin/activate`, `pip install httpx`, then
manually add a line to `requirements.txt` and hope you got the version right.
`uv` did the venv, the install, and the exact lock in one command.

### 5. Run the command

```console
uv run milspend UKR          # the entry-point script
uv run python -m milspend    # the __main__.py path (defaults to UKR)
```

`uv run` syncs the environment from the lock file first, then runs — so a
fresh clone + `uv run milspend` just works with no setup steps.

### 6. (Optional) See the package that would ship

```console
uv build
ls dist/
```

`milspend-0.1.0-py3-none-any.whl` is what `pip install milspend` would download
if this were on PyPI. Unzip it: it contains exactly the `milspend/` folder plus
metadata — the `[tool.hatch.build.targets.wheel] include` line decided that.
(Delete `dist/` afterwards; it's a build artifact, not source.)

---

## Now relate it to the mistral-vibe fork

Open the fork's `pyproject.toml` side by side with `milspend`'s and map it
field by field. Every concept is the same, just bigger:

| In `milspend` | In mistral-vibe | Note |
|---|---|---|
| `milspend/` next to `pyproject.toml` | `vibe/` next to `pyproject.toml` | same flat layout |
| 1 dependency (`httpx`) | ~60 dependencies, all `==`-pinned | `uv.lock` scales to hundreds of packages |
| `milspend = "milspend.cli:main"` | `vibe = "vibe.cli.entrypoint:main"` (+ `vibe-acp`, `vibe-app-server`) | one project can expose several commands |
| `[build-system]` → hatchling | hatchling **+ hatch-vcs** (version from git tags) | same backend, extra plugin |
| no tool config yet | `[tool.ruff]`, `[tool.pyright]`, `[tool.pytest]` … | tool config also lives in `pyproject.toml` — session 3 |

`httpx` is not a coincidence: it's genuinely one of mistral-vibe's
dependencies (the fork talks to the Mistral API over HTTP), so the dependency
students just added is one they'll meet again in session 7.

Then hand off to the **scavenger hunt** exercise: students now know what
`[project.scripts]` *is*, so "what function does `vibe` call?" is a lookup, not
a mystery.

---

## Notes for next time

- Live network call in class. If the venue wi-fi is flaky, hard-code a short
  list of `(year, value)` tuples in `main()` and still demo the packaging — the
  dependency story survives, `httpx` just isn't called.
- The World Bank API wants an **ISO-3** country code (`UKR`, `USA`, `DNK`), not
  ISO-2. A bad code returns `[metadata, null]` — `main()` turns that into a
  clean error, a small excuse to talk about checking API responses.
- Good countries to pull up live: `UKR` (3% → 36% across 2021–2023), `DNK` /
  `SWE` (the recent NATO-2% climb), `RUS`, `USA`.
