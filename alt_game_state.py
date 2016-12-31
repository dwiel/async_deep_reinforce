# -*- coding: utf-8 -*-
import numpy as np

# TODO
from constants import ACTION_SIZE


class GameState(object):
    def __init__(self, rand_seed):
        # height=210, width=160
        # self._screen = np.empty((210, 160, 1), dtype=np.uint8)

        self.reset()

    def _process_frame(self, action):
        reward = action
        terminal = False
        x_t = np.empty((84, 84), dtype=np.float32)

        return reward, terminal, x_t

    def reset(self):
        _, _, x_t = self._process_frame(0)

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
