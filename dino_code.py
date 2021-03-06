import os
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

class Dinosaur():

    def __init__(self, sizex=-1,sizey=-1):
        self.images, self.rect = files_load('dino.png', 5, 1, sizex, sizey, -1)     #getting image list and a rectange from files
        self.images_duck,self.rectduck = files_load('dino_ducking.png',2,1,59,sizey,-1) #getting image list for ducking and a rectange from files
        self.image = self.images[0]     #getting a single image from the list
        self.rect.bottom = height-3 #setting dinosuar on ground
        self.rect.left = 40 #setting dinosaur position from left
        self.standing_width = self.rect.width #width of standing sprite
        self.ducking_width = self.rectduck.width #width of ducking sprite 
        self.isJumping = False #jumping flag
        self.jumpSpeed = 11.5 #dinosaur jumping speed 
        self.isDead= False #Flag for game failure
        self.isDucking= False #Flag for duck movement 
        self.num = 0 #used to cycle through animations 
        self.counter=0 #used to cycle through animations
        self.movementVector = [0,0] #Array used by function move() from pygame. Rectangle is moved by the [x,y]


    def checkIfLanded(self):    #checks have the dinosaur landed or not
        if self.rect.bottom>height-3:
            self.rect.bottom = height-3
            self.isJumping = False


    def update(self):

        #if the dinosaur is jumping, then he eventually starting to fall
        if self.isJumping:  
            self.movementVector[1] = self.movementVector[1] + gravity

        # this section deals with sprite animation, cycles through walking animation, resets at %5 (walking animation has only 5 sprites 0-4, ducking animation has only 2 0-1)     
        if self.isDucking:  
            if self.counter % 5 == 0:
                self.num = (self.num + 1)%2
        else:
            if self.counter % 5 == 0:
                self.num = (self.num + 1)%2 + 2

        if not self.isDucking:
            self.image = self.images[self.num]
            self.rect.width = self.standing_width
        else:
            self.image = self.images_duck[(self.num)%2]
            self.rect.width = self.ducking_width
        self.counter = (self.counter + 1)
        
        self.rect = self.rect.move(self.movementVector) #changing the position of the dinosaur
        self.checkIfLanded()

    def draw(self):     #drawing a dinosaur
        if self.isDead:
            if self.isDucking:
                self.isDucking = False
            self.image = self.images[4]
        screen.blit(self.image, self.rect)
    

class Cactus(pygame.sprite.Sprite): #cactus class; pygame.sprite.Sprite is a simple base class for visible game objects from pygame library
    def __init__(self, group, speed=5, sizex=-1,sizey=-1):
        pygame.sprite.Sprite.__init__(self) #parent class constructor
        self.images, self.rect = files_load('cacti-small.png',3,1,sizex,sizey,-1)
        self.image = self.images[random.randrange(0,3)]
        self.rect.left = width + self.rect.width
        self.rect.bottom = height-3
        self.movementVector = [-1*speed, 0]

        self.add(group) #adding a cactus to a group

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect = self.rect.move(self.movementVector)

        if self.rect.right<0:   #Cactus is removed from the group cactuses when it goes out of the screen
            self.kill()


class DinoObsticle(pygame.sprite.Sprite): #pterodactyl class, pygame.Sprite is bacuse its a visible game object
    def __init__(self,group,speed=5,sizex=-1,sizey=-1):
        pygame.sprite.Sprite.__init__(self)
        self.images,self.rect = files_load('ptera.png',2,1,sizex,sizey,-1)
        self.ptera_height = [height-35,height-50,height-65,height-25] #different heigh pterodactyl can spawn at
        self.rect.centery = self.ptera_height[random.randrange(0,4)] #set randomness to height of pterodactyl
        self.image = self.images[0]
        self.rect.left = width + self.rect.width #set position from left side of screen
        self.movementVector = [-1*speed,0]
        self.num = 0 #used to cycle through wing animation
        self.counter = 0 #used to cycle through wing animation
        self.add(group) #adding pterodactyl to pterodactyl group

    def draw(self):
        screen.blit(self.image,self.rect)

    def update(self):
        if self.counter % 8 == 0: #frequencey of animation
            self.num = (self.num+1)%2
        self.image = self.images[self.num]
        self.rect = self.rect.move(self.movementVector) 
        self.counter = (self.counter + 1)
        if self.rect.right < 0: #goes beyond screen kill it
            self.kill()


class Ground():

    def __init__(self, speed= 1):       
        self.image,self.rect = env_img_load('ground.png',-1,-1,-1)      #getting ground image
        self.image2,self.rect2 = env_img_load('ground.png',-1,-1,-1)    #getting the same image, because one is not enough to have the moving ground
        self.rect.bottom = height       #placing the ground to the bottom of the screen
        self.rect2.bottom = height
        self.rect2.left = self.rect.right   # second ground picture initially will be to the right of the first one
        self.speed = speed      # setting the speed of ground motion 

    def draw(self):     #drawing a ground
        screen.blit(self.image,self.rect)           
        screen.blit(self.image2,self.rect2)

    def update(self):
        self.rect.left -= self.speed        #ground pictures will be moving to the left
        self.rect2.left -= self.speed

        if self.rect.right <0:                  # if the fist picture is gone out of the screen, it moved to the right of the second one
            self.rect.left = self.rect2.right

        if self.rect2.right <0:                 # the opposite to the previous one
            self.rect2.left = self.rect.right


