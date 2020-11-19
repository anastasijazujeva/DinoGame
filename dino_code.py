import os
import sys
import pygame
from pygame import *
import random

# Initialize all pygame modules
pygame.init()

# Screen settings
screen_size = (width,height) = (610,160)
FPS = 60 # frame rate
gravity = 0.6

black = (0,0,0)
white = (255,255,255)
background_color = (235,235,235)

# Initialize a high score
high_score = 0

# Display window
screen = pygame.display.set_mode(screen_size) # returns a pygame.Surface representing the window on screen. pygame.Surface is used to represent any image
clock = pygame.time.Clock() # clock object to track an amount of time
pygame.display.set_caption("Dinosaur Game") # set a title of the game

'''
    We gonna do it at the end. Now without sounds
    
jump_sound = pygame.mixer.Sound('foldername/jump.mp3')
fail_sound = pygame.mixer.Sound('foldername/fail.mp3')
'''
