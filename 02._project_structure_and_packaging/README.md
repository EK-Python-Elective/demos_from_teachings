# Session 2 — Demo: Build a Python project from scratch

Teaching demo for [session 2 of the curriculum](https://github.com/EK-Python-Elective/EK_DAT_Python_Elective_2026_fall/tree/main/02._project_structure_and_packaging)
(Project Structure & Python Packaging).

Session 2 is about *reading* a real `pyproject.toml` in the mistral-vibe fork.
This demo builds the smaller version first: a project with **one dependency and
one entry point**, created live in front of the class, so that every field in
mistral-vibe's `pyproject.toml` has already been seen in miniature.

The finished project is in [`qr/`](qr/). What follows is the script for building
it from an empty folder.

---

## What we're building

`qr` — a one-command CLI that prints a QR code for any text, right in the
terminal (scannable with a phone):

```console
$ uv run qr "https://kea.dk"
█████████████████████
██ ▄▄▄▄▄ █ █▄▀▄▀▄█▄██
██ █   █ █▀ ▀▄ ██▀ ██
██ █▄▄▄█ █▀ █▀▄ ▄█▄██
██▄▄▄▄▄▄▄█▄ ██ ██▀ ██
██▄█▀ █▄▄ ▀ ▄▀ ███▄██
██▄█▄ ▄▀▀▄▀▄▀▄▀█▀▄▀██
██▄▀▄▀▀ █▄███▀ ▄██ ██
██▄▄▄▀ ▄  ▀▄▄█▀ ▀████
██▄▄████▄█▄▄▄▄▄███▄██
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
```

No network, no files, no config — the whole app is one call to the `segno`
library. That's the point: the four things around it are the lesson.

| Piece | Where it ends up |
|---|---|
| Project metadata | `[project]` in `pyproject.toml` |
| A third-party dependency (`segno`) | `[project].dependencies` + `uv.lock` |
| A terminal command | `[project.scripts]` |
| A build backend | `[build-system]` |

Why `segno`: it's pure Python with **zero dependencies of its own**, so
`uv.lock` stays small enough to read end to end in class.

---

## Build it live

### 1. Start from nothing

```console
uv init --python 3.12 qr
cd qr
```

Look at what `uv init` made: `pyproject.toml`, `README.md`, `.python-version`,
and a `src/qr/` package with a `main()` in `__init__.py`. Modern `uv` (0.12+)
scaffolds a **src layout** with its own `uv_build` backend and even pre-fills
`[project.scripts]`.

**Talking point:** mistral-vibe uses a **flat layout** (`vibe/` sits next to
`pyproject.toml`, no `src/`) and the **hatchling** backend. Both layouts are
everywhere in the wild. We'll convert to the flat + hatchling shape so the demo
matches what students are about to read in their fork.

### 2. Reshape to a flat layout

```console
rm -r src
mkdir qr
```

Create the package files (see `qr/` in this repo for the final content):

- `qr/__init__.py` — just a version string
- `qr/cli.py` — `main()`
- `qr/__main__.py` — so `python -m qr` also works

`main()` in `cli.py` is deliberately tiny:

```python
import sys
import segno

def main() -> None:
    text = " ".join(sys.argv[1:])
    if not text:
        raise SystemExit("usage: qr <text>")
    segno.make(text).terminal(compact=True)
```

### 3. Wire up `pyproject.toml` by hand

Edit it to the shape mistral-vibe uses:

```toml
[project]
name = "qr"
version = "0.1.0"
description = "Print a QR code for any text, in the terminal"
readme = "README.md"
requires-python = ">=3.12"
dependencies = ["segno>=1.6"]

[project.scripts]
qr = "qr.cli:main"                  # <command> = "<module>:<function>"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
include = ["qr/"]
```

**Talking point — the entry point.** `qr = "qr.cli:main"` is the whole trick
behind "why does typing a word run Python?". At install time the build backend
writes a small launcher script named `qr` onto the `PATH`; that script imports
`qr.cli` and calls `main()`. Same line, same mechanism as
`vibe = "vibe.cli.entrypoint:main"`.

### 4. Add the dependency with uv

```console
uv add segno
```

Show the diff live:

- `pyproject.toml` — `segno>=1.6` was already in our `dependencies`; `uv add`
  confirms it.
- `uv.lock` — **new file**. Just two entries: our own `qr` package and `segno`.
  Each with an exact version and a hash. Nobody writes this by hand — and with a
  heavier dependency it would list dozens of transitive packages instead of one.
- `.venv/` — created automatically, `segno` installed into it.

**Talking point — uv vs pip.** With `pip` this would have been:
`python -m venv .venv`, `source .venv/bin/activate`, `pip install segno`, then
manually add a line to `requirements.txt` and hope you got the version right.
`uv` did the venv, the install, and the exact lock in one command.

### 5. Run the command

```console
uv run qr "hello world"       # the entry-point script
uv run python -m qr "hello"    # the __main__.py path
```

`uv run` syncs the environment from the lock file first, then runs — so a
fresh clone + `uv run qr ...` just works with no setup steps.

### 6. (Optional) See the package that would ship

```console
uv build
ls dist/
```

`qr-0.1.0-py3-none-any.whl` is what `pip install qr` would download if this
were on PyPI. Unzip it: it contains exactly the `qr/` folder plus metadata —
the `[tool.hatch.build.targets.wheel] include` line decided that. (Delete
`dist/` afterwards; it's a build artifact, not source.)

---

## Now relate it to the mistral-vibe fork

Open the fork's `pyproject.toml` side by side with `qr`'s and map it field by
field. Every concept is the same, just bigger:

| In `qr` | In mistral-vibe | Note |
|---|---|---|
| `qr/` next to `pyproject.toml` | `vibe/` next to `pyproject.toml` | same flat layout |
| 1 dependency (`segno`), no transitive deps | ~60 dependencies, all `==`-pinned, hundreds of transitive | `uv.lock` scales without changing shape |
| `qr = "qr.cli:main"` | `vibe = "vibe.cli.entrypoint:main"` (+ `vibe-acp`, `vibe-app-server`) | one project can expose several commands |
| `[build-system]` → hatchling | hatchling **+ hatch-vcs** (version from git tags) | same backend, extra plugin |
| no tool config yet | `[tool.ruff]`, `[tool.pyright]`, `[tool.pytest]` … | tool config also lives in `pyproject.toml` — session 3 |

Point at one dependency in the fork's list that students will actually meet
later — `httpx` (session 7), `pydantic` (session 4) — and note it arrived the
exact same way: `uv add`, then it's in `uv.lock`.

Then hand off to the **scavenger hunt** exercise: students now know what
`[project.scripts]` *is*, so "what function does `vibe` call?" is a lookup, not
a mystery.

---

## Notes for next time

- Fully offline — no wi-fi dependency, nothing to fall back to.
- `segno.make(text).terminal(compact=True)` — `compact=True` uses half-block
  characters so the code fits in fewer terminal rows. Drop it if a projector
  renders the half-blocks badly.
- Fun 20-second aside if you want one: longer text → denser QR (`qr "$(date)"`
  vs `qr "hi"`), because more data needs a bigger grid. Not required.
