# Getting Started with pykemon

`pykemon` is a Python package that gives you easy access to a rich Pokémon database covering all 9 generations. Whether you're interested in competitive analysis, data visualization, or just exploring the data, `pykemon` gives you a clean interface to query Pokémon stats, moves, abilities, items, and more.

---

## 📦 Installation

=== "pip"

    ```bash
    pip install git+https://github.com/byuirpytooling/pykemon.git
    ```

=== "uv"

    ```bash
    uv add git+https://github.com/byuirpytooling/pykemon.git
    ```

---

## Connecting to the Database

Everything starts with `get_connection()`, which returns a DuckDB connection to the bundled database:

```py
from pykemon.db import get_connection

con = get_connection()
```

The connection is **read-only**, so you can query freely without worrying about accidentally modifying the data.

To verify your connection and see the available tables directly from your terminal or notebook, you can run:

```py
con.execute("SHOW TABLES").fetchall()
[('ability',), ('item',), ('move',), ('nature',), ('pokemon',), ('pokemon_ability',), ('pokemon_move',), ('status_effect',), ('team',), ('team_pokemon',), ('team_pokemon_move',)]
```
---

## What's in the Database?

The database contains 8 tables:

| Table | Description |
|---|---|
| `pokemon` | Every Pokémon with base stats, types, and generation |
| `move` | Every move with type, power, accuracy, and effect |
| `pokemon_move` | Which Pokémon can learn which moves, and how |
| `ability` | Ability names and effects |
| `pokemon_ability` | Which Pokémon have which abilities |
| `item` | Item names, categories, and effects |
| `nature` | The 25 natures and their stat modifiers |
| `status_effect` | Status conditions with damage and stat modifiers |

---

## Querying the Data

You can query any table using SQL and get back a Polars DataFrame:

```py
import polars as pl
from pykemon.db import get_connection

con = get_connection()

pokemon = con.sql("SELECT * FROM pokemon").pl()
pokemon
```

Or filter directly in SQL:

```py
# Get all Fire type Pokémon
con.sql("SELECT name, total FROM pokemon WHERE primary_type = 'Fire' ORDER BY total DESC").pl()
```

---

## Things You Can Do

Here are some ideas to get you started:

### Explore Base Stats

```py
# Top 10 Pokémon by base stat total
con.sql("""
    SELECT name, primary_type, secondary_type, total
    FROM pokemon
    ORDER BY total DESC
    LIMIT 10
""").pl()
```

### Find a Pokémon's Full Moveset

```py
# All moves Pikachu can learn
con.sql("""
    SELECT p.name, m.move_name, m.type, m.power, pm.method
    FROM pokemon p
    JOIN pokemon_move pm ON p.pokemon_id = pm.pokemon_id
    JOIN move m ON pm.move_id = m.move_id
    WHERE p.name = 'Pikachu'
    ORDER BY m.power DESC NULLS LAST
""").pl()
```

### Compare Types

```py
# Average base stat total by primary type
con.sql("""
    SELECT primary_type, ROUND(AVG(total), 1) as avg_bst, COUNT(*) as count
    FROM pokemon
    GROUP BY primary_type
    ORDER BY avg_bst DESC
""").pl()
```

### Look Up Abilities

```py
# Find all Pokémon with a specific ability
con.sql("""
    SELECT p.name, a.ability_name, pa.slot
    FROM pokemon p
    JOIN pokemon_ability pa ON p.pokemon_id = pa.pokemon_id
    JOIN ability a ON pa.ability_id = a.ability_id
    WHERE a.ability_name = 'Intimidate'
""").pl()
```

### Work with Natures

```py
# All natures that boost Attack
con.sql("""
    SELECT name, stat_up, stat_down
    FROM nature
    WHERE stat_up = 'attack'
""").pl()
```

---

## Going Further

Once you're comfortable with the basics, check out the **Power Creep** vignette for a full worked example that analyzes how Pokémon base stats have changed across generations — including histograms, median trends, and a discussion of what the data reveals about game balance over time.

!!! note "Power Creep Vignette"
    The [Power Creep](power-creep.md) vignette walks through a complete analysis using `pykemon`, `polars`, and `matplotlib`. It's a great template for building your own analyses.
