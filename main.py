'''
Import thư viện để sử dụng code
'''
import pygame, sys, random
from pygame.locals import *

'''
Khai báo các biến định dạng màn hình, tài nguyên trong game
Vẽ nền cho game
'''

WINDOWWIDTH = 289
WINDOWHEIGHT = 511


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
FPS = 60
fpsClock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Flappy Dinosaur')


def main():
    '''
    Gán biến cho class và khai báo ra hàm gameStart cũng như game play
    '''
    dinosaur = Dinosaur()
    columns = Columns()
    score = Score()
    
    while True:
        gameStart(dinosaur)
        gamePlay(dinosaur, columns, score)

def gamePlay(dinosaur, columns, score):
    '''
    Khai báo giá trị của từng class
    Tạo vòng lặp game và bắt sự kiện MOUSEBUTTONDOWN trong vòng lặp game
    Cho hàm isGameOver vào để kết thúc game khi xảy ra va chạm
    '''
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
    '''
    Tạo màn hình đầu game trước khi bắt đầu trò chơi 
    '''
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
    '''
    Khai báo giá trị của class
    Vẽ nhân vật lên màn hình game
    Tạo hàm chuyển động rơi xuống và bắt sự kiện mouseClick để bay lên
    '''
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
    '''
    Khai báo giá trị của class cho 3 cột 
    Vẽ 3 cột lên màn hình game
    Tạo chuyển động cho cột di chuyển sang trái sau đó xóa cột đi ra khỏi màn hình và tạo cột mới
    '''
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
    '''
    Hàm kiểm tra va chạm theo hình chữ nhật
    '''
    if rect1[0] <= rect2[0]+rect2[2] and rect2[0] <= rect1[0]+rect1[2] and rect1[1] <= rect2[1]+rect2[3] and rect2[1] <= rect1[1]+rect1[3]:
        return True
    return False

def isGameOver(dinosaur, columns):
    '''
    Hàm kiểm tra gameover
    '''
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
