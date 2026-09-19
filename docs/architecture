
Overview
Minesweeper is a single player game on a fixed grid based on difficulty. The player uncovers cells to reveal 
numbers indicating nearby mines and flags cells they suspect are mines. The games is won by uncovering every 
safe cell and lost by uncovering a mine. The system is organized into four parts. Keeping them separate lets
the board, display**,** and input handling be changed independently.

Components

Board Manager - holds the grid and the state of every cell (covered, flagged, uncovered, mine) and each cell's
count of adjacent mines. It builds the board and places the mines.

Game Logic - Applies the rules: uncovering cells, the chain reveal of empty areas, flagging, and deciding win 
or loss.

User Interface - shows the grid, the mine count, and the game status, and presents the controls.

Input Handler - takes the player's clicks and passes them to the Game Logic.

Data flow

Player
  │  click / right-click
  ▼
Input Handler ──validated action──► Game Logic ◄──► Board Manager
                                        │        (read / update cells)
                                        │ state changed
                                        ▼
                                  User Interface ──renders──► Player

Key data structures

Grid - a collection of cells whose dimensions are set by the chosen difficulty (Easy is 10x10; other 
difficulties use larger boards). Each cell knows whether it is a mine, whether it is flagged or uncovered,
and how many neighboring mines it has. The selected difficulty sets both the grid size and the number of 
mines. Guarantees that the first click is safe.

Game state - the mine count, flags remaining, and whether the game is still playing, won or lost.
