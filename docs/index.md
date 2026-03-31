# pykemon

A Python package for accessing a rich Pokémon database covering all 9 generations — including base stats, moves, abilities, items, natures, and status effects.

---

## Quick Start

```bash
pip install git+https://github.com/byuirpytooling/pykemon.git
```

```py
from pykemon.db import get_connection

con = get_connection()
pokemon = con.sql("SELECT * FROM pokemon").pl()
```

---

## What's Inside

- **1,000+ Pokémon** across 9 generations, including regional forms and Mega Evolutions
- **Moves, abilities, items, natures, and status effects** — all in one place
- **DuckDB-powered** — fast SQL queries with no server required
- **Polars-friendly** — results come back as Polars DataFrames out of the box

---

## Where to Go Next

- [Getting Started](getting-started.md) — a full walkthrough of what you can do with the data
- [API Reference](API.md) — full documentation of the package
- [Power Creep Vignette](power-creep.md) — a worked example analyzing base stat trends across generations
