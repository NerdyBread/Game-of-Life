import pygame

class Button:
    def __init__(self, game, text, color, text_color, width, height, font_size, x, y):
        self.game = game
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        
        # Set properties
        self.width, self.height = width, height
        self.x, self.y = x, y
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.SysFont(None, font_size)
        
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        self._prep_text(text)
        
    def _prep_text(self, text):
        self.text_image = self.font.render(text, True, self.text_color, self.color)
        self.text_image_rect = self.text_image.get_rect()
        self.text_image_rect.center = self.rect.center
        
    def draw(self):
        self.screen.fill(self.color, self.rect)
        self.screen.blit(self.text_image, self.text_image_rect)
        
    def set_x(self, x):
        self.x = x
        
    def set_y(self, y):
        self.y = y