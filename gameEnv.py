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

GOAL_X = 580 # This should be calculated like initial pos of robot
GOAL_Y = 420 # This should be calculated like initial pos of robot

# Actions
UP = 0
DOWN = 1
RIGHT = 2
LEFT = 3


class GameEnv(gym.Env):
    """Custom Environment to control Ecron robot in openrave using gym interface"""
    metadata = {'render.modes': ['human']}

    def __init__(self, initX=2, initY=2, map="map/map1.csv", debug=False):

        self.debug = debug

        inFileStr = map
        self.inFile = np.genfromtxt(inFileStr, delimiter=',')

        # Get lengh of map
        self.nX = self.inFile.shape[0]
        self.nY = self.inFile.shape[1]
        self.pixelX = SCREEN_WIDTH/self.nX
        self.pixelY = SCREEN_HEIGHT/self.nY
        # Initialize screen
        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
        self.screen.fill(COLOR_BACKGROUND)
        # Set initial robot pos
        self.initX = initX
        self.initY = initY

        # Define discrete action space
        self.action_space = spaces.Discrete(4)
        # Define obs space as a single pixel
        self.observation_space = spaces.Box(low=0, high=max(SCREEN_WIDTH, SCREEN_HEIGHT), shape=
                (2,), dtype=np.uint16)

    def step(self, action):
        done = False
        reward = 0
        self.step_counter += 0.05
        # get increment from discrete action 
        increment = self._get_vel_from_action(action)
        # Move robot in desired direction
        pygame.draw.rect(self.screen, COLOR_BACKGROUND, self.robot)
        self.robot.move_ip(increment[0], increment[1])

        # Define collision sensors so they dont overflow screen size
        top_sensor = (self.robot.midtop[0], max(self.robot.midtop[1] - 1, 0))
        bottom_sensor = (self.robot.midbottom[0], min(self.robot.midbottom[1] + 1, SCREEN_HEIGHT))
        right_sensor = (min(self.robot.midright[0] + 1 , SCREEN_WIDTH), self.robot.midright[1])
        left_sensor = (max(self.robot.midleft[0] - 1, 0), self.robot.midleft[1])

        # In case of collision revert move
        if (self.screen.get_at(top_sensor)[:3] == COLOR_WALL
         or self.screen.get_at(bottom_sensor)[:3] == COLOR_WALL
          or self.screen.get_at(right_sensor)[:3] == COLOR_WALL
           or self.screen.get_at(left_sensor)[:3] == COLOR_WALL):
            self.robot.move_ip(-increment[0], -increment[1])
            reward -= 5

        if self.debug:
            print(str(self.screen.get_at(top_sensor)[:3]))
            print(str(self.screen.get_at(bottom_sensor)[:3]))
            print(str(self.screen.get_at(right_sensor)[:3]))
            print(str(self.screen.get_at(left_sensor)[:3]))

        # Update screen
        pygame.draw.rect(self.screen, COLOR_ROBOT, self.robot)
        pygame.display.update()

        time.sleep(SIM_PERIOD_MS/1000.0)

        obs = self._get_obs()

        # Reward calculation
        # Check if goal is reached
        if obs == (GOAL_X, GOAL_Y):
            reward += 100
            done = True
        # Use dense reward signal as L1 norm    
        else:
            reward += 7 - (GOAL_X - obs[0]) * 0.01
            reward += 5 - (GOAL_Y - obs[1]) * 0.01

        # Penalize time spent    
        reward -= self.step_counter

        if self.debug:
            print("Reward: "+str(reward))
            print("Current cell: "+str(obs))
            print("Action taken: "+str(action))

        return obs, reward, done, {}

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
        self.step_counter = 0.0

        return self._get_obs()

    def render(self, mode='human', close=False):
        return

    # Returns a vector with every pixel color from screen
    def _get_obs(self):
        pixArray = []
        #maxW = int(self.screen.get_width())
        #maxH = int(self.screen.get_height())
        # for i in range(maxW):
        #    for j in range(maxH):
        #        pixArray.append(self.screen.get_at((i, j))[:3])
#
        # print(str(self.robot.center))
        return self.robot.center

    # Given a discrete action returns pixels to move and direction
    def _get_vel_from_action(self, action):
        if action == UP:
            return [0, -self.pixelY/2.0]
        elif action == DOWN:
            return [0, self.pixelY/2.0]
        elif action == RIGHT:
            return [self.pixelX/2.0, 0]
        elif action == LEFT:
            return  [-self.pixelX/2.0, 0]
        return None
