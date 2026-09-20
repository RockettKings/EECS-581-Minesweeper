# Minesweeper — Project 1 TODO

Work breakdown by team. **Rule of thumb: finish every necessity before anyone starts an idea.** A complete, well-tested basic game beats a half-finished fancy one on the rubric.

The three teams build against a shared **interface contract** (the methods the UI is allowed to call on the game object). Back end and front devs need to agree on this before any code is written. 

---

## Team 1 — Backend Logic

### Necessities
- [ ] **Grid data structure** — stores, for every cell: whether it's a mine, whether it's revealed, whether it's flagged, and how many neighboring mines it has.
- [ ] **Random mine placement** — a given number of mines scattered across the board, different every game.
- [ ] **Adjacency counts** — for each non-mine cell, count how many of its 8 neighbors are mines.
- [ ] **First-click safety** — the first cell clicked *and all 8 of its neighbors* are guaranteed not to be mines. (Implementation: place mines after the first click, or relocate a mine if the first click lands on one.)
- [ ] **Reveal logic** — uncover a cell and report what's there.
- [ ] **Flood fill** — when a revealed cell has zero adjacent mines, automatically reveal the connected region of other zeros and their bordering numbers.
- [ ] **Flag toggling** — mark/unmark a cell as a suspected mine.
- [ ] **Win/loss detection** — loss when a mine is revealed; win when every non-mine cell is revealed.
- [ ] **Difficulty configs** — board dimensions and mine counts per difficulty:
  - Beginner — 9×9, 10 mines
  - Intermediate — 16×16, 40 mines
  - Expert — 16×30, 99 mines

### Ideas (only after necessities are done)
- [ ] **Chording** — clicking a satisfied number cell auto-reveals its remaining neighbors. Once a numbered cell has as many flags around it as its number (e.g., a "3" with 3 flags), clicking that number opens all its other neighbors in one action. The game checks only the flag *count*, not whether the flags are correct — so it speeds up play when flags are right and ends the game if a flag is wrong.
- [ ] **Hint system** — surface one provably safe cell on request.
- [ ] **Save/load** — persist an in-progress game or a high-score list to a file.

---

## Team 2 — UI and User Events

### Necessities
- [ ] **Render the grid** — draw the board and visually distinguish each cell state: hidden, revealed-number, revealed-blank, flagged, and mine.
- [ ] **Left-click to reveal** — reveals a cell by calling into the backend.
- [ ] **Right-click to flag** — flags/unflags a cell by calling into the backend.
- [ ] **Mine counter** — shows mines remaining (total mines minus flags placed). *(This is the same value as "flags left" — one display, not two.)*
- [ ] **Win/loss state** — a clear message or screen when the game ends, and input disabled once it's over.
- [ ] **New game / restart control** — start a fresh game without relaunching.
- [ ] **Difficulty selector** — let the player pick Beginner / Intermediate / Expert.
- [ ] **Timer** — counts up in seconds, starting on the first click and stopping when the game ends.

### Ideas (only after necessities are done)
- [ ] **Chord input** — middle-click or double-click a number to trigger the chording behavior (calls the backend `chord` method).
- [ ] **Sound effects and simple animations** — e.g., cascade reveal.

---

## Team 3 — Integration, QA, Testing

### Necessities
- [x] **Define and enforce the interface contract** — the exact set of methods the UI is allowed to call on the game object. Full text: `docs/interface_contract.md`. Enforced by `tests/test_interface_contract.py`. Signatures:
  - `GameManager(difficulty: int)`
  - `reveal(row: int, column: int) -> Tile | None`
  - `toggle_flag(row: int, column: int) -> None`
  - `get_state() -> GameState`
  - `get_board() -> Board | None`
- [ ] **Wire backend and UI together** — assemble a running game and keep it running as both sides change.
- [ ] **Unit tests** for the logic-heavy backend pieces: adjacency counts, flood fill, win/loss detection, first-click safety.
- [ ] **End-to-end sanity check** — play a full game (start → reveal → flag → win, and → loss) and confirm it behaves.
- [ ] **Bug tracking** — log issues, triage them, and verify fixes before closing.
- [ ] **Canvas submissions and the ACM/IEEE ethics write-up** required by the rubric.
