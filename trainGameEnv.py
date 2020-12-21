# Trains agent using DQN, see 
#https://stable-baselines.readthedocs.io/en/master/modules/dqn.html
# For more info about the algorithm implementation

import gym
import gameEnv

from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.deepq.policies import MlpPolicy
from stable_baselines import DQN

env = gameEnv.GameEnv(initX=1, initY=1)

model = DQN(MlpPolicy, env, verbose=1)
model.learn(total_timesteps=10000, log_interval=2)
model.save("deepq_game")

del model # remove to demonstrate saving and loading

model = DQN.load("deepq_game")

obs = env.reset()
while True:
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    