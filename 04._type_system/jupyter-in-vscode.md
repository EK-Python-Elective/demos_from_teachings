# Jupyter notebooks in VS Code

Run notebooks inside VS Code — the same editor you use for the rest of the course. Good when you want code, notebook, and terminal side by side.

## What you need first

- **VS Code** installed.
- **`uv`** installed (from session 1). Check with `uv --version`.
- The **Python** and **Jupyter** extensions from Microsoft. Install them from the Extensions panel (the square icon in the left bar, or `Ctrl/Cmd+Shift+X`): search for "Python" and "Jupyter", both publisher *Microsoft*, and click Install.

## Step 1 — make a project with a notebook kernel

A notebook runs Python through a "kernel". The kernel needs the `ipykernel` package available in the environment you point VS Code at. We create a small `uv` project for that:

```bash
mkdir jupyter-demo && cd jupyter-demo
uv init               # creates pyproject.toml
uv add ipykernel      # the package that lets a notebook run in this environment
```

`uv` creates a `.venv` folder in the project — that is the environment (and kernel) VS Code will use.

## Step 2 — create a notebook

Open the project in VS Code (`code .` from the project folder, or File → Open Folder). Then either:

- Open the Command Palette (`Ctrl/Cmd+Shift+P`) → **"Create: New Jupyter Notebook"**, or
- Create a new file ending in `.ipynb` (for example `explore.ipynb`) and open it.

You get a notebook view with an empty cell.

## Step 3 — select the kernel

Top-right of the notebook, click **"Select Kernel"** → **Python Environments** → choose the interpreter inside your project's `.venv` (it will show the project path). If VS Code offers to install `ipykernel`, say yes — though `uv add ipykernel` already handled it.

## Step 4 — run code

Type into a cell and press **`Shift+Enter`** to run it and move to the next cell:

```python
from dataclasses import dataclass

@dataclass
class Message:
    role: str
    content: str

m = Message("user", "hello")
m            # the cell shows the repr: Message(role='user', content='hello')
```

Useful basics:
- **`Shift+Enter`** run cell and go to next; **`Ctrl/Cmd+Enter`** run cell and stay.
- The **`+ Code`** / **`+ Markdown`** buttons add cells. Markdown cells are for notes/headings.
- **Restart** (circular arrow) clears all variables and starts the kernel fresh — do this when things get into a weird state.
- The **Variables** button shows everything currently defined — handy for inspecting types, which is the point in session 4.

## A note on `.ipynb` files and git

A notebook is a JSON file that stores your code **and its output**. That makes notebooks noisy in git diffs and not a good home for project source code. Keep notebooks for exploration and demos; put real code in `.py` files. (This repo's `.gitignore` already ignores `.ipynb_checkpoints/`.)
