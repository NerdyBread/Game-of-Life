import sys

import pygame

from cell import Cell
from settings import Settings

class GameOfLife:
    def __init__(self, n):
        self.n = n
        self.settings = Settings()
        self._generate_grid()
        self.neighbor_coords = [(-1, -1), (-1, 0), (-1, 1),
                                (0, -1), (0, 1),
                                (1, -1), (1, 0), (1, 1)]
        
        self.init_pygame()
        
    def init_pygame(self):
        """Initial pygame settings"""
        pygame.init()
        
        self.screen = pygame.display.set_mode((self.settings.screenX, self.settings.screenY))
        pygame.display.set_caption(self.settings.caption)
        
    def get_cell(self, x, y):
        """Return a cell object given x and y coordinates"""
        return self.grid[y][x]
    
    def _generate_grid(self):
        """Generate a grid of cells (all initially dead)"""
        self.grid = []
        for i in range(self.n):
            new_row = []
            for j in range(self.n):
                new_row.append(Cell(self))
            self.grid.append(new_row)
    
    def _get_cell_neighbors(self, x, y) -> int:
        """Returns number of living neighbors given a cell's x and y"""
        living_neighbors = 0
        for pair in self.neighbor_coords:
            if 0 <= (x + pair[0]) < self.n and 0 <= y+pair[1] < self.n:
                neighbor = self.grid[y+pair[1]][x+pair[0]]
                neighbor_current_state = neighbor.is_alive()
                living_neighbors += neighbor_current_state
        return living_neighbors
    
    def set_next_frame_states(self):
        """Updates first bit of each cell according to what state it should be next frame"""
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                neighbor_count = self._get_cell_neighbors(x, y)
                if cell.is_dead() and neighbor_count == 3:
                    cell.set_alive()
                if cell.is_alive():
                    if neighbor_count not in (2, 3):
                        cell.set_dead()
                    else:
                        # Keep cells alive next frame if they hit neighbor requirement
                        cell.set_alive()
    
    def update_cells(self):
        """Finish the two-pass cell update cycle"""
        for row in self.grid:
            for cell in row:
                cell.next_frame()
                
    def show_grid(self):
        """Command line display of game output"""
        for row in self.grid:
            row_text = ""
            for cell in row:
                row_text += str(int(cell.is_alive()))
            print(row_text)
        print("--------------")
            
    def switch_cell(self, x, y):
        cell = self.grid[y][x]
        cell.switch()
        
    def _check_events(self):
        """Pygame events like mouse clicks and such"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                    
    def _update_screen(self):
        """Update graphics and flip screen each frame"""
        self.screen.fill(self.settings.bg_color)        
            
        pygame.display.flip()
            
    def main(self):
        """Main game loop"""
        print("The Game of Life")
        # Initial game state
        self.switch_cell(1, 0)
        self.switch_cell(2, 1)
        self.switch_cell(0, 2)
        self.switch_cell(1, 2)
        self.switch_cell(2, 2)
        
        self.switch_cell(4, 4)
        self.switch_cell(4, 5)
        self.switch_cell(5, 4)
        self.switch_cell(5, 5)
        while True:
            self.set_next_frame_states()
            self.update_cells()
            
            self._check_events()
            self._update_screen()
            # Any user cell updates
            # self.show_grid()
        
if __name__ == "__main__":
    test = GameOfLife(15)
    test.main()