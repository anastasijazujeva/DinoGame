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
background_color = (235,235,235) # light gray

# Initialize a high score
high_score = 0

# Display window
screen = pygame.display.set_mode(screen_size) # returns a pygame.Surface representing the window on screen. pygame.Surface is used to represent any image
clock = pygame.time.Clock() # clock object to track seconds when Dino is running
pygame.display.set_caption("Dinosaur Game") # set a title of the game

# Adding sounds which are in the Files folder
# mixer module creates a new Sound object from a file and controls a playback
pointCount_sound = pygame.mixer.Sound('files/pointCount.wav') # point count sound
jump_sound = pygame.mixer.Sound('files/jump.wav') # sound when Dino jumps
fail_sound = pygame.mixer.Sound('files/fail.wav') # sound of failed game

# Function to load images for Dino environment
def env_img_load(name, size_x=-1, size_y=-1, colorkey=None):
    fullname = os.path.join('files', name) # os module provides functions for interacting with the operating system.
                                                # os.path module is used for common pathname manipulations
                                                    # os.path.join method is used for joining one or more path components intelligently
    img = pygame.image.load(fullname)
    img = img.convert() # change the pixel format of an image

    if colorkey is not None:
        if colorkey == -1:
            colorkey = img.get_at((0, 0)) # get a color value at a single pixel, position (0,0) (?)
        img.set_colorkey(colorkey, RLEACCEL) # RLEACCEL - provides better performance on non-accelerated displays

    if size_x != -1 or size_y != -1:
        img = pygame.transform.scale(img, (size_x, size_y)) # resize to new resolution

    return img, img.get_rect() # get_rect() - get the rectangular area of an image

# Function to load files from Files folder (there are stored images and sounds) for adding cactus, birds and other images
def files_load(filename, x, y, scale_x=-1, scale_y=-1, colorkey=None):
    fullname = os.path.join('files', filename)
    obj = pygame.image.load(fullname)
    obj = obj.convert()
    obj_rect = obj.get_rect()

    files = [] # free space to collect all images in the future

    # setting width and height for an image
    size_x = obj_rect.width/x
    size_y = obj_rect.height/y

    for i in range(0, y): # (0, y) - from 0 till y
        for j in range(0, x):
            rect = pygame.Rect((j * size_x, i * size_y, size_x , size_y)) # (left, top, width, height)
            img = pygame.Surface(rect.size) # object for representing images (takes rect - the line above)
            img = img.convert()
            img.blit(obj, (0,0), rect) # draw image passed obj onto another image passed to rect, position (0,0)

            if colorkey is not None:
                if colorkey == -1:
                    colorkey = img.get_at((0, 0))
                img.set_colorkey(colorkey, RLEACCEL)

            if scale_x != -1 or scale_y != -1:
                img = pygame.transform.scale(img, (scale_x, scale_y))

            files.append(img) # appends images to the end of the list

        file_rect = files[0].get_rect()

        return files, file_rect

