"""
Prologue Comment
File: test_interface_contract.py
Description: Enforces the GameManager interface contract used by the UI:
             allowed methods, state fields, first-click safety, flag
             rules, and that frontend modules do not call internals.
Inputs: Difficulty index, row/column positions, frontend source files
Outputs: Pytest results of each test case
External sources: None
Author: Jon Kazmaier
Created: [Sept 19 2026]
"""

import ast
import inspect
from pathlib import Path

import pytest

from game_manager import GameManager
from game_state import GameState, GameStatus


#methods the UI is allowed to call on GameManager
ALLOWED_MANAGER_METHODS = {
    "reveal",
    "toggle_flag",
    "get_state",
    "get_board",
}

#frontend files checked for contract method use
FRONTEND_FILES = (
    Path("input_handler.py"),
    Path("display.py"),
)

#expected rows, columns, and mines for each difficulty index
DIFFICULTY_SHAPES = {
    0: (10, 10, 10),
    1: (16, 16, 40),
    2: (16, 30, 99),
}

#GameState fields the UI may read
STATE_FIELDS = (
    "difficulty",
    "rows",
    "columns",
    "mine_count",
    "flags_placed",
    "flags_remaining",
    "first_move",
    "status",
    "is_active",
    "is_game_over",
)


#collects manager.method names used in a frontend source file
def manager_attributes(source: str) -> set[str]:
    tree = ast.parse(source)
    attrs = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Attribute):
            continue
        value = node.value
        if isinstance(value, ast.Name) and value.id == "manager":
            attrs.add(node.attr)
        elif isinstance(value, ast.Attribute) and value.attr == "manager":
            attrs.add(node.attr)
    return attrs


#finds the first hidden tile and returns its row, column, and tile
def first_hidden_tile(manager: GameManager):
    board = manager.get_board()
    width = board.dimension["column"]
    for index, tile in enumerate(board.board):
        if not tile.revealed:
            return divmod(index, width) + (tile,)
    raise AssertionError("expected a hidden tile")


#finds the first mine and returns its row, column, and tile
def first_mine(manager: GameManager):
    board = manager.get_board()
    width = board.dimension["column"]
    for index, tile in enumerate(board.board):
        if tile.isMine:
            return divmod(index, width) + (tile,)
    raise AssertionError("expected a mine")


#checks that the contract methods exist with the expected parameters
def test_required_methods_exist_with_expected_parameters():
    assert inspect.signature(GameManager).parameters["difficulty"].name == "difficulty"

    reveal = inspect.signature(GameManager.reveal)
    assert list(reveal.parameters) == ["self", "row", "column"]

    toggle = inspect.signature(GameManager.toggle_flag)
    assert list(toggle.parameters) == ["self", "row", "column"]

    assert inspect.signature(GameManager.get_state).return_annotation is GameState
    assert callable(GameManager.get_board)


#checks that get_state reports the selected difficulty size and mine count
@pytest.mark.parametrize("difficulty, rows, columns, mines", [
    (0, 10, 10, 10),
    (1, 16, 16, 40),
    (2, 16, 30, 99),
])
def test_constructor_exposes_difficulty_on_get_state(difficulty, rows, columns, mines):
    manager = GameManager(difficulty)
    state = manager.get_state()

    assert isinstance(state, GameState)
    assert state.difficulty == difficulty
    assert state.rows == rows
    assert state.columns == columns
    assert state.mine_count == mines
    assert state.flags_placed == 0
    assert state.flags_remaining == mines
    assert state.first_move is True
    assert state.status is GameStatus.PLAYING
    assert state.is_active is True
    assert state.is_game_over is False
    assert manager.get_board() is None


#checks that GameState exposes every field the UI is allowed to read
def test_get_state_exposes_contract_fields():
    state = GameManager(0).get_state()
    for field in STATE_FIELDS:
        assert hasattr(state, field), f"GameState is missing {field}"


#checks that an invalid difficulty raises ValueError
def test_invalid_difficulty_raises_value_error():
    with pytest.raises(ValueError):
        GameManager(3)


