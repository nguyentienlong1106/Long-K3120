import pathlib
import random
import pygame
from pygame.locals import *
from typing import List, Optional, Tuple


Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:
    
    def __init__(
        self,
        size: Tuple[int, int],
        randomize: bool=True,
        max_generations: Optional[float]=float('inf')
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool=False) -> Grid:
        # Copy from previous assignment
        Grid=[]
        for _ in range(self.rows):
            onerow=[]
            for _ in range(self.cols):
                if randomize:
                    onerow.append(random.randint(0,1))
                else:
                    onerow.append(0)
            Grid.append(onerow)
        
        return Grid
        pass

    def get_neighbours(self, cell: Cell) -> Cells:
        # Copy from previous assignment
        Cells=[]
        x,y = cell
        for i in range(x-1,x+2):
            if (i in range(self.rows)):
                for j in range(y-1,y+2):
                    if  (j in range(self.cols)):
                        if [i,j] != [x,y]:
                            Cells.append(self.curr_generation[i][j])
        return Cells
        pass

    def get_next_generation(self) -> Grid:
        # Copy from previous assignment
        Grid = self.create_grid()
        for i in range(self.rows):
            for j in range(self.cols):
                if self.curr_generation[i][j] == 1:
                    if sum(self.get_neighbours((i,j))) == 3 or sum(self.get_neighbours((i,j))) == 2:
                        Grid[i][j] = 1
                    else:
                        Grid[i][j] = 0
                elif self.curr_generation[i][j] == 0:
                    if sum(self.get_neighbours((i,j))) == 3:
                        Grid[i][j] = 1
                    else:
                        Grid[i][j] = 0
        self.curr_generation = Grid
        return self.curr_generation
        pass

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation.copy()
        self.curr_generation = self.get_next_generation()
        self.generations += 1
        
        pass

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        
        return self.generations <= self.max_generations
        pass

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.prev_generation != self.curr_generation
            
        pass

    @staticmethod
    def from_file(self, filename: pathlib.Path) -> 'GameOfLife':
        """
        Прочитать состояние клеток из указанного файла.
        """
        file = open(filename)
        grid = file.readlines()
        for i in range(len(grid)):
            grid[i] = list(map(int, grid[i][0:len(grid[i])-2 ]))
            self.curr_generation = grid
            life = GameOfLife((len(grid[0]), len(grid)))
            file.close()
            return life
        pass

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        file = open(filename, 'w')
        for i in range(len(self.curr_generation)):
            file.write(str(self.curr_generation[i]) + "/n")
        file.close()
        pass