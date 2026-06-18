import time, sys, os, pygame
import PySimpleGUI as psG
from pygame.locals import *                #Allows easier use of pygame functions
#from tkinter import *
#from PIL import Image, ImageTk
pygame.init() #Initializes pyGame
clock = pygame.time.Clock()         #Limits FPS to 60

#Much of this code was imported from my personal platformer project, so it may be a little messy

#Apologies, it requires another module on top of pyGame - pySimpleGUI.
#It can be installed through powershell with 'python -m pip install PySimpleGUI'

ScreenSizeObj = pygame.display.Info()
worldx, worldy = ScreenSizeObj.current_w,ScreenSizeObj.current_h
print(worldx,worldy)
screen = pygame.display.set_mode([worldx, worldy])
pygame.display.set_caption("40k Battleships")
ty = 64
tx = 64
global level #Sorry, I know its bad practice but I couldn't find a way around it
level = 0
running = True
#Background
background = pygame.image.load("Battleships Images/UI/background.png")




##############
debug = True #
##############

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.alive = True
        self.aniCounter = 0
        self.vertSpeed = 0
        self.curFrame = 0
        self.accRem = 0
        self.images = []
        self.aniCycles = 2

        for i in range(1,self.aniCycles + 1): #Loads the two frames of animation
            img = pygame.image.load("Battleships Images/UI/Cursor.png")
            #an easier way to add more frames of the animation - just add 1 more number to the next file
            img.convert_alpha()
            self.images.append(img)
            self.image = self.images[self.curFrame]
            self.bigrect = self.image.get_rect()
            self.rect = self.bigrect.inflate(-32,-16)


    def update(self):
        pressed_keys = pygame.key.get_pressed()
        mousePos = pygame.mouse.get_pos() #use rect.collidepoint for detection
        for ship in ship_list:
            if ship.rect.collidepoint(mousePos) == True:
                if pressed_keys[K_SPACE]:
                    print("Firing Shot!")

        if pressed_keys[K_ESCAPE]:
            running = False

        

    def animate(self):
        if self.aniCounter >= 20:                                    #Reduces the speeed of the animation 10x
            if self.curFrame >= self.aniCycles:                        #Resets the frame whenever it loops
                self.curFrame = 0
            self.image = self.images[self.curFrame]
            self.curFrame += 1
            self.aniCounter = 0

    def draw(self, surface):
        screen.blit(self.image, self.rect)

        

class UI(pygame.sprite.Sprite):
    def __init__(self, xloc,yloc, imgw, imgh, img):
        super().__init__()
        grid = pygame.image.load("Battleships Images/UI/grid.png")
        
        self.rect.y = yloc
        self.rect.x = xloc
        imgw = 128
        imgh = 128

    def draw(self, surface):
        screen.blit(grid, (0,0))
        screen.blit(background, (0,0))



class Ship(pygame.sprite.Sprite):
    def __init__(self, xloc,yloc, imgw, imgh, img):
        super().__init__()
        self.image = pygame.image.load("Battleships Images/Ships/Battleship_Large.png").convert_alpha()
        self.bigrect = self.image.get_rect()
        self.rect = self.bigrect.inflate(imgw,imgh)
        self.rect.y = yloc
        self.rect.x = xloc
        imgw = 256
        imgh = 256

    def draw(self, screen):
        screen.blit(self.image, self.rect)



class Level:                                             
    def ship(level, tx, ty):
        ship_list = pygame.sprite.Group()
        shloc = []   #sploc is a list which determines the location of the ships e.g. [0, 642,screenY,256]. it may be more efficient to add locs here.oly do when sure of a pos
        i = 0
        if level == 1:
             #Place spike locations for stage 1 here 
             shloc.append((64, worldy // 2,9))           #The last number is how many ships in a row there are                        
             shloc.append((worldx // 2, worldy -ty, 0))
        elif level == 2:
             shloc.append((worldx // 2+ty, worldy //2, 10))
             shloc.append((worldx // 2, worldy -ty, 10))
        while i < len(shloc):                                    
            j = 0
            while j <= shloc[i][2]:
                shp = Ship((shloc[i][0] + (j * (2.5*tx))), shloc[i][1], tx, ty, pygame.image.load("Battleships Images/Ships/Battleship_Large.png"))  #Change distance between ships with (j*tx)
                ship_list.add(shp)
                j = j + 1
            i = i + 1
        return ship_list


    def newLevel(level,tx,ty):
        level += 1
        Level.clearList()
        global ship_list 
        ship_list = Level.ship(level, tx, ty)       
        
    def clearList():
        ship_list = []






Level.newLevel(level, tx, ty)

player = Player() #spawn the player character
player.rect.y,player.rect.x = worldy // 2,worldx // 2    #moves to middle of screen


#Loop for the majority of the actual game
while running == True:
    clock.tick(60)            #Updates the clock
    #Allows quitting the game without Task Manager
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    

    player.update()
    
    player.animate()

    screen.blit(background,(0,0))

    player.draw(screen)
    ship_list.draw(screen)


    pygame.display.update()
    screen.fill("black")
