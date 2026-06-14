# Jupyter from the terminal, in the browser

Launch a notebook server from the command line and work in your web browser. Good when you want notebooks without VS Code, or want to show the "classic" Jupyter experience.

## What you need first

- **`uv`** installed (from session 1). Check with `uv --version`.

That's it — `uv` fetches Jupyter for you, so there's nothing to install globally.

## Option A — a one-off, no project

To start Jupyter Lab without setting anything up, let `uv` run it in a throwaway environment:

```bash
uvx --from jupyterlab jupyter lab
```

`uvx` runs a tool without installing it permanently. `--from jupyterlab` tells `uv` which package provides the `jupyter lab` command.

## Option B — inside a project (recommended if you'll reuse it)

If you want the same setup again later, add Jupyter to a project:

```bash
mkdir jupyter-demo && cd jupyter-demo
uv init
uv add --dev jupyterlab     # --dev: a tool for working on the project, not a dependency of it
uv run jupyter lab
```

`uv run` runs the command inside the project's environment, so any packages you `uv add` are importable from your notebook.

## What happens when it starts

- A server starts in your terminal and your browser opens automatically at **`http://localhost:8888`**.
- If the browser doesn't open, copy the URL the terminal prints — it includes a one-time **token** (`http://localhost:8888/lab?token=...`) that authorises your session. The terminal must stay open while you work; the server runs there.

In the browser:
1. Use the file browser on the left to pick a folder.
2. Click **+** (or File → New → Notebook) and choose the **Python 3** kernel.
3. Type code in a cell and press **`Shift+Enter`** to run it:

   ```python
   from pydantic import BaseModel

   class Config(BaseModel):
       model: str = "mistral-small"
       temperature: float = 0.7

   Config(temperature="not a number")   # watch Pydantic raise a validation error
   ```

## Shutting it down

Go back to the terminal and press **`Ctrl+C`**, then confirm (or press it twice). That stops the server. Closing only the browser tab does **not** stop it — the server keeps running in the terminal until you stop it.

## Lab vs. Notebook

`jupyter lab` is the modern interface (file browser, tabs, multiple notebooks). The older, simpler single-notebook interface is `jupyter notebook` — swap the command if you prefer it (`uvx --from notebook jupyter notebook`). Both run the same notebooks.

## A note on `.ipynb` files and git

A notebook is a JSON file storing code **and output**, which makes for noisy git diffs. Keep notebooks for exploration and demos; the project's real code belongs in `.py` files. (This repo's `.gitignore` already ignores `.ipynb_checkpoints/`.)
