import polars as pl
import duckdb

def insert_team_pokemon(con, team_pokemon: dict):
    con.execute("""
        INSERT INTO team_pokemon (
            team_id,
            pokemon_id,
            ability_id,
            nature_id,
            item_id,
            health_IV, attack_IV, defense_IV, sp_atk_IV, sp_def_IV, speed_IV,
            health_EV, attack_EV, defense_EV, sp_atk_EV, sp_def_EV, speed_EV,
            level
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        team_pokemon["team_id"],
        team_pokemon["pokemon_id"],
        team_pokemon["ability_id"],
        team_pokemon["nature_id"],
        team_pokemon.get("item_id"),
        team_pokemon.get("health_IV", 31),
        team_pokemon.get("attack_IV", 31),
        team_pokemon.get("defense_IV", 31),
        team_pokemon.get("sp_atk_IV", 31),
        team_pokemon.get("sp_def_IV", 31),
        team_pokemon.get("speed_IV", 31),
        team_pokemon.get("health_EV", 0),
        team_pokemon.get("attack_EV", 0),
        team_pokemon.get("defense_EV", 0),
        team_pokemon.get("sp_atk_EV", 0),
        team_pokemon.get("sp_def_EV", 0),
        team_pokemon.get("speed_EV", 0),
        team_pokemon.get("level", 100),
    ))

def update_team_pokemon():
    pass

def delete_team_pokemon():
    pass
