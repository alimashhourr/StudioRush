import pygame
from utils import resize_img

class Guitar():
    def __init__(self, x, y, size):
        self.img = resize_img(pygame.image.load("assets/images/instruments/guitar.png"), width=size)
        self.rect = self.img.get_rect(x=x, y=y)

    def update(self):
        pass
    
    def draw(self, screen):
        pass