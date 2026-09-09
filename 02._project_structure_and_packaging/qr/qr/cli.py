"""The command-line entry point.

`pyproject.toml` has:

    [project.scripts]
    qr = "qr.cli:main"

so after the package is installed, typing `qr` in the terminal runs `main()`
below. This is the same mechanism that turns `vibe` into a command in
mistral-vibe (`vibe = "vibe.cli.entrypoint:main"`).
"""

import sys

import segno


def main() -> None:
    """Print a QR code for the text given on the command line."""
    text = " ".join(sys.argv[1:])
    if not text:
        raise SystemExit("usage: qr <text>")

    # micro=False: segno defaults to a Micro QR Code for short text, which
    # most phone cameras can't scan (they only recognise standard QR Codes).
    code = segno.make(text, micro=False)
    code.terminal(compact=True)
