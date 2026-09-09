# qr

A tiny CLI built from scratch during **session 2** to see every part of a
Python project up close: `pyproject.toml`, a package folder, an entry point,
a dependency, and a lock file.

It prints a QR code for whatever text you give it — scan it with your phone.

```console
$ uv run qr "https://kea.dk"
█████████████████████████████
█████████████████████████████
████ ▄▄▄▄▄ ██▀█  █ ▄▄▄▄▄ ████
████ █   █ ███▀▀▄█ █   █ ████
████ █▄▄▄█ █▀█▄█▄█ █▄▄▄█ ████
████▄▄▄▄▄▄▄█▄█ █ █▄▄▄▄▄▄▄████
████ █▀ █▄▄▀▄█▀ ▀▄▀ ▀███▀████
████▄▄ ▀▀▄▄███▄▄▄█▀█▀▀▄▀ ████
████▄█▄▄█▄▄▄ ██  █▀ █▄██▀████
████ ▄▄▄▄▄ █▀▀▄▀ ▄▄▀ ▄▄ ▀████
████ █   █ █▀█ ▄▀▄▀█ ▄█▀▀████
████ █▄▄▄█ ██▀ █▄ ▄█▄█▄█▄████
████▄▄▄▄▄▄▄█▄▄█▄▄█▄█▄██▄█████
█████████████████████████████
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
```

## Layout

```
qr/
├── pyproject.toml        # metadata, the segno dependency, the entry point, the build backend
├── uv.lock              # exact resolved version of segno
├── .python-version      # which Python uv uses here
└── qr/                  # the package (flat layout, like mistral-vibe's vibe/)
    ├── __init__.py
    ├── cli.py           # main() — what `[project.scripts]` points at
    └── __main__.py      # so `python -m qr` works too
```

## Run it

```console
uv sync                  # create .venv, install from uv.lock
uv run qr "hello world"   # run the entry-point command
```

`segno` (the QR library) is a pure-Python package with **no dependencies of its
own** — so `uv.lock` stays tiny.

See the folder above (`../README.md`) for the full build walkthrough and how
this maps onto the mistral-vibe fork.
