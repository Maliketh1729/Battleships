import time, sys, os, pygame, random, pickle
#import PySimpleGUI as psG
from pygame.locals import *                #Allows easier use of pygame functions
#from tkinter import *
#from PIL import Image, ImageTk
pygame.init() #Initializes pyGame
clock = pygame.time.Clock()         #Limits FPS to 60

#Much of this code was imported from my personal platformer project, so it may be a little messy

pickleExists = os.path.exists(r"Z:/Yr 10 Computer Science/Personal Projects/PyGame Experimentation/Battleships/highScore.pkl")
if pickleExists == True:
    with open('highScore.pkl', 'rb') as f:                        #In read-only mode
        highScore = int(pickle.load(f))
        pickleConfirmation = True
        print("High Score: ",highScore,".Can you beat it?")
else:
    print("No score file found - high score inaccessible")
    pickleConfirmation = False
curScore = 0

#Apologies, it may require another module on top of pyGame - pySimpleGUI.
#It can be installed through powershell with 'python -m pip install PySimpleGUI'

ScreenSizeObj = pygame.display.Info()
worldx, worldy = ScreenSizeObj.current_w,ScreenSizeObj.current_h
print(worldx,worldy)
screen = pygame.display.set_mode([worldx, worldy])
pygame.display.set_caption("40k Battleships-Now with extra spaghetti!")
ty = 64
tx = 64
global level #Sorry, I know its bad practice but I couldn't find a way around it
level = 0
running = True
#Background
background = pygame.image.load("Battleships Images/UI/background.png")

hit_ships = pygame.sprite.Group()




##############
debug = False #              Makes ships visible
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

        self.torpedos = 35

        for i in range(1,self.aniCycles + 1): #Loads the two frames of animation
            img = pygame.image.load("Battleships Images/UI/Cursor.png")
            img.convert_alpha()
            self.images.append(img)
            self.image = self.images[self.curFrame]
            self.bigrect = self.image.get_rect()
            self.rect = self.bigrect.inflate(-32,-16)


    def update(self):
        pressed_keys = pygame.key.get_pressed()               
        mousePos = pygame.mouse.get_pos() #use rect.collidepoint for detection
        if pressed_keys[K_SPACE] and self.torpedos > 0: #If space is pressed and torpedos remain:
            hit = False
            torpedoCount = 0
            for ship in ship_list:                                                                     
                if ship.rect.collidepoint(mousePos) == True:    #If mouse position intersects the rect box:
                    print("Firing Shot!")#Fire
                    print("HIT!!!!!!")
                    print("Ships left:", len(ship_list)-1,". Shots left:", self.torpedos)
                    global curScore
                    print("Current score is: ", curScore)
                    curScore += 1                      #Could add a combo system;hit more ships in a row, ^ mult?. #Not updating for some reason-being reset?
                    ship_list.remove(ship)
                    hit_ships.add(ship)               #Delete the hit ship
                    ship.image = pygame.image.load("Battleships Images/Ships/hit_Ship.png").convert_alpha()
                    self.torpedos -= 1
                    hit = True
                    time.sleep(0.1)

            if hit == False:
                self.torpedos -= 1
                print("Firing Shot!")#Fire
                print("Miss")
                print("Ships left are stll:", len(ship_list)-1,". Shots left:", self.torpedos)
                time.sleep(0.1)
            ship = []                                     #Clear the log of collisions

        elif pressed_keys[K_ESCAPE]:
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

#need to make empty space spawn in all non-occupied areas
#maybye make a list of all allowed positions, allocate ships to it randomly and 0s become empty?

horiPos = [0,128,256,384,512,640,768,896,1024,1152,1280,1408,1536,1664]
vertPos = [0,128,256,384,512,640,768,896,1024]
#possLoc = [[horipos[0],vertpos[0]],[horipos[1],vertpos[0]...]      This would work but would be very inefficient to type

#could store ship locations in a list and regenerate if there is any overlap?


class Level:                                             
    def ship(level, tx, ty):
        ship_list = pygame.sprite.Group()
        hshloc = []
        vshloc = []
        i = 0
        #Place spike locations for stage 1 here 
        hshloc.append((horiPos[random.randint(0,8)], vertPos[random.randint(0,7)], 4))  #CARRIER         #The last number is how many ships in a row there are -1                       
        hshloc.append((horiPos[random.randint(0,11)], vertPos[random.randint(0,7)], 1)) #SUB
        vshloc.append((horiPos[random.randint(0,11)], vertPos[random.randint(0,6)], 1)) #DESTROYER
        vshloc.append((horiPos[random.randint(0,11)], vertPos[random.randint(0,5)], 2))  #CRUISER                   
        vshloc.append((horiPos[random.randint(0,11)], vertPos[random.randint(0,4)], 3)) #BATTLESHIP
        while i < len(hshloc):                                    
            j = 0
            while j <= hshloc[i][2]:  #repeat as long as no exceeding index 2 (how many times it tiles)
                shp = Ship((hshloc[i][0] + (j * (2*tx))), hshloc[i][1], tx, ty, pygame.image.load("Battleships Images/Ships/Battleship_Large.png"))  #Change distance between ships with (j*tx)
                ship_list.add(shp)        #^move this to            ^here to flip the tiling vertically
                j = j + 1                 
            i = i + 1
        i = 0
        while i < len(vshloc):                                    
            j = 0
            while j <= vshloc[i][2]:  #repeat as long as no exceeding index 2 (how many times it tiles)
                shp = Ship((vshloc[i][0]), vshloc[i][1] + (j * (2*tx)), tx, ty, pygame.image.load("Battleships Images/Ships/Battleship_Large.png"))  #Change distance between ships with (j*tx)
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
        empty_list = []




Level.newLevel(level, tx, ty)

player = Player() #spawn the player character
colGen = True
while colGen == True:                                  #While ships are colliding:
    colGen = False                                    
    ships = ship_list.sprites()
    for i, ship1 in enumerate(ships):                  #Goes through ship list and takes both value + index
        for ship2 in ships[i+1:]:                          #Takes another ship from it that is next
            if pygame.sprite.collide_mask(ship1, ship2):        #If they collide(mask is more accurate than rect)
                Level.newLevel(level, tx, ty)                        #Regenerate the level
                colGen = True
    
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
    if debug == True:              #Debug allows seeing the ship locs
        ship_list.draw(screen)
    hit_ships.draw(screen)

    if not ship_list:
        print("All ships destroyed, you win!")  #For some reason an empty sprite group is considered false
        running = False
        curScore += player.torpedos
        if curScore > highScore and pickleConfirmation == True:
            with open('highScore.pkl', 'wb') as f:
                pickle.dump(curScore, f)
            print("New High Score: ", curScore)

    if player.torpedos <= 0:                    #ordered so that if the player runs out of torpedos on the final shot they still win
        print("Game Over. You Lose")
        running = False
        curScore -= 5
        if curScore > highScore and pickleConfirmation == True:
            with open('highScore.pkl', 'wb') as f:
                pickle.dump(curScore, f)
            print("New High Score: ", curScore)


    pygame.display.update()
    screen.fill("black")
