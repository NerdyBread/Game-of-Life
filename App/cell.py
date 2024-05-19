import pygame
class Cell:
    def __init__(self, game, x, y):
        """First bit of state represents current state, second stores next frame value"""
        self.game = game # Connection to main game class
        self.state = 0b00
        self.kill_mask = 0b01
        self.alive_mask = 0b10
        
        # Graphical stuff
        self.settings = game.settings
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        
        self.length = game.settings.cell_length
        self.x = self.length * x
        self.y = self.length * y
        self.border_width = self.game.settings.border_width
        self.border_color = (0, 0, 0)
        
        
    def is_dead(self):
        """Cell is dead this frame"""
        return not self.state % 2
    
    def is_alive(self):
        """Cell is alive this frame"""
        return self.state % 2
    
    def set_dead(self):
        """Bitwise and to set next state to dead and preserve current state"""
        self.state &= self.kill_mask
        
    def set_alive(self):
        """Bitwise or to set next state to alive and preserve current state"""
        self.state |= self.alive_mask
        
    def switch(self):
        """User updates cell state in current frame"""
        self.state = ~self.state
        
    def next_frame(self):
        """Shift next frame bit to current state bit"""
        self.state = self.state >> 1
        
    def draw(self):
        if self.is_alive():
            color = self.settings.alive_color
        else:
            color = self.settings.dead_color
        pygame.draw.rect(self.screen, color, (self.x, self. y, self.length, self.length))

        # Black border around the cell
        pygame.draw.rect(self.screen, self.border_color, (self.x - self.border_width, self.y - self.border_width, 
                                     self.length + 2 * self.border_width, 
                                     self.length + 2 * self.border_width), self.border_width)
        
"""def show(cell):
    print(bin(cell.state))

if __name__ == "__main__":
    dead_cell = Cell("Hello")
    dead_cell.set_alive()
    show(dead_cell)
    print(dead_cell.is_alive())
    print(dead_cell.is_dead())
    dead_cell.next_frame()
    show(dead_cell)
    print(dead_cell.is_alive())
    print(dead_cell.is_dead())"""
    