# %%
import sys

sys.path.insert(0, "data-raw")
import polars as pl
import duckdb
from pathlib import Path
import json
from build_db import (
    insert_base_teams,
    make_db,
    insert_pokemon,
    insert_items,
    insert_pokemon_moves,
    insert_abilities,
    insert_moves,
    insert_pokemon_abilities,
    insert_natures,
    insert_status_effects,
    insert_team,
    insert_team_pokemon,
    insert_team_pokemon_move
)

# %%

POKEMON = Path("raw/pokemon.csv")
ITEM = Path("raw/items.csv")
POKEMON_MOVE = Path("normalized/pokemon_moves.csv")
ABILITY = Path("raw/ability.csv")
POKEMON_ABILITY = Path("normalized/pokemon_ability.csv")
NATURE = Path("raw/nature.csv")
STATUS_EFFECT = Path("raw/status_effect.csv")
MOVE = Path("raw/moves.csv")
TEAM = Path("raw/team.csv")
TEAM_POKEMON = Path("normalized/team_pokemon.csv")
TEAM_POKEMON_MOVE = Path("normalized/team_pokemon_move.csv")
BASE_TEAMS = Path("raw/base_teams.json")



# %%

con = duckdb.connect("../src/pykemon/data/pykemon.duckdb")
# %%
pokemon_df = pl.read_csv(POKEMON)
items_df = pl.read_csv(ITEM)
pokemon_moves_df = pl.read_csv(POKEMON_MOVE)
abilities_df = pl.read_csv(ABILITY)
pokemon_abilities_df = pl.read_csv(POKEMON_ABILITY)
natures_df = pl.read_csv(NATURE)
status_effects_df = pl.read_csv(STATUS_EFFECT)
moves_df = pl.read_csv(MOVE)


with open(BASE_TEAMS) as f:
    base_team_data = json.load(f)
#%%
make_db(con)
insert_pokemon(con, pokemon_df)
insert_items(con, items_df)
insert_moves(con, moves_df)
insert_pokemon_moves(con, pokemon_moves_df)
insert_abilities(con, abilities_df)
insert_pokemon_abilities(con, pokemon_abilities_df)
insert_natures(con, natures_df)
insert_status_effects(con, status_effects_df)
#%%

insert_base_teams(con, base_team_data)
# %%
con.close()
# %%
