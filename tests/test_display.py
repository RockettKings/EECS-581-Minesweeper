"""
Prologue Comment
File: test_display.py
Description: Tests display.py layout constants and the menu button
             geometry used by both drawing and click detection.
Inputs: Button index, expected menu/button sizes
Outputs: Pytest results of each test case
External sources: None
Author: Jon Kazmaier
Created: [Sept 19 2026]
"""

import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame
import pytest

import display
from game_manager import GameManager


@pytest.fixture(scope="module", autouse=True)
def pygame_setup():
    pygame.init()
    yield
    pygame.quit()


def test_difficulty_labels_match_ui_contract():
    assert display.DIFFICULTY_LABELS == ["Beginner", "Intermediate", "Expert"]


def test_layout_constants_are_positive():
    assert display.MENU_SIZE[0] > 0
    assert display.MENU_SIZE[1] > 0
    assert display.TOP_BAR_HEIGHT > 0
    assert display.CELL_SIZE > 0
    assert display.MIN_WINDOW_WIDTH > 0


@pytest.mark.parametrize("index", [0, 1, 2])
def test_menu_button_rect_is_inside_menu(index):
    rect = display.menu_button_rect(index)
    menu = pygame.Rect(0, 0, *display.MENU_SIZE)

    assert menu.contains(rect)


def test_menu_buttons_do_not_overlap():
    rects = [display.menu_button_rect(i) for i in range(len(display.DIFFICULTY_LABELS))]

    for i, left in enumerate(rects):
        for right in rects[i + 1 :]:
            assert not left.colliderect(right)


def test_menu_buttons_are_stacked_and_same_size():
    first = display.menu_button_rect(0)
    second = display.menu_button_rect(1)
    third = display.menu_button_rect(2)

    assert first.size == second.size == third.size
    assert first.x == second.x == third.x
    assert first.y < second.y < third.y


def test_draw_menu_does_not_raise():
    screen = pygame.display.set_mode(display.MENU_SIZE)
    font = pygame.font.SysFont(None, 24)

    display.draw_menu(screen, font)


def test_draw_game_does_not_raise():
    manager = GameManager(0)
    window_w = max(manager.get_state().columns * display.CELL_SIZE, display.MIN_WINDOW_WIDTH)
    window_h = manager.get_state().rows * display.CELL_SIZE + display.TOP_BAR_HEIGHT
    screen = pygame.display.set_mode((window_w, window_h))
    font = pygame.font.SysFont(None, 24)
    big_font = pygame.font.SysFont(None, 40, bold=True)

    display.draw_game(screen, font, big_font, manager, 0.0)


def _game_screen(manager):
    state = manager.get_state()
    window_w = max(state.columns * display.CELL_SIZE, display.MIN_WINDOW_WIDTH)
    window_h = state.rows * display.CELL_SIZE + display.TOP_BAR_HEIGHT
    screen = pygame.display.set_mode((window_w, window_h))
    font = pygame.font.SysFont(None, 24)
    big_font = pygame.font.SysFont(None, 40, bold=True)
    return screen, font, big_font


def _cell_center_color(screen, row, col):
    x = col * display.CELL_SIZE + display.CELL_SIZE // 2
    y = display.TOP_BAR_HEIGHT + row * display.CELL_SIZE + display.CELL_SIZE // 2
    return screen.get_at((x, y))[:3]


def _cell_colors(screen, row, col):
    x0 = col * display.CELL_SIZE
    y0 = display.TOP_BAR_HEIGHT + row * display.CELL_SIZE
    colors = set()
    for y in range(y0 + 1, y0 + display.CELL_SIZE - 1):
        for x in range(x0 + 1, x0 + display.CELL_SIZE - 1):
            colors.add(screen.get_at((x, y))[:3])
    return colors


def _forced_board(manager):
    """Force known cell states on the last row so drawing can be checked."""
    if manager.get_board() is None:
        manager.reveal(0, 0)
    board = manager.get_board()
    width = board.dimension["column"]

    def tile(col, **attrs):
        cell = board.board[9 * width + col]
        cell.revealed = False
        cell.isFlagged = False
        cell.isMine = False
        cell.adjacent = 0
        for name, value in attrs.items():
            setattr(cell, name, value)
        return cell

    return {
        "hidden": tile(9),
        "blank": tile(8, revealed=True),
        "number": tile(7, revealed=True, adjacent=3),
        "flagged": tile(6, isFlagged=True),
        "mine": tile(5, revealed=True, isMine=True),
    }


def test_draw_menu_uses_button_color_inside_menu_buttons():
    screen = pygame.display.set_mode(display.MENU_SIZE)
    font = pygame.font.SysFont(None, 24)
    pygame.mouse.set_pos((0, 0))

    display.draw_menu(screen, font)

    button = display.menu_button_rect(0)
    assert screen.get_at(button.center)[:3] == display.BUTTON_COLOR


def test_draw_game_distinguishes_contract_cell_states():
    manager = GameManager(0)
    cells = _forced_board(manager)
    screen, font, big_font = _game_screen(manager)

    display.draw_game(screen, font, big_font, manager, 0.0)

    hidden = _cell_center_color(screen, 9, 9)
    blank = _cell_center_color(screen, 9, 8)
    number_colors = _cell_colors(screen, 9, 7)
    flagged_colors = _cell_colors(screen, 9, 6)
    mine_colors = _cell_colors(screen, 9, 5)

    assert hidden == display.HIDDEN_CELL_COLOR
    assert blank == display.REVEALED_CELL_COLOR
    assert display.NUMBER_COLORS[3] in number_colors
    assert display.FLAG_COLOR in flagged_colors
    assert display.MINE_COLOR in mine_colors
    assert cells["number"].adjacent == 3


def test_draw_game_shows_game_over_overlay_after_loss():
    manager = GameManager(0)
    manager.reveal(0, 0)
    board = manager.get_board()
    width = board.dimension["column"]
    mine_index = next(i for i, tile in enumerate(board.board) if tile.isMine)
    row, col = divmod(mine_index, width)
    manager.reveal(row, col)

    screen, font, big_font = _game_screen(manager)
    display.draw_game(screen, font, big_font, manager, 4.0)

    center = screen.get_at((screen.get_width() // 2, screen.get_height() // 2))[:3]
    assert manager.get_state().is_game_over
    assert center == display.TEXT_COLOR


def test_mine_counter_uses_remaining_mines():
    manager = GameManager(0)
    manager.reveal(0, 0)
    board = manager.get_board()
    width = board.dimension["column"]
    hidden = next(
        (i, tile) for i, tile in enumerate(board.board) if not tile.revealed
    )
    index, _tile = hidden
    row, col = divmod(index, width)
    manager.toggle_flag(row, col)

    flags_used = display._count_flags(manager.get_state(), board)
    total_mines = display._get_total_mines(manager.get_state())

    assert total_mines == 10
    assert flags_used == 1
    assert max(total_mines - flags_used, 0) == 9
