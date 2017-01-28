import pytest
import numpy as np
from alt_game_state import GameState, UnexpectedCopyWindowInputShape


def test_tiny():
    gs = GameState(view_width=1, view_height=1, board_width=1, board_height=1)

    x_t = np.array([2]).reshape((1, 1))
    gs._copy_window(x_t)

    assert x_t[0, 0] == GameState.VISITED


def test_incorrect_view_shape():
    gs = GameState(view_width=1, view_height=1, board_width=3, board_height=3)

    x_t = np.array([3, 3]).reshape((1, 2))
    with pytest.raises(UnexpectedCopyWindowInputShape):
        gs._copy_window(x_t)


def test_tiny_view():
    BOARD_WIDTH = 5
    BOARD_HEIGHT = 5
    gs = GameState(
        view_width=1,
        view_height=1,
        board_width=BOARD_WIDTH,
        board_height=BOARD_HEIGHT
    )

    assert gs.board_position_x == BOARD_WIDTH / 2
    assert gs.board_position_y == BOARD_WIDTH / 2

    x_t = np.array([3]).reshape((1, 1))

    gs._copy_window(x_t)
    # assert x_t[0, 0] == 1

    image = np.zeros((BOARD_WIDTH, BOARD_HEIGHT))
    for gs.board_position_x in range(BOARD_WIDTH):
        for gs.board_position_y in range(BOARD_HEIGHT):
            gs._copy_window(x_t)
            image[gs.board_position_x, gs.board_position_y] = x_t[0, 0]

    target = np.zeros((BOARD_WIDTH, BOARD_HEIGHT), dtype=np.float32)
    target[:] = GameState.NOT_VISITED

    target[BOARD_WIDTH / 2, BOARD_WIDTH / 2] = GameState.VISITED
    np.testing.assert_allclose(image, target)


def test_wider_view():
    VIEW_WIDTH = 5
    VIEW_HEIGHT = 5

    gs = GameState(
        view_width=VIEW_WIDTH,
        view_height=VIEW_HEIGHT,
        board_width=3,
        board_height=3
    )

    assert gs.board_position_x == 1
    assert gs.board_position_y == 1

    target = np.zeros((3, 3), dtype=np.float32)
    target[:] = GameState.NOT_VISITED
    target[1, 1] = GameState.VISITED
    np.testing.assert_allclose(gs.height, target)

    x_t = np.random.random((VIEW_HEIGHT, VIEW_WIDTH))

    gs._copy_window(x_t)
    target = np.zeros((5, 5), dtype=np.float32)
    target[:] = GameState.OUT_OF_BOUNDS
    target[1:-1, 1:-1] = GameState.NOT_VISITED
    target[2, 2] = GameState.VISITED
    np.testing.assert_allclose(x_t, target)
