import pygame

class Instrument():
    def __init__(self, name, x, y):
        self.name = name
        self.img = pygame.image.load(f"assets/images/instruments/{name}.png")
        self.rect = self.img.get_rect(x=x, y=y)

        self.img_highlight = self.img.copy()
        self.img_highlight.fill((100, 100, 100, 50), special_flags=pygame.BLEND_RGBA_ADD)

    def update(self):
        pass
    
    def draw(self, screen):
        screen.blit(self.img, self.rect)