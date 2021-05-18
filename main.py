import pygame, sys, random
from pygame.locals import *

WINDOWWIDTH = 289
WINDOWHEIGHT = 511
SCREEN = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
GROUNDY = WINDOWHEIGHT * 0.8
GAME_GALLERY = {}
GAME_SOUNDS = {}
PLAYER = 'gallery/img/khunglong.png'
BACKGROUND = 'gallery/img/background.png'
PIPE = 'gallery/img/pipe.png'

DINOSAURWIDTH = 20
DINOSAURHEIGHT = 5
G = 0.5
SPEEDFLY = -8
DINOSAURIMG = pygame.image.load('gallery/img/khunglong.png')

COLUMNWIDTH = 60
COLUMNHEIGHT = 300
BLANK = 170
DISTANCE = 250
COLUMNSPEED = 2
COLUMNIMG = pygame.image.load('gallery/img/column.png')

BACKGROUND = pygame.image.load('gallery/img/background.png')

pygame.init()
FPS = 50
fpsClock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Flappy Dinosaur')


def main(): 
    dinosaur = Dinosaur()
    columns = Columns()
    score = Score()
    
    while True:
        gameStart(dinosaur)
        gamePlay(dinosaur, columns, score)

def gamePlay(dinosaur, columns, score):
    dinosaur.__init__()
    dinosaur.speed = SPEEDFLY
    columns.__init__()
    score.__init__()
    while True:
        mouseClick = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                mouseClick = True
        
        DISPLAYSURF.blit(BACKGROUND, (0, 0))
        columns.draw()
        columns.update()
        dinosaur.draw()
        dinosaur.update(mouseClick)
        score.draw()
        score.update(dinosaur, columns)

        if isGameOver(dinosaur, columns) == True:
            return

        pygame.display.update()
        fpsClock.tick(FPS)

def gameStart(dinosaur):
    dinosaur.__init__()

    font = pygame.font.SysFont('consolas', 40)
    headingSuface = font.render('Flappy T-rex', True, (255, 0, 0))
    headingSize = headingSuface.get_size()
    
    font = pygame.font.SysFont('consolas', 20)
    commentSuface = font.render('Click to start', True, (0, 255, 0))
    commentSize = commentSuface.get_size()
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                return

        DISPLAYSURF.blit(BACKGROUND, (0, 0))
        dinosaur.draw()
        DISPLAYSURF.blit(headingSuface, (int((WINDOWWIDTH - headingSize[0])/2), 80))
        DISPLAYSURF.blit(commentSuface, (int((WINDOWWIDTH - commentSize[0])/2), 400))

        pygame.display.update()
        fpsClock.tick(FPS)

class Score():
    def __init__(self):
        self.score = 0
        self.addScore = True
    
    def draw(self):
        font = pygame.font.SysFont('consolas', 60)
        scoreSuface = font.render(str(self.score), True, (0, 255, 0))
        textSize = scoreSuface.get_size()
        DISPLAYSURF.blit(scoreSuface, (int((WINDOWWIDTH - textSize[0])/2), 60))
    
    def update(self, dinosaur, columns):
        collision = False
        for i in range(3):
            rectColumn = [columns.ls[i][0] + columns.width, columns.ls[i][1], 1, columns.blank]
            rectBird = [dinosaur.x, dinosaur.y, dinosaur.width, dinosaur.height]
            if rectCollision(rectBird, rectColumn) == True:
                collision = True
                break
        if collision == True:
            if self.addScore == True:
                self.score += 1
            self.addScore = False
        else:
            self.addScore = True

class Dinosaur():
    def __init__(self):
        self.width = DINOSAURWIDTH
        self.height = DINOSAURHEIGHT
        self.x = (WINDOWWIDTH - self.width)/2
        self.y = (WINDOWHEIGHT- self.height)/2
        self.speed = 0
        self.suface = DINOSAURIMG
    def draw(self):
        DISPLAYSURF.blit(self.suface, (int(self.x), int(self.y)))   
    def update(self, mouseClick):
        self.y += self.speed + 0.5*G
        self.speed += G
        if mouseClick == True:
            self.speed = SPEEDFLY

class Columns():
    def __init__(self):
        self.width = COLUMNWIDTH
        self.height = COLUMNHEIGHT
        self.blank = BLANK
        self.distance = DISTANCE
        self.speed = COLUMNSPEED
        self.surface = COLUMNIMG
        self.ls = []
        for i in range(3):
            x = i*self.distance
            y = random.randrange(60, WINDOWHEIGHT - self.blank - 60, 20)
            self.ls.append([x, y])       
    def draw(self):
        for i in range(3):
            DISPLAYSURF.blit(self.surface, (self.ls[i][0], self.ls[i][1] - self.height))
            DISPLAYSURF.blit(self.surface, (self.ls[i][0], self.ls[i][1] + self.blank))
    def update(self):
        for i in range(3):
            self.ls[i][0] -= self.speed
        if self.ls[0][0] < -self.width:
            self.ls.pop(0)
            x = self.ls[1][0] + self.distance
            y = random.randrange(60, WINDOWHEIGHT - self.blank - 60, 10)
            self.ls.append([x, y])

def rectCollision(rect1, rect2):
    if rect1[0] <= rect2[0]+rect2[2] and rect2[0] <= rect1[0]+rect1[2] and rect1[1] <= rect2[1]+rect2[3] and rect2[1] <= rect1[1]+rect1[3]:
        return True
    return False

def isGameOver(dinosaur, columns):
    for i in range(3):
        rectBird = [dinosaur.x, dinosaur.y, dinosaur.width, dinosaur.height]
        rectColumn1 = [columns.ls[i][0], columns.ls[i][1] - columns.height, columns.width, columns.height]
        rectColumn2 = [columns.ls[i][0], columns.ls[i][1] + columns.blank, columns.width, columns.height]
        if rectCollision(rectBird, rectColumn1) == True or rectCollision(rectBird, rectColumn2) == True:
            return True
    if dinosaur.y + dinosaur.height < 0 or dinosaur.y + dinosaur.height > WINDOWHEIGHT:
        return True
    return False

        
if __name__ == '__main__':
    main()
