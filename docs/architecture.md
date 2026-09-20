# Minesweeper — System Architecture

## Overview

Minesweeper is a single-player game on a grid whose size is set by difficulty. The player uncovers cells to reveal numbers indicating nearby mines and flags cells they suspect are mines. The game is won by uncovering every safe cell and lost by uncovering a mine.

The system is organized into four parts. Keeping them separate lets the board, display, and input handling be changed independently.

## Components

- **Board Manager** — holds the grid and the state of every cell (covered, flagged, uncovered, mine) and each cell's count of adjacent mines. It builds the board and places the mines.
- **Game Logic** — applies the rules: uncovering cells, the chain reveal of empty areas, flagging, and deciding win or loss.
- **User Interface** — shows the grid, the mine count, and the game status, and presents the controls.
- **Input Handler** — takes the player's clicks and passes them to the Game Logic.

## Data Flow

```
Player
  │  click / right-click
  ▼
Input Handler ──validated action──► Game Logic ◄──► Board Manager
                                        │        (read / update cells)
                                        │ state changed
                                        ▼
                                  User Interface ──renders──► Player
```

## Key Data Structures

- **Grid** — a collection of cells whose dimensions are set by the chosen difficulty (Easy is 10×10; other difficulties use larger boards). Each cell knows whether it is a mine, whether it is flagged or uncovered, and how many neighboring mines it has. The selected difficulty sets both the grid size and the number of mines.
- **Game state** — the mine count, flags remaining, and whether the game is still playing, won, or lost.
