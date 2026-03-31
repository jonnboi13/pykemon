"""
This file biulds the duckdb database tables.
"""

import duckdb
import polars as pl

DB_PATH = "src/pykemon/data/pykemon.duckdb"


def make_db(con: duckdb.DuckDBPyConnection):
    """Create all tables in the database."""
    con.execute("CREATE SEQUENCE IF NOT EXISTS team_id_seq START 1")
    con.execute("CREATE SEQUENCE IF NOT EXISTS team_pokemon_id_seq START 1")
    con.execute("CREATE SEQUENCE IF NOT EXISTS team_pokemon_move_id_seq START 1")

    con.execute("""
        CREATE TABLE IF NOT EXISTS pokemon (
            pokemon_id      INTEGER PRIMARY KEY,
            number          INTEGER,
            name            VARCHAR,
            base_name       VARCHAR,
            form_name       VARCHAR,
            primary_type    VARCHAR,
            secondary_type  VARCHAR,
            total           INTEGER,
            hp              INTEGER,
            attack          INTEGER,
            defense         INTEGER,
            sp_atk          INTEGER,
            sp_def          INTEGER,
            speed           INTEGER,
            generation      INTEGER,
            link            VARCHAR,
            sprite_url      VARCHAR
        )
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS pokemon_move (
            pokemon_move_id  INTEGER PRIMARY KEY,
            pokemon_id       INTEGER,
            move_id          INTEGER,
            generation       INTEGER,
            game             VARCHAR,
            method           VARCHAR,
            detail           VARCHAR
        )
    """)

    con.execute("""
    CREATE TABLE IF NOT EXISTS move (
        move_id         INTEGER PRIMARY KEY,
        move_name       VARCHAR UNIQUE,
        type            VARCHAR,
        category        VARCHAR,
        power           INTEGER,
        accuracy        INTEGER,
        pp              INTEGER,
        makes_contact   BOOLEAN,
        introduced      INTEGER,
        effect          VARCHAR,
        z_effect        VARCHAR
    )
""")

    con.execute("""
    CREATE TABLE IF NOT EXISTS item (
        item_id     INTEGER PRIMARY KEY,
        name        VARCHAR,
        category    VARCHAR,
        effect      VARCHAR,
        sprite_url  VARCHAR
    )
""")

    con.execute("""
        CREATE TABLE IF NOT EXISTS ability (
            ability_id      INTEGER PRIMARY KEY,
            ability_name    VARCHAR UNIQUE,
            effect          VARCHAR
        )
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS pokemon_ability (
            pokemon_ability_id  INTEGER PRIMARY KEY,
            pokemon_id          INTEGER,
            ability_id          INTEGER,
            slot                VARCHAR
        )
    """)

    con.execute("""
    CREATE TABLE IF NOT EXISTS nature (
        nature_id   INTEGER PRIMARY KEY,
        name        VARCHAR UNIQUE,
        stat_up     VARCHAR,
        stat_down   VARCHAR
    )
""")

    con.execute("""
        CREATE TABLE IF NOT EXISTS status_effect (
            status_effect_id    INTEGER PRIMARY KEY,
            name                VARCHAR UNIQUE,
            abbreviation        VARCHAR,
            end_of_turn_damage  FLOAT,
            speed_modifier      FLOAT,
            attack_modifier     FLOAT,
            max_turns           INTEGER,
            effect              VARCHAR
        )
    """)


def get_gen_from_number(number: int) -> int:
    if number <= 151:
        return 1
    elif number <= 251:
        return 2
    elif number <= 386:
        return 3
    elif number <= 493:
        return 4
    elif number <= 649:
        return 5
    elif number <= 721:
        return 6
    elif number <= 809:
        return 7
    elif number <= 905:
        return 8
    else:
        return 9


def insert_pokemon(con, df: pl.DataFrame):
    df = df.with_row_index("pokemon_id", offset=1)

    form_gen_map = {
        "Mega": 6,
        "Alolan": 7,
        "Galarian": 8,
        "Hisuian": 9,
        "Paldean": 9,
    }

    def get_form_gen(form_name):
        if form_name is None:
            return None
        for key, gen in form_gen_map.items():
            if key in form_name:
                return gen
        return None

    df = (
        df.with_columns(
            pl.col("number")
            .map_elements(get_gen_from_number, return_dtype=pl.Int32)
            .alias("generation")
        )
        .with_columns(
            pl.col("form_name")
            .map_elements(get_form_gen, return_dtype=pl.Int32)
            .alias("form_gen")
        )
        .with_columns(pl.coalesce(["form_gen", "generation"]).alias("generation"))
        .drop("form_gen")
    )

    con.execute("""
        INSERT INTO pokemon SELECT * FROM df
    """)


def insert_items(con, df: pl.DataFrame):
    df = df.with_row_index("item_id", offset=1)
    con.execute("INSERT INTO item SELECT * FROM df")


def insert_pokemon_moves(con, df: pl.DataFrame):
    df = df.with_row_index("pokemon_move_id", offset=1)
    con.execute("INSERT INTO pokemon_move SELECT * FROM df")


def insert_moves(con, df: pl.DataFrame):
    df = df.with_row_index("move_id", offset=1)
    con.execute("INSERT INTO move SELECT * FROM df")


def insert_abilities(con, df: pl.DataFrame):
    df = df.with_row_index("ability_id", offset=1)
    con.execute("INSERT INTO ability SELECT * FROM df")


def insert_pokemon_abilities(con, df: pl.DataFrame):
    df = df.with_row_index("pokemon_ability_id", offset=1)
    con.execute("INSERT INTO pokemon_ability SELECT * FROM df")


def insert_natures(con, df: pl.DataFrame):
    df = df.with_row_index("nature_id", offset=1)
    con.execute("INSERT INTO nature SELECT * FROM df")


def insert_status_effects(con, df: pl.DataFrame):
    df = df.with_row_index("status_effect_id", offset=1)
    con.execute("INSERT INTO status_effect SELECT * FROM df")


def insert_team(con, df: pl.DataFrame):
    df = df.with_row_index("team_id", offset=1)
    con.execute("INSERT INTO team SELECT * FROM df")


def insert_team_pokemon(con, df: pl.DataFrame):
    df = df.with_row_index("team_pokemon_id", offset=1)
    con.execute("INSERT INTO team_pokemon SELECT * FROM df")


def insert_team_pokemon_move(con, df: pl.DataFrame):
    df = df.with_row_index("team_pokemon_move_id", offset=1)
    con.execute("INSERT INTO team_pokemon_move SELECT * FROM df")


def print_schema(con: duckdb.DuckDBPyConnection):
    """Print all tables and their columns."""
    tables = con.execute("SHOW TABLES").fetchall()
    for (table,) in tables:
        print(f"\n{table}")
        print("-" * 40)
        cols = con.execute(f"DESCRIBE {table}").fetchall()
        for col in cols:
            print(f"  {col[0]:<20} {col[1]}")
