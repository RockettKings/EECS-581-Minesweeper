"""
Prologue Comment
File: test_input_handler.py
Description: Tests input_handler.py click routing, difficulty selection,
             reveal/flag mapping, restart/menu controls, and the timer.
Inputs: Click positions, mouse buttons, keyboard keys, difficulty index
Outputs: Pytest results of each test case
External sources: None
Author: Jon Kazmaier
Created: [Sept 19 2026]
"""

import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

from unittest.mock import MagicMock

import pygame
import pytest

import display
from input_handler import MinesweeperGame


def cell_click_pos(row, col):
    x = col * display.CELL_SIZE + display.CELL_SIZE // 2
    y = display.TOP_BAR_HEIGHT + row * display.CELL_SIZE + display.CELL_SIZE // 2
    return (x, y)


@pytest.fixture
def game():
    pygame.init()
    instance = MinesweeperGame()
    yield instance
    pygame.display.quit()


def test_game_starts_on_menu(game):
    assert game.screen_mode == "menu"
    assert game.manager is None
    assert game.start_ticks is None
    assert game.frozen_elapsed is None
    assert game.screen.get_size() == display.MENU_SIZE


@pytest.mark.parametrize("index", [0, 1, 2])
def test_menu_button_click_starts_selected_difficulty(game, index):
    button = display.menu_button_rect(index)

    game._handle_click(button.center, 1)

    assert game.screen_mode == "playing"
    assert game.manager is not None
    state = game.manager.get_state()
    assert state.difficulty == index
    assert state.first_move
    assert state.is_active
    assert game.start_ticks is None


def test_menu_click_outside_buttons_does_not_start_game(game):
    game._handle_click((1, 1), 1)

    assert game.screen_mode == "menu"
    assert game.manager is None


def test_left_click_maps_to_reveal(game):
    game._start_game(0)
    game.manager.reveal = MagicMock()

    game._handle_game_click(cell_click_pos(2, 3), 1)

    game.manager.reveal.assert_called_once_with(2, 3)


def test_right_click_maps_to_toggle_flag(game):
    game._start_game(0)
    game.manager.toggle_flag = MagicMock()

    game._handle_game_click(cell_click_pos(4, 1), 3)

    game.manager.toggle_flag.assert_called_once_with(4, 1)


def test_top_bar_click_is_ignored(game):
    game._start_game(0)
    game.manager.reveal = MagicMock()
    game.manager.toggle_flag = MagicMock()

    game._handle_game_click((10, display.TOP_BAR_HEIGHT - 1), 1)
    game._handle_game_click((10, display.TOP_BAR_HEIGHT - 1), 3)

    game.manager.reveal.assert_not_called()
    game.manager.toggle_flag.assert_not_called()
    assert game.manager.get_state().first_move


def test_click_outside_board_is_ignored(game):
    game._start_game(0)
    game.manager.reveal = MagicMock()

    outside = (
        game.manager.get_state().columns * display.CELL_SIZE + 5,
        display.TOP_BAR_HEIGHT + 5,
    )
    game._handle_game_click(outside, 1)

    game.manager.reveal.assert_not_called()


def test_first_reveal_starts_timer(game):
    game._start_game(0)

    assert game._elapsed_seconds() == 0.0
    assert game.start_ticks is None

    game._handle_game_click(cell_click_pos(0, 0), 1)

    assert not game.manager.get_state().first_move
    assert game.start_ticks is not None
    assert game._elapsed_seconds() >= 0.0


def test_first_move_flag_does_not_start_timer(game):
    game._start_game(0)

    game._handle_game_click(cell_click_pos(0, 0), 3)

    assert game.manager.get_state().first_move
    assert game.start_ticks is None
    assert game._elapsed_seconds() == 0.0


