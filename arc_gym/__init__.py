from gym.envs.registration import register

register(
    id='arc-v0',
    entry_point='arc_gym.envs:ARCEnv',
)
