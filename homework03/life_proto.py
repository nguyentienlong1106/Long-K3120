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
        
        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size
        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        # Создание списка клеток
        # PUT YOUR CODE HERE
        self.grid=self.create_grid(randomize=True)
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.grid=self.create_grid()
            
            self.draw_grid() 
            self.draw_lines()
            
            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            # PUT YOUR CODE HERE
            self.grid = self.get_next_generation()
                              
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool=True) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        
        Grid=[]
        for _ in range(self.cell_height):
            onerow=[]
            for _ in range(self.cell_width):
                if randomize:
                    onerow.append(random.randint(0,1))
                else:
                    onerow.append(0)
            Grid.append(onerow)
        
        return Grid
        

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                if self.grid[i][j] == 1:
                    color = pygame.Color('green')
                else:
                    color = pygame.Color('white')
                pygame.draw.rect(self.screen,color,(j*self.cell_size,i*self.cell_size,self.cell_size,self.cell_size))
        
        pass

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        Cells=[]
        x,y = cell
        for i in range(x-1,x+2):
            if i in range(self.cell_height):
                for j in range(y-1,y+2):
                    if j in range(self.cell_width):
                        if [i,j] != [x,y]:
                            Cells.append(self.grid[i][j])
        return Cells


    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        Grid = self.create_grid()
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                if self.grid[i][j] == 1:
                    if sum(self.get_neighbours((i,j))) == 3 or sum(self.get_neighbours((i,j))) == 2:
                        Grid[i][j] = 1
                    else:
                        Grid[i][j] = 0
                elif self.grid[i][j] == 0:
                    if sum(self.get_neighbours((i,j))) == 3:
                        Grid[i][j] = 1
                    else:
                        Grid[i][j] = 0
        return Grid


if __name__ == '__main__':
    game = GameOfLife(320, 240, 20,5)
    game.grid = game.create_grid(randomize=True)
    game.run()