# dadjoke

A tiny CLI built from scratch during **session 2** to see every part of a
Python project up close: `pyproject.toml`, a package folder, an entry point,
a dependency, and a lock file.

```console
$ uv run dadjoke
Why don't eggs tell jokes? They'd crack each other up.
```

## Layout

```
dadjoke/
├── pyproject.toml        # metadata, the httpx dependency, the entry point, the build backend
├── uv.lock              # exact resolved versions of httpx and everything it pulls in
├── .python-version      # which Python uv uses here
└── dadjoke/             # the package (flat layout, like mistral-vibe's vibe/)
    ├── __init__.py
    ├── cli.py           # main() — what `[project.scripts]` points at
    └── __main__.py      # so `python -m dadjoke` works too
```

## Run it

```console
uv sync          # create .venv, install from uv.lock
uv run dadjoke   # run the entry-point command
```

See the folder above (`../README.md`) for the full build walkthrough and how
this maps onto the mistral-vibe fork.
