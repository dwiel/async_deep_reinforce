import numpy as np
import random
import tinyik

from game_state_base import BaseGameState

runs = 0
scores = []
difficulty = 0.02
terminate_steps = 100
max_score = 0.1


def best_score(difficulty, steps):
    steps_to_goal = max(0, difficulty - 0.01) / 0.01
    return max(0, steps - steps_to_goal)


class VirtualArmGameState(BaseGameState):
    ACTION_SIZE = 3
    environment_shape = [1]

    def _reset(self):
        global runs
        global scores
        global difficulty
        global terminate_steps
        global max_score

        runs += 1
        # self.arm = tinyik.Actuator(['z', [1., 0., 0.], 'z', [1., 0., 0.]])
        self.arm = tinyik.Actuator(['z', [1., 0., 0.]])
        self.goal = np.array([1, 0, 0])
        # print('runs', runs)
        # difficulty = min(runs/100000.0 * 0.1, 0.1)
        # print('difficulty', difficulty)
        # self.terminate_steps = max(min(runs/1000000.0 * 200, 200), 5)
        mean_score = np.mean(scores)
        print('ms', mean_score)

        if len(scores) > 20 and np.mean(scores) > 0.9:
            difficulty += 0.01
            terminate_steps += 5
            max_score += 0.1
            # reset score counter
            scores = []
        if terminate_steps > 5 and len(scores) > 4980 and np.mean(scores) < 0.9:
            difficulty -= 0.01
            terminate_steps -= 5
            max_score += 0.1
            # reset score counter
            scores = []

        if difficulty >= 0.15:
            max_score = 10
        if difficulty >= 0.20:
            max_score = 50
        if difficulty >= 0.30:
            max_score = 100

        self.difficulty = difficulty
        self.terminate_steps = terminate_steps
        print('difficulty', self.difficulty)
        print('terimate_steps', self.terminate_steps)

        # self.initial_position = random.choice([-1, 1]) * self.difficulty
        self.initial_position = np.random.uniform(
            -self.difficulty, self.difficulty, 1
        )[0]
        self.arm.angles[0] = self.initial_position
        self.score = 0.0

    def _score(self):
        # return 1 - np.linalg.norm(self.arm.ee - self.goal)
        # self.score += (1.0 - abs(self.arm.angles[0]))**2
        return self.score

    def _terminal(self):
        global scores
        global max_score

        terminate = self.time_steps >= self.terminate_steps
        terminate = terminate or (self.score >= max(2, max_score))
        if terminate:
            # pscore = self.score / (
            #     best_score(self.initial_position, self.terminate_steps)
            # )
            pscore = self.score / max(2, max_score)
            print('initial', self.initial_position)
            print('angle', self.arm.angles[0])
            print('score', self.score)
            print('max_score', max_score, max(2, max_score))
            print('pscore', pscore)
            scores.append(pscore)
            scores = scores[-500:]
        return terminate

    def _apply_action(self, action):
        if action is not None:
            if action == 0:
                pass
            elif action == 1:
                self.arm.angles[0] += 0.01
            elif action == 2:
                self.arm.angles[0] -= 0.01
            # elif action == 2:
            #     self.arm.angles[1] += 0.1
            # elif action == 3:
            #     self.arm.angles[1] -= 0.1

        self.arm.angles[0] = min(self.arm.angles[0], 1)
        self.arm.angles[0] = max(self.arm.angles[0], -1)

        # recompute score
        # self.score += int(abs(self.arm.angles[0]) < 0.02)
        self.score += int(abs(self.arm.ee[0]) > 0.98)

        # penalize for hitting min/max bounds
        if abs(self.arm.angles[0]) > 0.99:
            self.score -= 1


        return np.array([self.arm.angles[0]])
