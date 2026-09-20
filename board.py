
"""
Prologue Comment
File: board.py
Description: Generates the Minesweeper board. Builds the grid of Tile
             objects, randomly places mines while keeping a safe zone
             around the player's first click, and computes each cell's
             count of adjacent mines.
Inputs:  difficulty (int: 0/1/2), and the first-clicked row and column.
Outputs: A fully built board (list of Tile objects) with mines placed
         and adjacency numbers set, returned by makeBoard().
External sources: Code is original. Claude was used as a logic and conceptual
checker. Verifying edge cases, and confirming correctness. 
Author: Jaycob Campos
Created: [Sept 14 2026]
"""

from difficulty import BEGINNER
from difficulty import INTERMEDIATE
from difficulty import EXPERT
from random import randint

class Tile:
    def __init__(self):
        self.isMine = False
        self.isNumber = False
        self.revealed = False
        self.isFlagged = False
        self.adjacent = 0


class Board:
    # Builds a board for the given difficulty. Requires the first click position
    # Location up front so a 3x3 grid can be formed around the starting position 
    # to make sure no mines get placed around the start. 
    def __init__(self, difficulty, clickedRow, clickedColumn):
        self.difficulty = difficulty
        self.clickedRow = clickedRow
        self.clickedColumn = clickedColumn

        self.dimension = self.setDimension(difficulty)
        self.mineCount = self.setMineCount(difficulty)

        self.board = []

        self.validateClick()

    def validateClick(self):
        if self.clickedRow < 0 or self.clickedRow >= self.dimension["row"]:
            raise ValueError(
                f"First click is not within the board dimensions for Row."
            )

        if self.clickedColumn < 0 or self.clickedColumn >= self.dimension["column"]:
            raise ValueError(
                f"First click is not within the board dimensions for Column."
            )

    def isValidPlacement(self, index, startingRow, startingColumn):
        width = self.dimension["column"]
        totalCells = self.dimension["row"] * self.dimension["column"]

        # checking to make sure index isn't out of the board
        # Also checks that board isn't broken
        if width <= 0 or index < 0 or index >= totalCells:
            return False

        row = index // width
        column = index % width

        # Makes sure the index isn't within a 3x3 grid of starting click
        if abs(row - startingRow) <= 1 and abs(column - startingColumn) <= 1:
            return False

        return True

    def setMineCount(self, difficulty):
        match difficulty:
            case 0:
                return BEGINNER.mineCount
            case 1:
                return INTERMEDIATE.mineCount
            case 2:
                return EXPERT.mineCount

        return None

    def setDimension(self, difficulty):
        match difficulty:
            case 0:
                return BEGINNER.gridSize
            case 1:
                return INTERMEDIATE.gridSize
            case 2:
                return EXPERT.gridSize

        return None

    # Fills the baord with tiles then places mines and lastly computes adjacenty counts
    # then returns the completed board.
    def makeBoard(self):
        totalCells = (self.dimension["row"] * self.dimension["column"])

        for _ in range(totalCells):
            self.board.append(Tile())

        self.placeMines()
        self.addNumberAroundMines()

        return self.board

    def placeMines(self):
        placedMineCount = 0
        index = 0
        # inserting the mines at the front of the board
        # Not allowing the mines to be placed within a 3x3 grid of the
        # start click
        while placedMineCount < self.mineCount:
            if self.isValidPlacement(index, self.clickedRow, self.clickedColumn):
                self.board[index].isMine = True
                placedMineCount += 1

            index += 1

        # using yates-fisher shuffle to move mines around the board
        for i in range(len(self.board) - 1, -1, -1):
            if not self.isValidPlacement(i, self.clickedRow, self.clickedColumn):
                continue

            randomIndex = randint(0, i)
            while not self.isValidPlacement(randomIndex, self.clickedRow, self.clickedColumn):
                randomIndex = randint(0, i)

            temp = self.board[i]
            self.board[i] = self.board[randomIndex]
            self.board[randomIndex] = temp

    def addNumberAroundMines(self):
        width = self.dimension["column"]
        height = self.dimension["row"]

        for index in range(len(self.board)):
            if not self.board[index].isMine:
                continue

            row = index // width
            column = index % width

            # checking around the index to increment it's adjacent value

            # top-left
            if row - 1 >= 0 and column - 1 >= 0:
                self.board[(row - 1) * width + (column - 1)].adjacent += 1
            # top
            if row - 1 >= 0:
                self.board[(row - 1) * width + column].adjacent += 1
            # top-right
            if row - 1 >= 0 and column + 1 < width:
                self.board[(row - 1) * width + (column + 1)].adjacent += 1
            # left
            if column - 1 >= 0:
                self.board[row * width + (column - 1)].adjacent += 1
            # right
            if column + 1 < width:
                self.board[row * width + (column + 1)].adjacent += 1
            # bottom-left
            if row + 1 < height and column - 1 >= 0:
                self.board[(row + 1) * width + (column - 1)].adjacent += 1
            # bottom
            if row + 1 < height:
                self.board[(row + 1) * width + column].adjacent += 1
            # bottom-right
            if row + 1 < height and column + 1 < width:
                self.board[(row + 1) * width + (column + 1)].adjacent += 1

        for tile in self.board:
            if tile.adjacent > 0 and tile.isMine == False:
                tile.isNumber = True
