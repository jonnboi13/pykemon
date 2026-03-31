# 🔴 pykemon

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docs](https://img.shields.io/badge/docs-mkdocs-green)](https://byuirpytooling.github.io/pykemon)

A Python package that gives data science students easy access to a rich Pokémon database — covering all 9 generations of Pokémon, moves, abilities, items, natures, and more. No scraping, no setup, just query and go.

---

## 📦 Installation

**pip:**
```bash
pip install git+https://github.com/byuirpytooling/pykemon.git
```

**uv:**
```bash
uv add git+https://github.com/byuirpytooling/pykemon.git
```

---

## ⚡ Quick Start

```python
from pykemon.db import get_connection

con = get_connection()
pokemon = con.sql("SELECT * FROM pokemon").pl()
pokemon
```

---

## 🗄️ What's in the Database?

| Table | Description | Rows (approx.) |
|---|---|---|
| `pokemon` | Every Pokémon with base stats, types, and generation | 1,000+ |
| `move` | Every move with type, power, accuracy, and effect | 900+ |
| `pokemon_move` | Which Pokémon can learn which moves, and how | 100,000+ |
| `ability` | Ability names and effects | 300+ |
| `pokemon_ability` | Which Pokémon have which abilities | 3,000+ |
| `item` | Item names, categories, and effects | 900+ |
| `nature` | The 25 natures and their stat modifiers | 25 |
| `status_effect` | Status conditions with damage and stat modifiers | 10+ |

---

## 📚 Documentation

Full documentation, a getting started guide, and worked vignettes are available at:

**[byuirpytooling.github.io/pykemon](https://byuirpytooling.github.io/pykemon)**

---

## 🔬 Example Analysis

Looking for inspiration? Check out the [Power Creep vignette](https://byuirpytooling.github.io/pykemon/power-creep/) — a full worked example analyzing how Pokémon base stats have changed across all 9 generations.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.
