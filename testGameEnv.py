import pygame
import gym
import gameEnv
import numpy

if __name__ == '__main__':

    env = gameEnv.GameEnv()

    obs = env.reset()
    #print(str(obs))
    #while True:
    for i in range(5):
        action = 1
        obs, rewards, dones, info = env.step(action)

        #print(str(obs))