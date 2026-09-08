"""One deliberate violation for every rule the mistral-vibe fork's [tool.ruff] selects.

Teaching fixture for session 2, part 3 (tooling). NOT meant to run — every block
below trips a different ruff rule on purpose.

The `ruff.toml` next to this file mirrors the fork's `[tool.ruff.lint]` exactly
(select / ignore / the flake8-tidy-imports + isort + pylint settings), so:

    uvx ruff check ruff_check_failures.py          # see every failure
    uvx ruff check --fix ruff_check_failures.py    # auto-fix the fixable ones

Dropping this file straight into your fork works too — it already has the config.
"""

from __future__ import annotations

# I  (isort): import block not sorted — `json` should come before `sys`. (fixable)
# F  (pyflakes): both `json` and `sys` are imported but never used — F401 per line. (fixable)
import sys
import json

from typing import Optional

# TID (flake8-tidy-imports, ban-relative-imports = "all"): relative imports are banned.
from . import qr  # TID252 — this fixture won't run, so the dangling import is fine


# D2 (pydocstyle "D2xx"): D202 — no blank line allowed right after a function docstring.
def greet() -> None:
    """Say hello."""

    print("hi")


# UP (pyupgrade): UP045 — `Optional[str]` should be written `str | None`. (fixable)
def middle_name(name: Optional[str]) -> str:
    return name or ""


# ANN (flake8-annotations): ANN001 + ANN201 — argument and return type both missing.
def double(n):
    return n * 2


# PLR (pylint "refactor"): PLR2004 — magic value used directly in a comparison.
def is_ok(status: int) -> bool:
    return status == 200


# B0 (flake8-bugbear "B0xx"): B006 — mutable value as a default argument.
def append_item(item: int, bucket: list[int] = []) -> list[int]:
    bucket.append(item)
    return bucket


# B905: `zip()` called without an explicit `strict=`.
def pair_up(a: list[int], b: list[int]) -> list[tuple[int, int]]:
    return list(zip(a, b))


# RUF010: explicit `str()` inside an f-string; use the `!s` conversion flag. (fixable)
def describe(value: object) -> str:
    return f"value is {str(value)}"


# RUF019: redundant `key in dict` check before indexing; use `.get()`. (fixable)
def lookup(data: dict[str, int]) -> int:
    if "count" in data and data["count"]:
        return data["count"]
    return 0


class Config:
    """Holds settings."""

    # RUF012: mutable class-attribute default without a `ClassVar` annotation.
    tags: list[str] = []


# RUF022: `__all__` is not sorted. (fixable)
__all__ = ["middle_name", "greet", "double"]


# RUF100: the suppression comment on the next line silences a rule that never fires. (fixable)
spare = 1 + 1  # noqa: PLR2004
