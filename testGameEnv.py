import pygame
import gym
import gameEnv
import numpy

if __name__ == '__main__':

    env = gameEnv.GameEnv(initX=1, initY=1, debug=True)

    obs = env.reset()
    #print(str(obs))
    #while True:
    for i in range(20):
        action = 2
        obs, rewards, dones, info = env.step(action)

        #print(str(obs))