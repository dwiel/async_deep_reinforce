import numpy as np

from game_state_base import BaseGameState


class AccumulateGameState(BaseGameState):
    environment_shape = [1]
    def _reset(self):
        self.state = 0

    def _score(self):
        return self.state

    def _terminal(self):
        self.time_steps = 100

    def _apply_action(self, action):
        if action:
            self.state += action - 2

        return np.array([self.state])