def test_flag_after_first_reveal_marks_a_hidden_cell(game):
    game._start_game(0)
    game._handle_game_click(cell_click_pos(0, 0), 1)

    board = game.manager.get_board()
    width = board.dimension["column"]
    hidden = next(
        (i, tile) for i, tile in enumerate(board.board) if not tile.revealed
    )
    index, tile = hidden
    row, col = divmod(index, width)

    game._handle_game_click(cell_click_pos(row, col), 3)

    assert tile.isFlagged


def test_r_restarts_same_difficulty_and_resets_timer(game):
    game._start_game(1)
    game._handle_game_click(cell_click_pos(0, 0), 1)
    assert game.start_ticks is not None

    game._handle_keydown(pygame.K_r)

    assert game.screen_mode == "playing"
    state = game.manager.get_state()
    assert state.difficulty == 1
    assert state.first_move
    assert game.start_ticks is None
    assert game.frozen_elapsed is None
    assert game.manager.get_board() is None


def test_escape_returns_to_menu(game):
    game._start_game(0)

    game._handle_keydown(pygame.K_ESCAPE)

    assert game.screen_mode == "menu"
    assert game.manager is None
    assert game.start_ticks is None
    assert game.screen.get_size() == display.MENU_SIZE


def test_keyboard_ignored_on_menu(game):
    game._handle_keydown(pygame.K_r)
    game._handle_keydown(pygame.K_ESCAPE)

    assert game.screen_mode == "menu"
    assert game.manager is None


def test_timer_freezes_when_game_is_over(game):
    game._start_game(0)
    game._handle_game_click(cell_click_pos(0, 0), 1)

    board = game.manager.get_board()
    width = board.dimension["column"]
    mine_index = next(i for i, tile in enumerate(board.board) if tile.isMine)
    row, col = divmod(mine_index, width)

    game._handle_game_click(cell_click_pos(row, col), 1)

    assert game.manager.get_state().is_game_over
    frozen = game._elapsed_seconds()
    pygame.time.wait(40)
    assert game._elapsed_seconds() == frozen


def test_clicks_do_not_change_board_after_loss(game):
    game._start_game(0)
    game._handle_game_click(cell_click_pos(0, 0), 1)

    board = game.manager.get_board()
    width = board.dimension["column"]
    mine_index = next(i for i, tile in enumerate(board.board) if tile.isMine)
    mine_row, mine_col = divmod(mine_index, width)
    game._handle_game_click(cell_click_pos(mine_row, mine_col), 1)

    hidden = next(
        (i, tile)
        for i, tile in enumerate(board.board)
        if not tile.revealed and not tile.isMine
    )
    index, tile = hidden
    row, col = divmod(index, width)
    was_flagged = tile.isFlagged
    was_revealed = tile.revealed

    game._handle_game_click(cell_click_pos(row, col), 1)
    game._handle_game_click(cell_click_pos(row, col), 3)

    assert tile.revealed == was_revealed
    assert tile.isFlagged == was_flagged


def test_clicks_after_game_over_do_not_call_manager(game):
    game._start_game(0)
    game._handle_game_click(cell_click_pos(0, 0), 1)

    board = game.manager.get_board()
    width = board.dimension["column"]
    mine_index = next(i for i, tile in enumerate(board.board) if tile.isMine)
    mine_row, mine_col = divmod(mine_index, width)
    game._handle_game_click(cell_click_pos(mine_row, mine_col), 1)

    game.manager.reveal = MagicMock()
    game.manager.toggle_flag = MagicMock()
    game._handle_game_click(cell_click_pos(1, 1), 1)
    game._handle_game_click(cell_click_pos(1, 1), 3)

    game.manager.reveal.assert_not_called()
    game.manager.toggle_flag.assert_not_called()


def test_started_window_uses_board_size(game):
    game._start_game(0)
    state = game.manager.get_state()

    expected_w = max(state.columns * display.CELL_SIZE, display.MIN_WINDOW_WIDTH)
    expected_h = state.rows * display.CELL_SIZE + display.TOP_BAR_HEIGHT

    assert game.screen.get_size() == (expected_w, expected_h)
