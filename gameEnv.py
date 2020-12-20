import gym
import time
import pygame
import sys
import numpy as np
from gym import spaces

# Display params
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
COLOR_BACKGROUND = (0, 0, 0)
COLOR_WALL = (255, 255, 255)
COLOR_ROBOT = (255, 0, 0)

SIM_PERIOD_MS = 500.0

GOAL_X = 14
GOAL_Y = 10

# Actions
UP = 1
DOWN = 2
RIGHT = 3
LEFT = 4


class GameEnv(gym.Env):
    """Custom Environment to control Ecron robot in openrave using gym interface"""
    metadata = {'render.modes': ['human']}

    def __init__(self, initX=2, initY=2, map="map/map1.csv"):

        inFileStr = map
        self.inFile = np.genfromtxt(inFileStr, delimiter=',')

        # Get lengh of map
        self.nX = self.inFile.shape[0]
        self.nY = self.inFile.shape[1]
        self.pixelX = SCREEN_WIDTH/self.nX
        self.pixelY = SCREEN_HEIGHT/self.nY
        # Initialize screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
        self.screen.fill(COLOR_BACKGROUND)
        # Set initial robot pos
        self.initX = 2
        self.initY = 2

    def step(self, action):
        done = False
        reward = 0
        # Move robot in desired direction
        pygame.draw.rect(self.screen, COLOR_BACKGROUND, self.robot)
        #self.robot.move_ip(incrementX, incrementY)
        self.robot.move_ip(0,self.pixelY/2.0)
        #Update screen
        pygame.draw.rect(self.screen, COLOR_ROBOT, self.robot)
        pygame.display.update()

        time.sleep(SIM_PERIOD_MS/1000.0)

        obs = self._get_obs()

        #if self.debug
        #    print("Reward: "+str(reward))
        #    print("Current cell: "+str(obs))
        #    print("Action taken: "+str(action))

        return obs, reward, done, None

    def reset(self):
        for iX in range(self.nX):
            # print "iX:",iX
            for iY in range(self.nY):
                # print "* iY:",iY
                # -- Skip box if map indicates a 0
                if self.inFile[iX][iY] == 0:
                    continue
                pygame.draw.rect(self.screen, COLOR_WALL,
                                 pygame.Rect(self.pixelX*iX, self.pixelY*iY, self.pixelX, self.pixelY))
                self.robot = pygame.draw.rect(self.screen, COLOR_ROBOT,
                                              pygame.Rect(self.pixelX*self.initX+self.pixelX/4.0, self.pixelY*self.initY+self.pixelY/4.0, self.pixelX/2.0, self.pixelY/2.0))
        pygame.display.flip()
        time.sleep(0.5)

        return self._get_obs()

    def render(self, mode='human', close=False):
        return

    # Returns a vector with every pixel color from screen
    def _get_obs(self):
        pixArray = []
        maxW = int(self.screen.get_width())
        maxH = int(self.screen.get_height())
        for i in range(maxW):
            for j in range(maxH):
                pixArray.append(self.screen.get_at((i, j))[:3])

        return pixArray

    # Given a discrete action returns velocity vector
    def _get_vel_from_action(self, action):
        # Go backwards
        if action == DOWN:
            return
        # Turn right
        elif action == RIGHT:
            return
        # Turn left
        elif action == LEFT:
            return
        # Go straight
        elif action == UP:
            return

        return
