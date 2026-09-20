# Interface Contract

The UI may talk to the backend only through `GameManager`.
That object is the interface contract. Backend internals (`Board`,
`GameState` mutators, flood fill, mine placement) are not part of the
UI API.

This contract is taken from the current `input_handler.py` /
`display.py` call sites so Teams 1 and 2 can stay aligned.

## Allowed `GameManager` methods

The frontend may construct a manager and call only these methods:

```text
GameManager(difficulty: int) -> GameManager
reveal(row: int, column: int) -> Tile | None
toggle_flag(row: int, column: int) -> None
get_state() -> GameState
get_board() -> Board | None
```

`difficulty` is `0` (Beginner), `1` (Intermediate), or `2` (Expert).

Restart is allowed by constructing a new `GameManager` with the same
difficulty. `reset()` and `start_game()` exist on the manager but are
**not** part of the UI contract; the current UI does not call them.

## Method rules

### `GameManager(difficulty)`
- Creates a playable game in the `PLAYING` state.
- `get_board()` is `None` until the first successful `reveal`.
- Invalid difficulty raises `ValueError`.

### `reveal(row, column)`
- Uncovers the cell at `(row, column)`.
- The first reveal builds the board and is first-click safe: the
  clicked cell and its neighbors are never mines.
- After the first reveal, `get_state().first_move` is `False`.
- Does nothing (`None`) if the game is over, the cell is already
  revealed, or the cell is flagged.
- Out-of-bounds positions raise `ValueError`.
- Revealing a mine marks the game `LOST` and reveals all mines.
- Revealing the last safe cell marks the game `WON`.

### `toggle_flag(row, column)`
- Flags or unflags a covered cell.
- Does nothing if the game is over, the board does not exist yet,
  or the cell is already revealed.
- Out-of-bounds positions raise `ValueError`.
- Updates `get_state().flags_placed` and `get_state().flags_remaining`.

### `get_state()`
- Returns the current `GameState`. The UI may **read** these fields:

| Field | Meaning |
|---|---|
| `difficulty` | `0`, `1`, or `2` |
| `rows`, `columns` | board size for the selected difficulty |
| `mine_count` | total mines |
| `flags_placed` | flags currently on the board |
| `flags_remaining` | `max(0, mine_count - flags_placed)` |
| `first_move` | `True` until the first `reveal` |
| `status` | `GameStatus.PLAYING`, `WON`, or `LOST` |
| `is_active` | `True` while `status` is `PLAYING` |
| `is_game_over` | `True` when `WON` or `LOST` |

The UI must not call `GameState` mutators (`complete_first_move`,
`record_flag_placed`, `record_flag_removed`, `mark_won`, `mark_lost`,
`reset`). Those are backend-only.

### `get_board()`
- Returns `None` before the first reveal.
- After the first reveal, returns the `Board`. Display may read:

| Field | Meaning |
|---|---|
| `board.board` | list of `Tile` objects, row-major |
| `board.dimension["row"]` / `["column"]` | grid size |
| `tile.revealed` | cell has been uncovered |
| `tile.isFlagged` | cell is flagged |
| `tile.isMine` | cell contains a mine |
| `tile.adjacent` | neighboring mine count |
| `tile.isNumber` | `True` when `adjacent > 0` and not a mine |

The UI must not call `Board.makeBoard()` or placement helpers.

## Current difficulty sizes

These are the values `get_state()` reports today:

| Index | Label | Size | Mines |
|---|---|---|---|
| 0 | Beginner | 10×10 | 10 |
| 1 | Intermediate | 16×16 | 40 |
| 2 | Expert | 16×30 | 99 |

`TODO.md` still lists Beginner as 9×9. The running code is 10×10.
The contract follows the running code until the teams change it.

## Not in the contract

The UI must not call:

- `GameManager._initialize_board`, `_get_tile`, `_flood_fill`
- `GameManager.is_valid_position`, `check_win`, `reveal_all_mines`
- `GameManager.start_game`, `GameManager.reset`
- any `Board` or `GameState` method listed as backend-only above
