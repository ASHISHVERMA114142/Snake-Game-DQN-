from turtle import width
import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np
import math
pygame.init()
font = pygame.font.Font(None,25)

# Reset 
# Reward
# Play(action) -> Direction
# Game_Iteration
# is_collision


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
 
Point = namedtuple('Point','x , y')


# Basic initilization of the snakegame envoirment ...
BLOCK_SIZE=20
SPEED = 40
WHITE = (255,255,255)
RED = (200,0,0)
BLUE1 = (0,0,255)
BLUE2 = (0,100,255)
BLACK = (0,0,0)

class SnakeGameAI:
    def __init__(self,w=640,h=480):
        self.w=w
        self.h=h
        #init display
        # this will set the envoirment height and width
        self.display = pygame.display.set_mode((self.w,self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        
        #init game state 
        #   this will reset all the things...
        self.reset()
    def reset(self):
        # default direction of the snake movement...
        self.direction = Direction.RIGHT
        # calculation of the head position...
        self.head = Point(self.w/2,self.h/2)
        self.snake = [self.head,
                      Point(self.head.x-BLOCK_SIZE,self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE),self.head.y)]
        self.score = 0
        self.food = None
        # first we will np.place the food ...
        self._place__food()
        self.frame_iteration = 0
      
    # this will set the random food and also check that the food position will not conflict with the sanke body...
    def _place__food(self):
        x = random.randint(0,(self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = random.randint(0,(self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food = Point(x,y)
        if(self.food in self.snake):
            self._place__food()


    def play_step(self,action):
        self.frame_iteration+=1
        # 1. Collect the user input like uesr will press key 
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                pygame.quit()
                quit()
            
        # 2. Move according to the move button press 
        self._move(action)
        self.snake.insert(0,self.head)

        # 3. Check if game Over
        reward = 0  # eat food: +10 , game over: -10 , else: 0
        # saves the reward 
        game_over = False 
        if(self.is_collision() or self.frame_iteration > 100*len(self.snake) ):
            # if game is over then code will terminate ...
            game_over=True
            reward = -10
            return reward,game_over,self.score
        # 4. Place new Food or just move
        if(self.head == self.food):
            # if the head of the sanke will hit the food then score will increase..
            self.score+=1
            reward=10
            self._place__food()
            
        else:
            self.snake.pop()
        
        # 5. Update UI and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. Return game Over and Display Score
        
        return reward,game_over,self.score


    # design the display of the envoirment ... after each food each ui will updated...
    def _update_ui(self):
        self.display.fill(BLACK)
        for pt in self.snake:
            pygame.draw.rect(self.display,BLUE1,pygame.Rect(pt.x,pt.y,BLOCK_SIZE,BLOCK_SIZE))
            pygame.draw.rect(self.display,BLUE2,pygame.Rect(pt.x+4,pt.y+4,12,12))
        pygame.draw.rect(self.display,RED,pygame.Rect(self.food.x,self.food.y,BLOCK_SIZE,BLOCK_SIZE))
        text = font.render("Score: "+str(self.score),True,WHITE)
        self.display.blit(text,[0,0])
        pygame.display.flip()
    
    #  This will be the output of the snake game...
    def _move(self,action):
        # Action
        # [1,0,0] -> Straight
        # [0,1,0] -> Right Turn 
        # [0,0,1] -> Left Turn

        clock_wise = [Direction.RIGHT,Direction.DOWN,Direction.LEFT,Direction.UP]
        idx = clock_wise.index(self.direction)
        if np.array_equal(action,[1,0,0]): # go straight
            new_dir = clock_wise[idx]   
        elif np.array_equal(action,[0,1,0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx] # right Turn
        else:
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx] # Left Turn
        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        #  according to the head position and the direction of the head will change...
        if(self.direction == Direction.RIGHT):
            x+=BLOCK_SIZE
        elif(self.direction == Direction.LEFT):
            x-=BLOCK_SIZE
        elif(self.direction == Direction.DOWN):
            y+=BLOCK_SIZE
        elif(self.direction == Direction.UP):
            y-=BLOCK_SIZE
        self.head = Point(x,y)
    
    # this will detect the collision of the snake with the box...
    def is_collision(self,pt=None):
        if(pt is None):
            pt = self.head
        #hit boundary
        if(pt.x>self.w-BLOCK_SIZE or pt.x<0 or pt.y>self.h - BLOCK_SIZE or pt.y<0):
            return True
        if(pt in self.snake[1:]):
            return True
        return False
