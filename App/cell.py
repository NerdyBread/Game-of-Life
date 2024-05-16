class Cell:
    def __init__(self, game):
        """First bit of state represents current state, second stores next frame value"""
        self.game = game # Connection to main game class
        self.state = 0b00
        self.kill_mask = 0b01
        self.alive_mask = 0b10
        self.dead_cells = (0b00, 0b10)
        self.living_cells = (0b01, 0b11)
        
    def is_dead(self):
        return self.state in self.dead_cells
    
    def is_alive(self):
        """Because I'm lazy"""
        return self.state in self.living_cells
    
    def set_dead(self):
        """Bitwise and to set next state to dead and preserve current state"""
        self.state &= self.kill_mask
        
    def set_alive(self):
        """Bitwise or to set next state to alive and preserve current state"""
        self.state |= self.alive_mask
        
    def switch(self):
        self.state = ~self.state
        
    def next_frame(self):
        """Shift next frame bit to current state bit"""
        self.state = self.state >> 1
        
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
    