# Function to extract numbers for a score
def Numbers(number):
    if number > -1:
        num = []
        while(number/10 != 0):
            num.append(number%10)
            number = int(number/10)

        num.append(number%10)
        for i in range(len(num),5):
            num.append(0)
        num.reverse()

        return num

class Scores():
    def __init__(self, x=-1, y=-1):
        self.score = 0
        self.numbers,self.numbersrect = files_load('numbers.png',12,1,11,int(11*6/5),-1)
        self.image = pygame.Surface((55,int(11*6/5)))
        self.rect = self.image.get_rect()

        if x == -1:
            self.rect.left = width * 0.89
        else:
            self.rect.left = x

        if y == -1:
            self.rect.top = height * 0.1
        else:
            self.rect.top = y

    def draw(self):
        screen.blit(self.image,self.rect)

    def update(self,score):
        score_num = Numbers(score)
        self.image.fill(background_color)

        for i in score_num:
            self.image.blit(self.numbers[i],self.numbersrect)
            self.numbersrect.left += self.numbersrect.width
        self.numbersrect.left = 0


def game():
    global high_score
    gameSpeed = 5
    Dino = Dinosaur(40,40)
    game_ground = Ground(gameSpeed)
    cactuses = pygame.sprite.Group()    #creating cactuses group
    pterodactyl = pygame.sprite.Group() #creating pterodactyl group
    last_obstacle = pygame.sprite.Group()   #last_obstacle is meant to keep track of the last created obstacle to decide when to create a new one
    scr = Scores()
    highscr = Scores(width * 0.78) 
    QuitFlag = False
    numbers,numbersrect = files_load('numbers.png',12,1,11,int(11*6/5),-1)
    HI_img = pygame.Surface((22,int(11*6/5)))
    HI_rect = HI_img.get_rect()
    HI_img.fill(background_color)
    HI_img.blit(numbers[10],numbersrect)
    numbersrect.left += numbersrect.width
    HI_img.blit(numbers[11],numbersrect)
    HI_rect.top = height * 0.1
    HI_rect.left = width * 0.73


    while QuitFlag== False:
        while Dino.isDead== False:
            for event in pygame.event.get():   
                if event.type == pygame.QUIT:
                    QuitFlag = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if (Dino.rect.bottom == height-3 and Dino.isDucking == False) :
                            Dino.isJumping = True
                            if pygame.mixer.get_init() != None:
                                jump_sound.play()
                            Dino.movementVector[1] = -1*Dino.jumpSpeed

                    if event.key == pygame.K_DOWN:
                        if not (Dino.isJumping or Dino.isDead):
                            Dino.isDucking = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        Dino.isDucking = False

            for i in cactuses:      #forcing cactuses to move
                i.movementVector[0] = -1*gameSpeed
                if pygame.sprite.collide_mask(Dino,i):
                    Dino.isDead = True
                    if pygame.mixer.get_init() != None:
                        fail_sound.play()
            
            for f in pterodactyl:
                f.movementVector[0] = -1*gameSpeed
                if pygame.sprite.collide_mask(Dino,f):
                    Dino.isDead = True
                    if pygame.mixer.get_init() != None:
                        fail_sound.play()


            if len(cactuses)<2: 
                if len(cactuses)==0 and random.randrange(0,10)==1:    #creating the first obstacle which always gonna be a cactus
                    last_obstacle.empty()
                    last_obstacle.add(Cactus(cactuses, gameSpeed, 40, 40))
                else:
                    for i in last_obstacle:
                        if i.rect.right < width*0.5:    #if last obstacle went through the half of the screen we can create another cactus
                            last_obstacle.empty()
                            last_obstacle.add(Cactus(cactuses, gameSpeed, 40, 40))

            if len(pterodactyl)==0 and random.randrange(0,25) == 1 :# randomness of spawnining 
                for l in last_obstacle:
                    if l.rect.right < width*0.75: #if last obstacle went through the 70% of the screen we can create another ptera
                        last_obstacle.empty() #empty of all obstacles 
                        last_obstacle.add(DinoObsticle(pterodactyl,gameSpeed, 46, 40)) #add pterodactyl obsticle with given gamespeed

            screen.fill(background_color)
            Dino.draw()
            Dino.update()
            game_ground.draw()
            game_ground.update()
            cactuses.draw(screen)
            cactuses.update()
            pterodactyl.draw(screen)
            pterodactyl.update()
            scr.draw()
            scr.update(Dino.counter)
            highscr.update(high_score)

            if high_score != 0:
                highscr.draw()
                screen.blit(HI_img,HI_rect)

            pygame.display.update()
            clock.tick(FPS)

            if(Dino.counter%1000==999):
                game_ground.speed+=1 
                gameSpeed+=1

            if QuitFlag:
                break

        while Dino.isDead:
                
            if Dino.counter > high_score:
                high_score = Dino.counter

            for event in pygame.event.get():   
                if event.type == pygame.QUIT:
                    QuitFlag = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        Dino.isDead = False
                        game()
                        
            if QuitFlag:
                break 

        pygame.quit()
        quit()


game()
