class Settings:
    """Store all pygame settings"""
    def __init__(self):
        self.screenX = 800
        self.screenY = 800
        self.caption = "Game of Life by NerdyBread"
        self.bg_color = (242, 179, 255)
        self.rows = 15 # Number of cells in each row and column
        
        # Cell properties
        self.alive_color = (64, 0, 128)
        self.dead_color = (156, 153, 176)
        self.cell_length = self.screenX / self.rows