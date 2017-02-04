# -*- coding: utf-8 -*-
from __future__ import print_function
import numpy as np


def limit(x, low, high):
    if x < low:
        return low
    if x > high:
        return high
    return x


def within(x, low, high):
    return x >= low and x < high


def window(x, width):
    start = x - int(width / 2)
    return start, start + width


class UnexpectedCopyWindowInputShape(ValueError):
    def __init__(self, game_state, x_t):
        super(UnexpectedCopyWindowInputShape, self).__init__(
            'expected x_t to be shape {expected_input_shape}, found {shape}'.
            format(
                shape=x_t.shape, **game_state.__dict__
            )
        )


class GameState(object):
    environment_shape = [84, 84]
    VISITED = 0
    OUT_OF_BOUNDS = -1
    NOT_VISITED = 1
    ACTION_SIZE = 4

    def __init__(
            self,
            rand_seed=0,
            body_width=1,
            body_height=1,
            velocity=1,
            view_width=84,
            view_height=84,
            board_width=5,
            board_height=5,
    ):

        self.body_width = body_width
        self.body_height = body_height
        self.velocity = velocity
        self.view_width = view_width
        self.view_height = view_height
        self.expected_input_shape = (self.view_width, self.view_height)

        self.board_width = board_width
        self.board_height = board_height

        self.terminal_count = 0
        self.reset()

    def _is_valid_board_position(self, x, y):
        return within(x, 0, self.board_width) and within(
            y, 0, self.board_height
        )

    def _copy_window(self, x_t):
        x_t[:] = self.OUT_OF_BOUNDS
        if x_t.shape != self.expected_input_shape:
            raise UnexpectedCopyWindowInputShape(self, x_t)

        view_offset_x = (self.board_position_x - self.view_width / 2)
        view_offset_y = (self.board_position_y - self.view_height / 2)

        for i in range(self.view_width):
            for j in range(self.view_height):
                board_x = view_offset_x + i
                board_y = view_offset_y + j

                if self._is_valid_board_position(board_x, board_y):
                    x_t[i, j] = self.height[board_x, board_y]

        # would be nice to do with matrix math somehow
        # x_t[0:self.view_width,] = self.height[view_offset_x:view_offset_x+self.view_width]

    def _score(self):
        max_score = float(self.board_height * self.board_width)
        return np.sum(self.height == self.VISITED) / max_score * 1000

    def _process_frame(self, action):
        before_move_score = self._score()

        # mark this site as visited
        # x_range = slice(self.position_x - 2, self.position_x + 3)
        # y_range = slice(self.position_y - 2, self.position_y + 3)
        x_range = self.board_position_x
        y_range = self.board_position_y
        self.height[x_range, y_range] = self.VISITED

        # move
        if action == None:
            pass
        elif action == 0:
            self.board_position_x += self.velocity
        elif action == 1:
            self.board_position_x -= self.velocity
        elif action == 2:
            self.board_position_y += self.velocity
        elif action == 3:
            self.board_position_y -= self.velocity

        self.board_position_x = limit(
            self.board_position_x, 0, self.board_width - 1
        )
        self.board_position_y = limit(
            self.board_position_y, 0, self.board_height - 1
        )

        self.time_steps += 1

        terminal = self.time_steps > self.board_width * self.board_height * 2

        # mark out of bounds with -1
        x_t = np.ones((self.view_width, self.view_height),
                      dtype=np.float32) * self.OUT_OF_BOUNDS

        self._copy_window(x_t)

        after_move_score = self._score()
        reward = after_move_score - before_move_score - 0.1

        if terminal:
            if self.terminal_count % 5 == 0:
                print('reward', reward)
                print('score', after_move_score)
            self.terminal_count += 1

        # print('x, y', self.board_position_x, self.board_position_y)
        # print('reward', reward)
        # print('score', score)
        # for i in range(self.height.shape[0]):
        #     for j in range(self.height.shape[1]):
        #         if self.height[i, j] == 0:
        #             print(' ', end="")
        #         elif self.height[i, j] == 1:
        #             print('-', end="")
        #         else:
        #             print('X', end="")
        #     print('')

        return reward, terminal, x_t

    def reset(self):
        # print('reset')
        self.board_position_x = self.board_width / 2
        self.board_position_y = self.board_height / 2
        self.height = np.ones((self.board_width, self.board_height),
                              dtype=np.float32) * self.NOT_VISITED
        self.time_steps = 0

        _, _, x_t = self._process_frame(None)

        self.reward = 0
        self.terminal = False
        # stack 4 images up in time
        self.s_t = np.stack((x_t, x_t, x_t, x_t), axis=2)

    def process(self, action):
        r, t, x_t1 = self._process_frame(action)

        self.reward = r
        self.terminal = t
        # remove the oldest frame, add on this newest one
        self.s_t1 = np.append(
            self.s_t[:, :, 1:], x_t1.reshape((84, 84, 1)), axis=2
        )

    def update(self):
        self.s_t = self.s_t1
