import polars as pl
import duckdb

def insert_team(con, team: dict):
    con.execute("""
        INSERT INTO team (team_name) VALUES (?)
    """, (team["team_name"],))

def update_team():
    pass

def delete_team():
    pass
