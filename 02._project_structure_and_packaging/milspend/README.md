# milspend

A tiny CLI built from scratch during **session 2** to see every part of a
Python project up close: `pyproject.toml`, a package folder, an entry point,
a dependency, and a lock file.

It reports a country's **military expenditure as a share of GDP**, from the
World Bank's open-data API (underlying source: SIPRI).

```console
$ uv run milspend UKR
Military expenditure (% of GDP) — Ukraine
  2015    3.8%
  2016    3.7%
  2017    3.2%
  2018    3.6%
  2019    4.1%
  2020    4.4%
  2021    3.4%
  2022   25.6%
  2023   36.5%
  2024   34.5%

$ uv run milspend DNK
```

## Layout

```
milspend/
├── pyproject.toml        # metadata, the httpx dependency, the entry point, the build backend
├── uv.lock              # exact resolved versions of httpx and everything it pulls in
├── .python-version      # which Python uv uses here
└── milspend/            # the package (flat layout, like mistral-vibe's vibe/)
    ├── __init__.py
    ├── cli.py           # main() — what `[project.scripts]` points at
    └── __main__.py      # so `python -m milspend` works too
```

## Run it

```console
uv sync                # create .venv, install from uv.lock
uv run milspend UKR    # run the entry-point command (ISO-3 country code, default UKR)
```

See the folder above (`../README.md`) for the full build walkthrough and how
this maps onto the mistral-vibe fork.
