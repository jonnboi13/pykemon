"""
This file is for the functions to connect to the db.
"""

import duckdb
from importlib.resources import files


def get_connection() -> duckdb.DuckDBPyConnection:
    """Connect to the bundled pykemon DuckDB database.

    Returns a read-only DuckDB connection to the database containing
    all Pokémon, moves, abilities, items, natures, and status effects.

    Returns:
        A read-only connection to the pykemon database.

    Example:
        ```py
        from pykemon.db import get_connection

        con = get_connection()
        con.sql("SELECT name, total FROM pokemon LIMIT 5").pl()
        ```
    """
    path = files("pykemon.data").joinpath("pykemon.duckdb")
    return duckdb.connect(str(path), read_only=True)