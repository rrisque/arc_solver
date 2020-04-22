import json
import os
import random

import gym

from utils.utils import plot_task


class ARCEnv(gym.Env):
    """
    Gym environment for ARC.
    """
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(ARCEnv, self).__init__()
        self.training_dir = '../../data/training/'
        self.tasks = []
        self._populate_tasks()
        self.task = random.choice(self.tasks)
        self.attempts = 0

    def _populate_tasks(self):
        for filename in os.listdir(self.training_dir):
            with open(self.training_dir + filename, 'r') as f:
                self.tasks.append(json.load(f))

    def step(self, action):
        reward = 0
        if action == self.task['test'][0]['output']:
            reward = 1

        if self.attempts == 3:
            self.attempts = 0
            self.task = random.choice(self.tasks)

        return self.task, reward

    def reset(self, symbol=None):
        self.task = random.choice(self.tasks)
        self.attempts = 0
        return self.task

    def render(self, mode='human'):
        plot_task(self.task)

    def close(self):
        ...


if __name__ == '__main__':
    env = ARCEnv()
    obs = env.reset()

    # cheat and give the correct answer
    obs, reward = env.step(obs['test'][0]['output'])
    print(reward)
