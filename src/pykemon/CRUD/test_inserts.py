"""
Pykemon Team Manager CLI
Handles base team seeding and interactive team/pokemon management.
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "data-raw"))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__))))

import duckdb
from build_db import make_db
from team import insert_team
from team_pokemon import insert_team_pokemon
from team_pokemon_move import insert_team_pokemon_move

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "src", "pykemon", "data", "pykemon.duckdb")


# ---------------------------------------------------------------------------
# Seed data
# ---------------------------------------------------------------------------

BASE_TEAMS = [
    {
        "team": {"team_name": "Fire Squad"},
        "pokemon": [
            {"pokemon_id": 6,   "ability_id": 1, "nature_id": 1},
            {"pokemon_id": 38,  "ability_id": 2, "nature_id": 2},
            {"pokemon_id": 59,  "ability_id": 1, "nature_id": 3},
            {"pokemon_id": 78,  "ability_id": 1, "nature_id": 4},
            {"pokemon_id": 136, "ability_id": 2, "nature_id": 5},
            {"pokemon_id": 145, "ability_id": 3, "nature_id": 6},
        ],
        "moves": [
            [53, 94, 76, 14],
            [53, 86, 76, 50],
            [53, 24, 76, 44],
            [53, 76, 50, 32],
            [53, 44, 76, 14],
            [86, 97, 57, 65],
        ],
    },
    {
        "team": {"team_name": "Water Warriors"},
        "pokemon": [
            {"pokemon_id": 9,   "ability_id": 4, "nature_id": 7},
            {"pokemon_id": 55,  "ability_id": 5, "nature_id": 8},
            {"pokemon_id": 62,  "ability_id": 4, "nature_id": 9},
            {"pokemon_id": 121, "ability_id": 6, "nature_id": 10},
            {"pokemon_id": 130, "ability_id": 7, "nature_id": 11},
            {"pokemon_id": 131, "ability_id": 8, "nature_id": 12},
        ],
        "moves": [
            [57, 58, 99, 14],
            [57, 58, 94, 86],
            [57, 2,  67, 99],
            [57, 58, 94, 86],
            [57, 58, 44, 82],
            [57, 58, 44, 86],
        ],
    },
    {
        "team": {"team_name": "Psychic Masters"},
        "pokemon": [
            {"pokemon_id": 65,  "ability_id": 9,  "nature_id": 13},
            {"pokemon_id": 80,  "ability_id": 10, "nature_id": 14},
            {"pokemon_id": 96,  "ability_id": 9,  "nature_id": 15},
            {"pokemon_id": 103, "ability_id": 11, "nature_id": 16},
            {"pokemon_id": 122, "ability_id": 9,  "nature_id": 17},
            {"pokemon_id": 124, "ability_id": 12, "nature_id": 18},
        ],
        "moves": [
            [94, 86, 50, 100],
            [94, 57, 58, 44],
            [94, 86, 50, 100],
            [94, 76, 78, 99],
            [94, 86, 50, 100],
            [94, 58, 78, 44],
        ],
    },
]


# ---------------------------------------------------------------------------
# DB helpers
# ---------------------------------------------------------------------------

def get_teams(con):
    return con.execute("SELECT team_id, team_name FROM team").fetchall()


def get_team_pokemon(con, team_id):
    return con.execute("""
        SELECT tp.team_pokemon_id, TRIM(p.name, '"') AS name, tp.pokemon_id
        FROM team_pokemon tp
        JOIN pokemon p ON tp.pokemon_id = p.pokemon_id
        WHERE tp.team_id = ?
    """, (team_id,)).fetchall()


def get_pokemon_moves(con, team_pokemon_id):
    return con.execute("""
        SELECT tpm.team_pokemon_move_id, m.move_name, tpm.move_id
        FROM team_pokemon_move tpm
        JOIN move m ON tpm.move_id = m.move_id
        WHERE tpm.team_pokemon_id = ?
    """, (team_pokemon_id,)).fetchall()


def get_abilities_for_pokemon(con, pokemon_id):
    return con.execute("""
        SELECT a.ability_id, a.ability_name
        FROM pokemon_ability pa
        JOIN ability a ON pa.ability_id = a.ability_id
        WHERE pa.pokemon_id = ?
    """, (pokemon_id,)).fetchall()


def get_all_natures(con):
    return con.execute("SELECT nature_id, name FROM nature ORDER BY nature_id").fetchall()


def get_first_move_for_pokemon(con, pokemon_id):
    return con.execute("""
        SELECT move_id FROM pokemon_move
        WHERE pokemon_id = ?
        ORDER BY pokemon_move_id
        LIMIT 1
    """, (pokemon_id,)).fetchone()


def pokemon_can_learn_move(con, pokemon_id, move_id):
    result = con.execute("""
        SELECT COUNT(*) FROM pokemon_move
        WHERE pokemon_id = ? AND move_id = ?
    """, (pokemon_id, move_id)).fetchone()
    return result[0] > 0


def get_move_by_name(con, move_name):
    return con.execute("""
        SELECT move_id, move_name FROM move
        WHERE LOWER(move_name) = LOWER(?)
    """, (move_name,)).fetchone()


# ---------------------------------------------------------------------------
# Seed base teams
# ---------------------------------------------------------------------------

def seed_base_teams(con):
    for base in BASE_TEAMS:
        exists = con.execute("SELECT COUNT(*) FROM team WHERE team_name = ?",
                             (base["team"]["team_name"],)).fetchone()[0]
        if exists:
            print(f"  Skipping '{base['team']['team_name']}' — already exists.")
            continue

        insert_team(con, base["team"])
        team_id = con.execute("SELECT team_id FROM team WHERE team_name = ?",
                              (base["team"]["team_name"],)).fetchone()[0]

        for pkmn in base["pokemon"]:
            insert_team_pokemon(con, {
                "team_id":    team_id,
                "pokemon_id": pkmn["pokemon_id"],
                "ability_id": pkmn["ability_id"],
                "nature_id":  pkmn["nature_id"],
            })

        tp_ids = [row[0] for row in con.execute("""
            SELECT team_pokemon_id FROM team_pokemon
            WHERE team_id = ?
            ORDER BY team_pokemon_id
        """, (team_id,)).fetchall()]

        for i, move_ids in enumerate(base["moves"]):
            moves = [{"team_pokemon_id": tp_ids[i], "move_id": m} for m in move_ids]
            insert_team_pokemon_move(con, moves)

        print(f"  Seeded team: {base['team']['team_name']}")


# ---------------------------------------------------------------------------
# Input helpers
# ---------------------------------------------------------------------------

def prompt_int(prompt, min_val, max_val, allow_quit=True):
    """Prompt for an integer. Returns None if user types 'q'."""
    while True:
        raw = input(prompt).strip()
        if allow_quit and raw.lower() == "q":
            return None
        try:
            val = int(raw)
            if min_val <= val <= max_val:
                return val
            print(f"  Please enter a number between {min_val} and {max_val} (or 'q' to cancel).")
        except ValueError:
            print("  Invalid input — please enter a number (or 'q' to cancel).")


def search_and_select_pokemon(con):
    """Search for a pokemon and return (pokemon_id, pokemon_name) or None if cancelled."""
    while True:
        search = input("Search pokemon by name (or 'q' to cancel): ").strip()
        if search.lower() == "q":
            return None

        matches = con.execute("""
            SELECT pokemon_id, TRIM(name, '"') AS name FROM pokemon
            WHERE LOWER(TRIM(name, '"')) LIKE LOWER(?)
            ORDER BY name
        """, (f"%{search}%",)).fetchall()

        if not matches:
            print("  No pokemon found. Try again.")
            continue

        print("\nMatches:")
        for i, (pid, name) in enumerate(matches, 1):
            print(f"  {i}. {name} (#{pid})")

        choice = prompt_int("Select number (0 to search again, q to cancel): ", 0, len(matches))
        if choice is None:
            return None
        if choice == 0:
            continue

        pokemon_id, pokemon_name = matches[choice - 1]
        confirm = input(f"  Confirm: {pokemon_name}? (y/n/q): ").strip().lower()
        if confirm == "q":
            return None
        if confirm == "y":
            return pokemon_id, pokemon_name


def select_ability(con, pokemon_id):
    """Prompt user to select an ability. Returns ability_id or None if cancelled."""
    abilities = get_abilities_for_pokemon(con, pokemon_id)
    if not abilities:
        print("  No abilities found for this pokemon.")
        return None

    print("\nAbilities:")
    for i, (aid, aname) in enumerate(abilities, 1):
        print(f"  {i}. {aname}")

    choice = prompt_int("Select ability (or 'q' to cancel): ", 1, len(abilities))
    if choice is None:
        return None
    return abilities[choice - 1][0]


def select_nature(con):
    """Prompt user to select a nature. Returns nature_id or None if cancelled."""
    natures = get_all_natures(con)
    print("\nNatures:")
    for nature_id, name in natures:
        print(f"  {nature_id:2}. {name}")

    choice = prompt_int("Select nature 1-25 (or 'q' to cancel): ", 1, 25)
    if choice is None:
        return None
    return natures[choice - 1][0]


# ---------------------------------------------------------------------------
# Team actions
# ---------------------------------------------------------------------------

def create_new_team(con):
    print("\n--- New Team ---")
    team_name = input("Enter team name (or 'q' to cancel): ").strip()
    if not team_name or team_name.lower() == "q":
        return

    exists = con.execute("SELECT COUNT(*) FROM team WHERE team_name = ?", (team_name,)).fetchone()[0]
    if exists:
        print(f"  A team named '{team_name}' already exists.")
        return

    insert_team(con, {"team_name": team_name})
    print(f"  Team '{team_name}' created!")


def add_pokemon_to_team(con, team_id):
    current = get_team_pokemon(con, team_id)
    if len(current) >= 6:
        print("  Team is full (6 pokemon max).")
        return

    print("\n--- Add Pokemon ---")
    result = search_and_select_pokemon(con)
    if result is None:
        return
    pokemon_id, pokemon_name = result

    ability_id = select_ability(con, pokemon_id)
    if ability_id is None:
        return

    nature_id = select_nature(con)
    if nature_id is None:
        return

    insert_team_pokemon(con, {
        "team_id":    team_id,
        "pokemon_id": pokemon_id,
        "ability_id": ability_id,
        "nature_id":  nature_id,
    })

    tp_id = con.execute("""
        SELECT team_pokemon_id FROM team_pokemon
        WHERE team_id = ? AND pokemon_id = ?
        ORDER BY team_pokemon_id DESC LIMIT 1
    """, (team_id, pokemon_id)).fetchone()[0]

    first_move = get_first_move_for_pokemon(con, pokemon_id)
    if first_move:
        insert_team_pokemon_move(con, [{"team_pokemon_id": tp_id, "move_id": first_move[0]}])

    print(f"  {pokemon_name} added!")


def change_pokemon(con, team_id, team_pokemon_id, old_name):
    """Replace a pokemon in a team slot with a new one."""
    print(f"\n--- Replace {old_name} ---")
    result = search_and_select_pokemon(con)
    if result is None:
        return

    pokemon_id, pokemon_name = result

    ability_id = select_ability(con, pokemon_id)
    if ability_id is None:
        return

    nature_id = select_nature(con)
    if nature_id is None:
        return

    # remove old pokemon and its moves
    con.execute("DELETE FROM team_pokemon_move WHERE team_pokemon_id = ?", (team_pokemon_id,))
    con.execute("DELETE FROM team_pokemon WHERE team_pokemon_id = ?", (team_pokemon_id,))

    # insert new pokemon
    insert_team_pokemon(con, {
        "team_id":    team_id,
        "pokemon_id": pokemon_id,
        "ability_id": ability_id,
        "nature_id":  nature_id,
    })

    tp_id = con.execute("""
        SELECT team_pokemon_id FROM team_pokemon
        WHERE team_id = ? AND pokemon_id = ?
        ORDER BY team_pokemon_id DESC LIMIT 1
    """, (team_id, pokemon_id)).fetchone()[0]

    first_move = get_first_move_for_pokemon(con, pokemon_id)
    if first_move:
        insert_team_pokemon_move(con, [{"team_pokemon_id": tp_id, "move_id": first_move[0]}])

    print(f"  {old_name} replaced with {pokemon_name}!")


def edit_pokemon_moves(con, team_pokemon_id, pokemon_id, pokemon_name):
    print(f"\n--- Edit Moves: {pokemon_name} ---")
    moves = get_pokemon_moves(con, team_pokemon_id)

    print("\nCurrent moves:")
    for i, (tpm_id, move_name, move_id) in enumerate(moves, 1):
        print(f"  {i}. {move_name}")
    for i in range(len(moves) + 1, 5):
        print(f"  {i}. (empty)")

    slot = prompt_int("Select move slot to replace 1-4 (or 'q' to cancel): ", 1, 4)
    if slot is None:
        return

    # if slot has a move, we'll replace it; if empty we just insert
    tpm_id_to_replace = moves[slot - 1][0] if slot <= len(moves) else None

    # show top 10 moves by power
    top_moves = con.execute("""
        SELECT DISTINCT m.move_name, m.power, m.type, m.category
        FROM pokemon_move pm
        JOIN move m ON pm.move_id = m.move_id
        WHERE pm.pokemon_id = ?
          AND m.power IS NOT NULL
        ORDER BY m.power DESC
        LIMIT 10
    """, (pokemon_id,)).fetchall()

    print(f"\nTop 10 moves for {pokemon_name} by power:")
    for move_name, power, mtype, category in top_moves:
        print(f"  {move_name:<20} Power: {power:<5} Type: {mtype:<10} Category: {category}")

    while True:
        move_name_input = input("\nEnter move name (or 'q' to cancel): ").strip()
        if move_name_input.lower() == "q":
            return

        move = get_move_by_name(con, move_name_input)
        if not move:
            print("  Move not found. Try again.")
            continue

        move_id, move_name = move
        if not pokemon_can_learn_move(con, pokemon_id, move_id):
            print(f"  Move unavailable for {pokemon_name}. Try again.")
            continue

        if tpm_id_to_replace:
            con.execute("DELETE FROM team_pokemon_move WHERE team_pokemon_move_id = ?", (tpm_id_to_replace,))
        insert_team_pokemon_move(con, [{"team_pokemon_id": team_pokemon_id, "move_id": move_id}])
        print(f"  Slot {slot} updated to {move_name}!")
        break


def edit_team(con, team_id, team_name):
    while True:
        print(f"\n--- Team: {team_name} ---")
        pokemon_list = get_team_pokemon(con, team_id)

        if pokemon_list:
            print("Pokemon:")
            for i, (tp_id, name, pid) in enumerate(pokemon_list, 1):
                moves = get_pokemon_moves(con, tp_id)
                move_names = ", ".join(m[1] for m in moves) if moves else "no moves"
                print(f"  {i}. {name} — [{move_names}]")
        else:
            print("  (no pokemon yet)")

        print("\nOptions:")
        if len(pokemon_list) < 6:
            print("  a. Add pokemon")
        if pokemon_list:
            print("  m. Change a pokemon's moves")
            print("  c. Change a pokemon")
        print("  b. Back")

        choice = input("Select: ").strip().lower()

        if choice == "a" and len(pokemon_list) < 6:
            add_pokemon_to_team(con, team_id)

        elif choice == "m" and pokemon_list:
            idx = prompt_int("Select pokemon number (or 'q' to cancel): ", 1, len(pokemon_list))
            if idx is None:
                continue
            tp_id, pname, pid = pokemon_list[idx - 1]
            edit_pokemon_moves(con, tp_id, pid, pname)

        elif choice == "c" and pokemon_list:
            idx = prompt_int("Select pokemon to replace (or 'q' to cancel): ", 1, len(pokemon_list))
            if idx is None:
                continue
            tp_id, pname, pid = pokemon_list[idx - 1]
            change_pokemon(con, team_id, tp_id, pname)

        elif choice == "b":
            break
        else:
            print("  Invalid option.")


# ---------------------------------------------------------------------------
# Main menu
# ---------------------------------------------------------------------------

def main_menu(con):
    while True:
        print("\n========== Pykemon Team Manager ==========")
        teams = get_teams(con)

        print("Teams:")
        for i, (tid, tname) in enumerate(teams, 1):
            print(f"  {i}. {tname}")
        print(f"  {len(teams) + 1}. + New team")
        print("  q. Quit")

        choice = input("\nSelect: ").strip().lower()

        if choice == "q":
            print("Goodbye!")
            break

        try:
            idx = int(choice)
        except ValueError:
            print("  Invalid option.")
            continue

        if idx == len(teams) + 1:
            create_new_team(con)
        elif 1 <= idx <= len(teams):
            team_id, team_name = teams[idx - 1]
            print(f"\nSelected: {team_name}")
            action = input("  [e]dit / [b]ack: ").strip().lower()
            if action == "q" or action == "b":
                continue
            if action == "e":
                edit_team(con, team_id, team_name)
        else:
            print("  Invalid option.")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    con = duckdb.connect(DB_PATH)
    make_db(con)

    print("Seeding base teams...")
    seed_base_teams(con)

    main_menu(con)
    con.close()