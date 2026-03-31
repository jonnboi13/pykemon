import polars as pl
import duckdb

def insert_team_pokemon_move(con, team_pokemon_moves: list[dict]):
    con.executemany("""
        INSERT INTO team_pokemon_move (team_pokemon_id, move_id)
        VALUES (?, ?)
    """, [(r["team_pokemon_id"], r["move_id"]) for r in team_pokemon_moves])

def update_team_pokemon_move():
    pass

def delete_team_pokemon_move():
    pass
