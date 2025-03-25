import pygame
from os import listdir
from utils import resize_img

class Font:
    def __init__(self, dir, size):
        self.font = {}
        for file_name in listdir(dir):
            char = file_name[0]
            img = pygame.image.load(dir + '/' + file_name)
            img = resize_img(img, height=size)
            self.font[char] = img
    
    def display(self, screen, text, x, y, spacing):
        new_x = x
        for char in text:
            img = self.font[char]
            screen.blit(img, (new_x, y))
            new_x += img.get_width() + spacing