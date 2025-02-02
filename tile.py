import pygame
from utils import resize_img

class Tile():
    def __init__(self, x, y, size):
        self.img = resize_img(pygame.image.load(f"assets/images/tiles/wall.png"), width=size)
        self.rect = self.img.get_rect(x=x*size, y=y*size)

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.img, self.rect)