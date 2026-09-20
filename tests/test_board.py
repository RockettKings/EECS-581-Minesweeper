"""
Prologue Comment
File: test_board.py
Description: Tests board.py, checking for correct board
             structure, safe first click, and adjacent
             mine counts.
Inputs:  difficulty, first-click row/column, mine count/mine position
Outputs: Pytest results of each test case
External sources: Original code with assistance by OpenAI 
                  ChatGPT for correctness. Logic is reviewed
                  and tested by the author.
Author: Khang Phan
Created: [Sept 15 2026]
"""

from board import Board
import pytest

#clears mines and adjacent counts so a test can place its own mines
def clear_board(board):
    #clear mines on board
    for tile in board.board:
        tile.isMine = False
        tile.isNumber = False
        tile.adjacent = 0

#checks board size, tile count, and mine count for each difficulty
@pytest.mark.parametrize("difficulty, rows, columns, mines", [
    (0, 10, 10, 10),
    (1, 16, 16, 40),
    (2, 16, 30, 99)
])
def test_board_structure(difficulty, rows, columns, mines):
    board = Board(difficulty, 1, 1)
    board.makeBoard()
    mineCount = sum(tile.isMine for tile in board.board)

    #test board dimensions
    assert board.dimension["row"] == rows
    assert board.dimension["column"] == columns

    #test total tiles/board size
    assert len(board.board) == rows*columns

    #test mine count
    assert mineCount == mines

#checks that a first click outside the board raises ValueError
@pytest.mark.parametrize("firstRow, firstCol", [
    (-1, 1),
    (1, -1),
    (10, 1),
    (1, 10)
])
def test_first_click_out_of_bounds(firstRow, firstCol):
    with pytest.raises(ValueError):
        Board(0, firstRow, firstCol)

#checks that mines cannot be placed off the board or in the safe zone
@pytest.mark.parametrize("index, firstRow, firstCol", [
    (-1, 1, 1),
    (100, 1, 1),
    (0, 1, 1),
    (10, 1, 1),
    (11, 1, 1)
])
def test_invalid_mine_placement(index, firstRow, firstCol):
    board = Board(0, firstRow, firstCol)
    assert not board.isValidPlacement(index, firstRow, firstCol)

#checks that mines can be placed on valid cells away from the first click
@pytest.mark.parametrize("index, firstRow, firstCol", [
    (2, 0, 0),
    (45, 0, 0),
    (90, 0, 0)
])
def test_valid_mine_placement(index, firstRow, firstCol):
    board = Board(0, firstRow, firstCol)
    assert board.isValidPlacement(index, firstRow, firstCol)

#checks that the first click and its neighbors are never mines
@pytest.mark.parametrize("row, column, safeTiles", [
    (1, 1, [0, 1, 2, 10, 12, 20, 21, 22]),
    (0, 7, [6, 7, 8, 16, 17, 18]),
    (9, 0, [80, 81, 91])
])
def test_safe_first_click(row, column, safeTiles):
    for _ in range(10):
        board = Board(0, row, column)
        board.makeBoard()

        for index in safeTiles:
            assert not board.board[index].isMine

#checks adjacent counts around a single placed mine
@pytest.mark.parametrize("mineTile, row, column, adjacentTiles", [
    (33, 1, 1, [22, 23, 24, 32, 34, 42, 43, 44]),
    (99, 1, 1, [88, 89, 98])
])
def test_adjacency_count(mineTile, row, column, adjacentTiles):
    board = Board(0, row, column)
    board.makeBoard()

    clear_board(board)
    board.board[mineTile].isMine = True
    board.addNumberAroundMines()

    for index in adjacentTiles:
        assert board.board[index].isNumber
        assert board.board[index].adjacent == 1
    assert board.board[mineTile].adjacent == 0

    for index, tile in enumerate(board.board):
        if index not in adjacentTiles and index != mineTile:
            assert tile.adjacent == 0

#checks adjacent counts when two mines share neighbors
def test_adjacency_count_multiple_mines():
    board = Board(0, 1, 1)
    board.makeBoard()

    clear_board(board)
    board.board[50].isMine = True
    board.board[61].isMine = True
    board.addNumberAroundMines()
    singleMineAdjacent = [40, 41, 52, 62, 70, 71, 72]
    doubleMineAdjacent = [51, 60]

    for index in singleMineAdjacent:
        assert board.board[index].isNumber
        assert board.board[index].adjacent == 1
    assert not board.board[50].isNumber
    #assert board.board[50].adjacent == 0

    for index in doubleMineAdjacent:
        assert board.board[index].isNumber
        assert board.board[index].adjacent == 2
    assert not board.board[61].isNumber
    #assert board.board[61].adjacent == 0