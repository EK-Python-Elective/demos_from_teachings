# Session 2 — Demo: Build a Python project from scratch

Teaching demo for [session 2 of the curriculum](https://github.com/EK-Python-Elective/EK_DAT_Python_Elective_2026_fall/tree/main/02._project_structure_and_packaging)
(Project Structure & Python Packaging).

Session 2 is about *reading* a real `pyproject.toml` in the mistral-vibe fork.
This demo builds the smaller version first: a project with **one dependency and
one entry point**, created live in front of the class, so that every field in
mistral-vibe's `pyproject.toml` has already been seen in miniature.

The finished project is in [`dadjoke/`](dadjoke/). What follows is the script
for building it from an empty folder.

---

## What we're building

`dadjoke` — a one-command CLI that fetches a random dad joke over HTTP:

```console
$ uv run dadjoke
Why don't eggs tell jokes? They'd crack each other up.
```

The joke is not the point. The point is the four things around it:

| Piece | Where it ends up |
|---|---|
| Project metadata | `[project]` in `pyproject.toml` |
| A third-party dependency (`httpx`) | `[project].dependencies` + `uv.lock` |
| A terminal command | `[project.scripts]` |
| A build backend | `[build-system]` |

---

## Build it live

### 1. Start from nothing

```console
uv init --python 3.12 dadjoke
cd dadjoke
```

Look at what `uv init` made: `pyproject.toml`, `README.md`, `.python-version`,
and a `src/dadjoke/` package with a `main()` in `__init__.py`. Modern `uv`
(0.12+) scaffolds a **src layout** with its own `uv_build` backend and even
pre-fills `[project.scripts]`.

**Talking point:** mistral-vibe uses a **flat layout** (`vibe/` sits next to
`pyproject.toml`, no `src/`) and the **hatchling** backend. Both layouts are
everywhere in the wild. We'll convert to the flat + hatchling shape so the demo
matches what students are about to read in their fork.

### 2. Reshape to a flat layout

```console
rm -r src
mkdir dadjoke
```

Create the package files (see `dadjoke/` in this repo for the final content):

- `dadjoke/__init__.py` — just a version string
- `dadjoke/cli.py` — `fetch_joke()` and `main()`
- `dadjoke/__main__.py` — so `python -m dadjoke` also works

`main()` in `cli.py` is deliberately tiny:

```python
import httpx

API_URL = "https://icanhazdadjoke.com/"

def fetch_joke() -> str:
    response = httpx.get(API_URL, headers={"Accept": "application/json"})
    response.raise_for_status()
    return response.json()["joke"]

def main() -> None:
    print(fetch_joke())
```

### 3. Wire up `pyproject.toml` by hand

Edit it to the shape mistral-vibe uses:

```toml
[project]
name = "dadjoke"
version = "0.1.0"
description = "Print a random dad joke from icanhazdadjoke.com"
readme = "README.md"
requires-python = ">=3.12"
dependencies = ["httpx>=0.28"]

[project.scripts]
dadjoke = "dadjoke.cli:main"       # <command> = "<module>:<function>"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
include = ["dadjoke/"]
```

**Talking point — the entry point.** `dadjoke = "dadjoke.cli:main"` is the
whole trick behind "why does typing a word run Python?". At install time the
build backend writes a small launcher script named `dadjoke` onto the `PATH`;
that script imports `dadjoke.cli` and calls `main()`. Same line, same mechanism
as `vibe = "vibe.cli.entrypoint:main"`.

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
uv run dadjoke          # the entry-point script
uv run python -m dadjoke # the __main__.py path
```

`uv run` syncs the environment from the lock file first, then runs — so a
fresh clone + `uv run dadjoke` just works with no setup steps.

### 6. (Optional) See the package that would ship

```console
uv build
ls dist/
```

`dadjoke-0.1.0-py3-none-any.whl` is what `pip install dadjoke` would download
if this were on PyPI. Unzip it: it contains exactly the `dadjoke/` folder plus
metadata — the `[tool.hatch.build.targets.wheel] include` line decided that.
(Delete `dist/` afterwards; it's a build artifact, not source.)

---

## Now relate it to the mistral-vibe fork

Open the fork's `pyproject.toml` side by side with `dadjoke`'s and map it field
by field. Every concept is the same, just bigger:

| In `dadjoke` | In mistral-vibe | Note |
|---|---|---|
| `dadjoke/` next to `pyproject.toml` | `vibe/` next to `pyproject.toml` | same flat layout |
| 1 dependency (`httpx`) | ~60 dependencies, all `==`-pinned | `uv.lock` scales to hundreds of packages |
| `dadjoke = "dadjoke.cli:main"` | `vibe = "vibe.cli.entrypoint:main"` (+ `vibe-acp`, `vibe-app-server`) | one project can expose several commands |
| `[build-system]` → hatchling | hatchling **+ hatch-vcs** (version from git tags) | same backend, extra plugin |
| no tool config yet | `[tool.ruff]`, `[tool.pyright]`, `[tool.pytest]` … | tool config also lives in `pyproject.toml` — session 3 |

Then hand off to the **scavenger hunt** exercise: students now know what
`[project.scripts]` *is*, so "what function does `vibe` call?" is a lookup, not
a mystery.

---

## Notes for next time

- `httpx` is genuinely one of mistral-vibe's dependencies — nice, but it does
  mean a live network call in class. If the venue wi-fi is flaky, swap `main()`
  for a hard-coded joke and still demo the packaging (the dependency story
  survives; `httpx` just isn't called).
- `icanhazdadjoke.com` needs the `Accept: application/json` header or it
  returns HTML — a small, real reason to talk about request headers.