#checks that the first reveal builds the board and clears first_move
def test_first_reveal_builds_board_and_clears_first_move():
    manager = GameManager(0)

    tile = manager.reveal(0, 0)

    assert manager.get_board() is not None
    assert manager.get_state().first_move is False
    assert tile is None or tile.revealed or tile.adjacent == 0


#checks that the first click and its neighbors are never mines
def test_first_reveal_is_safe_for_click_and_neighbors():
    manager = GameManager(0)
    row, column = 4, 4
    manager.reveal(row, column)
    board = manager.get_board()
    width = board.dimension["column"]

    for row_offset in (-1, 0, 1):
        for column_offset in (-1, 0, 1):
            neighbor_row = row + row_offset
            neighbor_column = column + column_offset
            if not (0 <= neighbor_row < board.dimension["row"]):
                continue
            if not (0 <= neighbor_column < width):
                continue
            tile = board.board[neighbor_row * width + neighbor_column]
            assert tile.isMine is False


#checks that out of bounds reveal and flag raise ValueError
def test_out_of_bounds_reveal_and_flag_raise_value_error():
    manager = GameManager(0)

    with pytest.raises(ValueError):
        manager.reveal(-1, 0)
    with pytest.raises(ValueError):
        manager.toggle_flag(0, 99)


#checks that flagging before the board exists does nothing
def test_toggle_flag_before_first_reveal_is_noop():
    manager = GameManager(0)

    manager.toggle_flag(0, 0)

    assert manager.get_board() is None
    assert manager.get_state().flags_placed == 0
    assert manager.get_state().first_move is True


#checks that toggling a flag updates flags_placed and flags_remaining
def test_toggle_flag_updates_flags_remaining():
    manager = GameManager(0)
    manager.reveal(0, 0)
    row, column, tile = first_hidden_tile(manager)
    remaining_before = manager.get_state().flags_remaining

    manager.toggle_flag(row, column)

    assert tile.isFlagged is True
    assert manager.get_state().flags_placed == 1
    assert manager.get_state().flags_remaining == remaining_before - 1

    manager.toggle_flag(row, column)

    assert tile.isFlagged is False
    assert manager.get_state().flags_placed == 0
    assert manager.get_state().flags_remaining == remaining_before


#checks that reveal does not open a flagged cell
def test_reveal_does_not_open_a_flagged_cell():
    manager = GameManager(0)
    manager.reveal(0, 0)
    row, column, tile = first_hidden_tile(manager)
    manager.toggle_flag(row, column)

    result = manager.reveal(row, column)

    assert result is None
    assert tile.revealed is False
    assert tile.isFlagged is True


#checks that revealing a mine marks the game lost and shows all mines
def test_revealing_a_mine_ends_the_game():
    manager = GameManager(0)
    manager.reveal(0, 0)
    row, column, tile = first_mine(manager)

    result = manager.reveal(row, column)
    state = manager.get_state()

    assert result is tile
    assert tile.revealed is True
    assert state.status is GameStatus.LOST
    assert state.is_active is False
    assert state.is_game_over is True
    assert all(mine.revealed for mine in manager.get_board().board if mine.isMine)


#checks that reveal and flag do nothing after the game is over
def test_actions_after_game_over_are_noops():
    manager = GameManager(0)
    manager.reveal(0, 0)
    mine_row, mine_column, _ = first_mine(manager)
    manager.reveal(mine_row, mine_column)
    row, column, tile = first_hidden_tile(manager)
    flags_before = manager.get_state().flags_placed

    assert manager.reveal(row, column) is None
    manager.toggle_flag(row, column)

    assert tile.revealed is False
    assert tile.isFlagged is False
    assert manager.get_state().flags_placed == flags_before
    assert manager.get_state().is_game_over is True


#checks that the UI only calls the allowed GameManager methods
@pytest.mark.parametrize("path", FRONTEND_FILES)
def test_frontend_only_calls_allowed_manager_methods(path):
    attrs = manager_attributes(path.read_text())
    unexpected = attrs - ALLOWED_MANAGER_METHODS
    assert unexpected == set(), f"{path} calls manager.{sorted(unexpected)}"
