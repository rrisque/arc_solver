import gym


class ARCEnv(gym.Env):
    """
    Gym environment for ARC.
    """
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(ARCEnv, self).__init__()

    def step(self, action):
        ...

    def reset(self, symbol=None):
        return self._next_observation()

    def _next_observation(self):
        ...

    def render(self, mode='human'):
        ...

    def close(self):
        ...


if __name__ == '__main__':
    env = ARCEnv()
    env.reset()
    done = False
    while not done:
        obs, reward, done = env.step(env.action_space.sample())
