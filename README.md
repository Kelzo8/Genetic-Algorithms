# Genetic-Algorithms

## Exercises

Early standalone exercises live in `exercises/`. They don't use the GP engine.

```bash
python exercises/onemax_ga.py               # GA on OneMax
python exercises/symbolic_regression_gp.py  # first standalone GP (symbolic regression)
```

OneMax's default settings are in `exercises/config.example.py`. To use local
settings, copy it to `exercises/config.py` and edit that file; it is ignored by Git.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Genetic programming

The GP engine lives in the `GP/` package; each problem is a separate package
that supplies its own terminals and fitness function. Run everything from the
repository root:

```bash
python -m symreg.main     # symbolic regression sanity check (seed in GP/gp_config.py)
python -m pytest          # unit tests
```
