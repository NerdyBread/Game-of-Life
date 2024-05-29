import sys

import pygame

from button import Button
from cell import Cell
from settings import Settings

class GameOfLife:
    def __init__(self, n):
        self.n = n
        self.settings = Settings(n)
        self.init_pygame()
        self._generate_grid()
        self.neighbor_coords = [(-1, -1), (-1, 0), (-1, 1),
                                (0, -1), (0, 1),
                                (1, -1), (1, 0), (1, 1)]
        self._init_buttons()
        
    def init_pygame(self):
        """Initial pygame settings"""
        pygame.init()
        
        self.screen = pygame.display.set_mode((self.settings.screenX, self.settings.screenY+50))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption(self.settings.caption)
        
    def _init_buttons(self):
        """Create all buttons in bottom toolbar"""
        button_text_color_dark = self.settings.button_text_color_dark
        play_button_color = self.settings.play_button_color
        pause_button_color = self.settings.pause_button_color
        button_width = 60
        button_height = 20
        button_font_size = 20
        
        button_x = (self.screen_rect.width / 2) - (button_width / 2)
        button_y = self.screen_rect.height - button_height - 5 # The extra 5px adds a little border at the bottom
        
        self.play_button = Button(self, "Play", play_button_color, button_text_color_dark, button_width,
                                  button_height, button_font_size, button_x, button_y)
        self.pause_button = Button(self, "Pause", pause_button_color, button_text_color_dark, button_width,
                                   button_height, button_font_size, button_x, button_y)
        
        # Create pause buttons
        button_border = 20
        button_distance = button_width + button_border
        
        button_x += button_distance
        clear_button_color = self.settings.clear_button_color
        button_text_color_light = self.settings.button_text_color_light
        
        self.clear_button = Button(self, "Clear", clear_button_color, button_text_color_light, button_width,
                                   button_height, button_font_size, button_x, button_y)
        
        # Speed up and slow down buttons
        button_x += button_distance
        
        slow_button_color = self.settings.slow_button_color
        speed_button_color = self.settings.speed_button_color
        
        self.slow_down_button = Button(self, "Slow Down", slow_button_color, button_text_color_dark, button_width,
                                       button_height, button_font_size, button_x, button_y)
        
    def _get_cell(self, x, y):
        """Return a cell object given x and y coordinates"""
        return self.grid[y][x]
    
    def _generate_grid(self):
        """Generate a grid of cells (all initially dead)"""
        self.grid = []
        for y in range(self.n):
            new_row = []
            for x in range(self.n):
                new_row.append(Cell(self, x, y))
            self.grid.append(new_row)
    
    def _get_cell_neighbors(self, x, y) -> int:
        """Returns number of living neighbors given a cell's x and y"""
        living_neighbors = 0
        for pair in self.neighbor_coords:
            if 0 <= (x + pair[0]) < self.n and 0 <= (y+pair[1]) < self.n:
                neighbor = self.grid[y+pair[1]][x+pair[0]]
                neighbor_current_state = neighbor.is_alive()
                living_neighbors += neighbor_current_state
        return living_neighbors
    
    def set_next_frame_states(self):
        """Updates first bit of each cell according to what state it should be next frame"""
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                neighbor_count = self._get_cell_neighbors(x, y)
                # Underlying cell life/death logic
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
                cell.next_frame() # Shifts the next frame bit to current frame
            
    def _switch_cell(self, x, y):
        cell = self.grid[y][x]
        cell.switch()
        
    def _check_events(self):
        """Pygame events like mouse clicks and such"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.settings.is_paused():
                    self._check_play_button(mouse_pos)
                else:
                    self._check_pause_button(mouse_pos)
                self._check_clear_button(mouse_pos)
                self._check_cell_clicked(mouse_pos)
                
    def _check_play_button(self, mouse_pos):
        """Check if play button was clicked"""
        if self.play_button.rect.collidepoint(mouse_pos):
            self.settings.paused = False

    def _check_pause_button(self, mouse_pos):
        """Check if pause button was clicked"""
        if self.pause_button.rect.collidepoint(mouse_pos):
            self.settings.paused = True
            
    def clear_screen(self):
        """Tied to clear button"""
        for row in self.grid:
            for cell in row:
                if cell.is_alive():
                    cell.switch()
            
    def _check_clear_button(self, mouse_pos):
        if self.clear_button.rect.collidepoint(mouse_pos):
            self.clear_screen()
        
    def _check_cell_clicked(self, mouse_pos):
        """Check which cell was clicked"""
        # Heuristic approach to narrow down cell click checking
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        # Map the mouse coordinates to an approximate cell range
        cell_len = self.settings.cell_length
        approx_x = int(mouse_x // cell_len)
        approx_y = int(mouse_y // cell_len)
        # These are right with a margin of error of one cell
        for row in range(approx_y-1, approx_y+2):
            for index in range(approx_x-1, approx_x+2):
                if 0 <= index < self.n and 0 <= row < self.n:
                    cell = self.grid[row][index]
                    if cell.rect.collidepoint(mouse_pos):
                        cell.switch()
                        return None # Break out of both loops
                    
    def _update_screen(self):
        """Update graphics and flip screen each frame"""
        self.screen.fill(self.settings.dead_color)
        for row in self.grid:
            for cell in row:
                cell.draw()
                
        self._manage_buttons()
            
        pygame.display.flip()
        
    def _manage_buttons(self):
        if self.settings.is_paused():
            self.play_button.draw()
        else:
            self.pause_button.draw()
        self.clear_button.draw()
            
    def main(self):
        """Main game loop"""
        # Initial game state
        self._switch_cell(22, 22)
        self._switch_cell(23, 22)
        self._switch_cell(22, 23)
        self._switch_cell(23, 23)
        self._update_screen()
        
        while True:
            self._check_events()
            # Frontend
            self._update_screen()
            if not self.settings.is_paused():
                # Backend
                self.set_next_frame_states()
                self.update_cells()
                pygame.time.delay(self.settings.frame_time)
                
        
if __name__ == "__main__":
    test = GameOfLife(48)
    test.main()