class Settings:
    """Store all pygame settings"""
    def __init__(self, n):
        self.screenX = 750
        self.screenY = 750
        self.caption = "Game of Life by NerdyBread"
        self.bg_color = (255, 255, 255)
        self.rows = n # Number of cells in each row and column
        
        # Cell properties
        self.alive_color = (64, 0, 128)
        self.dead_color = (87, 81, 81)
        self.cell_length = self.screenX / self.rows
        self.border_width = 3
        
        # Game settings
        self.paused = True
        self.frame_time = 500 # milliseconds
        
        # Button properties
        self.button_text_color = (0, 0, 0)
        self.play_button_color = (16, 237, 16)
        self.pause_button_color = (255, 0, 0)
        
    def is_paused(self):
        return self.paused