import pygame
import random

from pygame.locals import *
from typing import List, Tuple


Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:


    def __init__(self, width: int=640, height: int=480, cell_size: int=10, speed: int=10) -> None:

        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.screen_size = width, height
        self.screen = pygame.display.set_mode(self.screen_size)
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size
        self.speed = speed
        #self.grid = self.create_grid(randomize=True)


    def draw_lines(self) -> None:
        
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (0, y), (self.width, y))


    def run(self) -> None:
        
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.screen.fill(pygame.Color('white'))
            self.draw_lines()
            self.draw_grid()
            self.grid = self.get_next_generation()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


    def create_grid(self, randomize: bool=False) -> Grid:

        grid = []
        for i in range(self.cell_height):
            row = []
            for j in range(self.cell_width):
                if randomize:
                    cell = random.randint(0,1)
                else:
                    cell = 0
                row.append(cell)
            grid.append(row)
        return grid


    def draw_grid(self) -> None:
        
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                x = j * self.cell_size
                y = i * self.cell_size
                if self.grid[i][j] == 1:
                    pygame.draw.rect(self.screen, pygame.Color('green'), (x, y, self.cell_size, self.cell_size))
                else:
                    pygame.draw.rect(self.screen, pygame.Color('white'), (x, y, self.cell_size, self.cell_size))


    def get_neighbours(self, cell: Cell) -> Cells:

        cells = []
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if 0 <= i < self.cell_height and 0 <= j < self.cell_width and not(i == cell[0] and j == cell[1]):
                    cells.append(self.grid[i][j])
        return cells
        

    def get_next_generation(self) -> Grid:

        new_grid = self.create_grid()
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                k = sum(self.get_neighbours((i, j)))
                if self.grid[i][j] == 0:
                    if k == 3:
                        new_grid[i][j] = 1
                    else:
                        new_grid[i][j] = 0
                else:
                    if k == 2 or k == 3:
                        new_grid[i][j] = 1
                    else:
                        new_grid[i][j] = 0
        return new_grid


if __name__ == '__main__':
    from pprint import pprint as pp
    game = GameOfLife(320, 240, 20)
    game.grid = game.create_grid(randomize=True)
    game.run()