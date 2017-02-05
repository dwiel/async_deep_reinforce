# -*- coding: utf-8 -*-
from __future__ import print_function
import random
import numpy as np



class BaseGameState(object):
    def __init__(
            self,
            rand_seed=0,
    ):
        self.terminal_count = 0
        self.reset()
        random.seed(rand_seed)

    def _reset(self):
        raise NotImplemented()

    def _score(self):
        raise NotImplemented()

    def _terminal(self):
        raise NotImplemented()

    def _apply_action(self, action):
        """
        given action, apply action, return new sensor status
        """
        raise NotImplemented()

    def _process_frame(self, action):
        before_move_score = self._score()

        # apply action
        x_t = self._apply_action(action)

        self.time_steps += 1

        after_move_score = self._score()
        reward = after_move_score - before_move_score

        # TODO: decide if this is a terminal state
        terminal = self._terminal()

        if terminal:
            if self.terminal_count % 5 == 0:
                print('reward', reward)
                print('score', after_move_score)
                print('angles', self.arm.angles)
                print('ee', self.arm.ee)
            self.terminal_count += 1

        return reward, terminal, x_t

    def reset(self):
        self.time_steps = 0

        self._reset()
        # TODO: None action is sort of weird ...
        _, _, x_t = self._process_frame(None)

        self.reward = 0
        self.terminal = False
        # stack 4 images up in time
        self.s_t = np.stack((x_t, x_t, x_t, x_t), axis=len(x_t.shape))

    def process(self, action):
        r, t, x_t1 = self._process_frame(action)

        self.reward = r
        self.terminal = t
        # remove the oldest frame, add on this newest one
        self.s_t1 = np.append(
            self.s_t[..., 1:],
            np.expand_dims(x_t1, -1),
            axis=-1,
        )

    def update(self):
        self.s_t = self.s_t1
