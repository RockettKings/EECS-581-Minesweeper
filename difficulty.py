"""
Prologue Comment
File: difficulty.py
Description: Defines the difficulty presets for the Minesweeper board.
             Each preset stores the grid size (rows and columns) and the
             number of mines. Provides BEGINNER, INTERMEDIATE, and EXPERT
             configurations used by the Board class.
Inputs:  rows, columns, and mineCount when a Difficulty is created.
Outputs: Difficulty objects (BEGINNER, INTERMEDIATE, EXPERT), each
         exposing gridSize ({"row", "column"}) and mineCount.
External sources: None — original code.
Author: Jaycob Campos
Created: [sept 14 2026]
"""


# holds the configuration for one difficulty level
class Difficulty:
    def __init__(self, rows, columns, mineCount):
        self.gridSize = {"row": rows, "column": columns}
        self.mineCount = mineCount

# preset difficulty levels used throughout the game.
BEGINNER = Difficulty(10, 10, 10)
INTERMEDIATE = Difficulty(16, 16, 40)
EXPERT = Difficulty(16, 30, 99)

