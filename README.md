# Genetic-Algorithms

## OneMax

Run the genetic algorithm with:

```bash
python onemax_ga.py
```

The default settings are in `config.example.py`. To use local settings, copy it
to `config.py` and edit that file; `config.py` is ignored by Git.

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
