import curses

from life import GameOfLife
from ui import UI

from time import sleep

import argparse

parser = argparse.ArgumentParser(description='data')
parser.add_argument('-rows', '--rows', type=int, help='rows of data')
parser.add_argument('-cols', '--cols', type=int, help='cols of data')
parser.add_argument('-max-generations', '--maxgenerations', type=int, help='max-generations of data')
agrs = parser.parse_args()

class Console(UI):


    def __init__(self, life: GameOfLife) -> None:
        
        super().__init__(life)


    def draw_borders(self, screen) -> None:
        r = self.life.rows 
        c = self.life.cols 
        self.screen = curses.newwin(c + 1, r + 1, 0, 0)
        self.screen.border('|', '|', '-', '-', '+', '+', '+', '+')
        self.screen.refresh()
        pass


    def draw_grid(self, screen) -> None:
        
        for i in range(1,self.life.rows):
            for j in range(1,self.life.cols):
                if self.life.curr_generation[i][j] == 1:
                    self.screen.addch(j , i , "*")
                else:
                    self.screen.addstr(j , i , " ")
        self.screen.refresh()
                    

    def run(self) -> None:
        
        self.screen = curses.initscr()
        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(True)
        while True:
            self.screen.erase()
            self.draw_borders(self.screen)
            self.draw_grid(self.screen)
            sleep(1)
            self.life.step()
            
        curses.echo()
        curses.nocbreak()
        self.screen.keypad(False)
        curses.endwin()


'''
if __name__ == "__main__":
    life = GameOfLife((agrs.rows, agrs.cols), agrs.maxgenerations)
    ui = Console(life)
    ui.run()

'''
life = GameOfLife((15,10), max_generations=50)
ui = Console(life)
ui.run()
