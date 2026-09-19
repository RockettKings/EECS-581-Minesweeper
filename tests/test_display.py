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
