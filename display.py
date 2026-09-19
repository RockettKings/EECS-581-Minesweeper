'''
Prologue comment
File: display.py
Description: 
External sources:
Author: Nick Heyer, Andrew Kruckemyer
Created: 9/17/26
'''
import pygame
from game_state import GameStatus

# required constants (referenced in input_handler.py)
# feel free to change these values
DIFFICULTY_LABELS = ["Beginner", "Intermediate", "Expert"]
MENU_SIZE = (300, 200)
TOP_BAR_HEIGHT = 40
CELL_SIZE = 30
MIN_WINDOW_WIDTH = 400

# basic colors used by the menu and game board
BACKGROUND_COLOR = (225, 225, 225)
BUTTON_COLOR = (190, 190, 190)
BUTTON_HOVER_COLOR = (210, 210, 210)
BORDER_COLOR = (90, 90, 90)
HIDDEN_CELL_COLOR = (180, 180, 180)
REVEALED_CELL_COLOR = (235, 235, 235)
TOP_BAR_COLOR = (205, 205, 205)
TEXT_COLOR = (20, 20, 20)
MINE_COLOR = (190, 40, 40)
FLAG_COLOR = (190, 40, 40)

NUMBER_COLORS = {
    1: (0, 0, 200),
    2: (0, 130, 0),
    3: (200, 0, 0),
    4: (0, 0, 120),
    5: (120, 0, 0),
    6: (0, 120, 120),
    7: (0, 0, 0),
    8: (90, 90, 90),
}
 
# required funcions (referenced in input_handler.py)
# called in input_handler.py to get the clickable rect for the difficulty buttons
def menu_button_rect(index):
    """Returns the clickable rect for the difficulty button at `index`.
    Used by input_handler.py for click detection AND should be used
    here in draw_menu() so buttons are drawn exactly where clicks are
    detected. Feel free to change the layout -- just keep both uses in
    sync."""
    width, height = 200, 40
    x = (MENU_SIZE[0] - width) // 2
    y = 40 + index * (height + 10)
    return pygame.Rect(x, y, width, height)

# called in input_handler.py to draw the menu screen with difficulty buttons
def draw_menu(screen, font):
    """draw the difficulty menu with three buttons for Beginner, Intermediate, and Expert.
    Use menu_button_rect(i) for each index in range(len(DIFFICULTY_LABELS))
    so clicks and drawing agree on button position."""

# called in input_handler.py to draw the game screen with the grid, status bar, mine counter, timer, and win/loss message
def draw_game(screen, font, big_font, manager, elapsed_seconds):
    """draw the game grid, status bar, mine counter, timer, and
    win/loss message."""
    # gives you the current game state and board to use for drawing
    state = manager.get_state()
    board = manager.get_board()
 