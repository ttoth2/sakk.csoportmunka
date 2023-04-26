import pygame
import time

FPS=60
WIDTH, HEIGHT=800,800
ROWS,COLS=8,8
SQUARE_SIZE=WIDTH//COLS

WHITE=(255,255,255)
BLACK=(0,0,0)

WIN=pygame.display.set_mode((WIDTH,HEIGHT))
def main():
    run=True
    ora=pygame.time.Clock()
    while run:
        ora.tick(FPS)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False

class Board:
    def __init__ (self):
        self.board =[]
        self.selected.piece=None
    def draw_squares(self,win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2,ROWS,2):
                pygame.draw.rect(win,WHITE,(row*SQUARE_SIZE,col*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE))



