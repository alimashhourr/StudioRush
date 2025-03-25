import pygame
from utils import resize_img

class Instrument():
    def __init__(self, name, x, y):
        self.name = name
        self.img = pygame.image.load(f"assets/images/instruments/{name}.png")
        self.img_hover = pygame.image.load(f"assets/images/instruments/{name}_hover.png")
        self.rect = self.img.get_rect(x=x, y=y)
        self.playing = False

    def update(self, now, dt, player):
        if not self.rect.colliderect(player.rect):
            self.playing = False

    def draw(self, screen, player):
        if self.rect.colliderect(player.rect):
            screen.blit(self.img_hover, self.rect)
        else:
            screen.blit(self.img, self.rect)

    def play(self):
        self.playing = True
    
    def handle_input(self, event): # returns True when game is won, to add instrument to track
        pass  # To be implemented in subclasses