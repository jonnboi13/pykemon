# Using the Team Editor

The `team_editor()` function launches an interactive CLI for managing your Pokemon teams directly from the terminal.

## Getting Started

```python
from pykemon import team_editor

team_editor()
```

That's it. Running this will launch the team manager in your terminal.

## Main Menu

When you start the editor you'll see a list of your teams:

```
========== Pykemon Team Manager ==========
Teams:
  1. Fire Squad
  2. Water Warriors
  3. Psychic Masters
  4. + New team
  q. Quit
```

Type a number to select a team, the last number to create a new team, or `q` to quit.

## Creating a New Team

Select the `+ New team` option and enter a name when prompted:

```
--- New Team ---
Enter team name (or 'q' to cancel): My Team
  Team 'My Team' created!
```

Your new team will appear in the main menu immediately.

## Editing a Team

Select a team and type `e` to enter the editor:

```
Selected: My Team
  [e]dit / [b]ack: e
```

Inside the team editor you have three options:

- `a` — Add a pokemon (available when the team has fewer than 6)
- `m` — Change a pokemon's moves
- `c` — Replace a pokemon with a different one

## Adding a Pokemon

Type `a` and search by name:

```
Search pokemon by name (or 'q' to cancel): Bulbasaur

Matches:
  1. Bulbasaur (#1)
Select number (0 to search again, q to cancel): 1
  Confirm: Bulbasaur? (y/n/q): y
```

You'll then be prompted to select an ability from the ones available for that pokemon, and a nature from the full list of 25. Once confirmed, the pokemon is added to your team with its first learnable move.

## Editing Moves

Type `m`, select a pokemon, then select a move slot (1-4):

```
Current moves:
  1. Tackle
  2. (empty)
  3. (empty)
  4. (empty)

Top 10 moves for Bulbasaur by power:
  Solar Beam           Power: 120   Type: Grass      Category: Special
  ...

Enter move name (or 'q' to cancel): Solar Beam
  Slot 2 updated to Solar Beam!
```

If you enter a move the pokemon can't learn, you'll get a message and can try again.

## Replacing a Pokemon

Type `c` and select the slot you want to replace. You'll go through the same search and confirm flow as adding a pokemon. The old pokemon and its moves are removed and replaced with the new one.

## Notes

- Teams are capped at 6 pokemon
- All changes are saved to the database immediately
- Type `q` at any prompt to cancel and go back
