"""
Prologue Comment
File: test_display_helpers.py
Description: Tests display.py helpers against the real GameManager,
             Board, and Tile objects from the interface contract.
Inputs: Real tiles/board state, GameStatus values
Outputs: Pytest results of each test case
External sources: None
Author: Jon Kazmaier
Created: [Sept 20 2026]
"""

import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import display
from board import Tile
from game_manager import GameManager
from game_state import GameStatus


#starts a beginner game and reveals one cell so the board exists
def live_manager():
    manager = GameManager(0)
    manager.reveal(0, 0)
    return manager


#returns the tile at a row and column on the flat board list
def tile_at(board, row, col):
    width = board.dimension["column"]
    return board.board[row * width + col]


#checks that _get_cell reads a tile from the real Board object
def test_get_cell_reads_contract_board_after_first_reveal():
    manager = live_manager()
    board = manager.get_board()
    expected = tile_at(board, 0, 0)

    cell = display._get_cell(board, 0, 0)

    assert cell is expected
    assert cell.revealed is True


#checks that _cell_info reads a revealed numbered tile
def test_cell_info_reads_revealed_number_from_tile():
    tile = Tile()
    tile.revealed = True
    tile.adjacent = 3

    revealed, flagged, is_mine, number = display._cell_info(None, tile, 0, 0)

    assert revealed is True
    assert flagged is False
    assert is_mine is False
    assert number == 3


#checks that _cell_info reads the isFlagged field
def test_cell_info_reads_flagged_tile():
    tile = Tile()
    tile.isFlagged = True

    revealed, flagged, is_mine, number = display._cell_info(None, tile, 0, 0)

    assert revealed is False
    assert flagged is True
    assert is_mine is False


#checks that _cell_info reads the isMine field
def test_cell_info_reads_revealed_mine():
    tile = Tile()
    tile.revealed = True
    tile.isMine = True

    revealed, flagged, is_mine, number = display._cell_info(None, tile, 0, 0)

    assert revealed is True
    assert is_mine is True


#checks that a new tile is treated as hidden and not a mine
def test_cell_info_reads_hidden_blank_tile():
    tile = Tile()

    revealed, flagged, is_mine, number = display._cell_info(None, tile, 0, 0)

    assert revealed is False
    assert flagged is False
    assert is_mine is False
    assert number in (None, 0)


#checks that _count_flags matches a flag placed through GameManager
def test_count_flags_matches_flagged_tiles_on_real_board():
    manager = live_manager()
    board = manager.get_board()
    width = board.dimension["column"]
    hidden = next(tile for tile in board.board if not tile.revealed)
    index = board.board.index(hidden)
    row, col = divmod(index, width)

    manager.toggle_flag(row, col)

    assert display._count_flags(manager.get_state(), board) == 1
    assert manager.get_state().flags_placed == 1


#checks that _get_total_mines reads mine_count from GameState
def test_get_total_mines_reads_state_mine_count():
    manager = GameManager(0)
    state = manager.get_state()

    assert display._get_total_mines(state) == state.mine_count == 10


#checks the win and loss overlay strings
def test_game_over_message_for_win_and_loss():
    won = GameManager(0).get_state()
    won.status = GameStatus.WON
    lost = GameManager(0).get_state()
    lost.status = GameStatus.LOST

    assert display._game_over_message(won) == "You Win!"
    assert display._game_over_message(lost) == "Game Over"
