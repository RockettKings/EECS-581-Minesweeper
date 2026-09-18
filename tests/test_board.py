from board import Board
import pytest

def test_easy_board_dimensions():
    board = Board(0, 1, 1)

    assert board.dimension["row"] == 9
    assert board.dimension["column"] == 9

def test_mid_board_dimensions():
    board = Board(1, 1, 1)
    assert board.dimension["row"] == 16
    assert board.dimension["column"] == 16

def test_hard_board_dimensions():
    board = Board(2, 1, 1)
    assert board.dimension["row"] == 16
    assert board.dimension["column"] == 30

def test_easy_board_size():
    board = Board(0, 1, 1)
    board.makeBoard()
    assert len(board.board) == 9*9

def test_mid_board_size():
    board = Board(1, 1, 1)
    board.makeBoard()
    assert len(board.board) == 16*16

def test_hard_board_size():
    board = Board(2, 1, 1)
    board.makeBoard()
    assert len(board.board) == 16*30

def test_easy_mine_count():
    board = Board(0, 1, 1)
    board.makeBoard()
    mineCount = sum(tile.isMine for tile in board.board)
    assert mineCount == 10

def test_mid_mine_count():
    board = Board(1, 1, 1)
    board.makeBoard()
    mineCount = sum(tile.isMine for tile in board.board)
    assert mineCount == 40

def test_hard_mine_count():
    board = Board(2, 1, 1)
    board.makeBoard()
    mineCount = sum(tile.isMine for tile in board.board)
    assert mineCount == 99

def test_negative_row_click():
    with pytest.raises(ValueError):
        Board(0, -1, 1)

def test_negative_col_click():
    with pytest.raises(ValueError):
        Board(0, 1, -1)

def test_click_out_of_bounds():
    with pytest.raises(ValueError):
        Board(0, 3, 9)

def test_negative_placement():
    board = Board(0, 1, 1)
    assert not board.isValidPlacement(-1, 1, 1)

def test_placement_out_of_bounds():
    board = Board(0, 4, 5)
    assert not board.isValidPlacement(81, 4, 5)

def test_invalid_placement():
    board = Board(0, 1, 1)
    assert not board.isValidPlacement(0, 1, 1)
    assert not board.isValidPlacement(10, 1, 1)


def test_valid_placement():
    board = Board(0, 0, 0)
    assert board.isValidPlacement(45, 0, 0)
    assert board.isValidPlacement(3, 0, 0)

def test_first_click_mines():
    board = Board(0, 1, 1)
    board.makeBoard()

    assert not board.board[0].isMine
    assert not board.board[1].isMine
    assert not board.board[2].isMine
    assert not board.board[9].isMine
    assert not board.board[10].isMine
    assert not board.board[11].isMine
    assert not board.board[18].isMine
    assert not board.board[19].isMine
    assert not board.board[20].isMine