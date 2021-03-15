import pygame
from pygame.locals import *

from life import GameOfLife
from ui import UI

import argparse

parser = argparse.ArgumentParser(description='data')
parser.add_argument('-width','--width', type=int, help='width of data')
parser.add_argument('-height','--height', type=int, help='height of data')
parser.add_argument('-cell-size','--cellsize', type=int, help='cellsize of data')
args = parser.parse_args()

class GUI(UI):

    def __init__(self, life: GameOfLife, cell_size: int=10, speed: int=10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.width = life.rows * self.cell_size
        self.height = life.cols * self.cell_size
        self.screen = pygame.display.set_mode((self.width,self.height))
        pass

    def draw_lines(self) -> None:
        # Copy from previous assignment
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (0, y), (self.width, y))
        pass

    def draw_grid(self) -> None:
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                if self.life.curr_generation[i][j] == 1:
                    color = pygame.Color('green')
                else:
                    color = pygame.Color('white')
                pygame.draw.rect(self.screen,color,(j*self.cell_size,i*self.cell_size,self.cell_size,self.cell_size))
    def run(self) -> None:
        # Copy from previous assignment
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        running = True
        pausa = False
        while running:
            
            if not pausa:
                self.draw_grid()
                self.draw_lines()
                pygame.display.flip()
                clock.tick(self.speed)
                self.life.step()
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x_mouse, y_mouse = pygame.mouse.get_pos()
                        column = x_mouse // self.cell_size
                        row = y_mouse // self.cell_size
                        self.life.curr_generation=life.prev_generation
                        if self.life.curr_generation[row][column] == 0:
                            self.life.curr_generation[row][column] = 1
                        else:
                            self.life.curr_generation[row][column] = 0                        
                        self.draw_grid()                      
                        self.draw_lines()
                        pygame.display.flip()
                if event.type == pygame.KEYDOWN:
                    if event.key == K_SPACE:
                        pausa = not pausa             
            
        pass
if __name__ == '__main__':
    r = int(args.width//args.cellsize)
    c = int(args.height//args.cellsize)
    life = GameOfLife((r, c), False)
    gui = GUI(life, args.cellsize , 1)
    gui.run()
