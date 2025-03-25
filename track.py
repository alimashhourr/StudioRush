import pygame
from utils import resize_img

class Track():
    def __init__(self, instrument_names, customer):
        self.instruments = []
        self.instrument_names = instrument_names
        self.width = 200
        self.height = 100
        self.spacing = 5
        self.instrument_slot_size = self.width//4 - self.spacing
        self.instrument_slot_margin = 8

        icon_size = self.width//4 - self.instrument_slot_margin*2

        self.customer_img = resize_img(pygame.image.load(f"assets/images/customers/{customer}.png"), self.height//2)
        self.instruments_icons = [resize_img(pygame.image.load(f"assets/images/instruments/{instrument}.png"), icon_size, icon_size) for instrument in instrument_names]
    
    def add(self, instrument):
        self.instruments.append(instrument)

    def draw(self, screen, idx):
        x = 350 + (self.width + self.spacing)*idx
        pygame.draw.rect(screen, (255, 255, 255), (x, self.spacing, self.width, self.height))
        pygame.draw.rect(screen, (180, 180, 180), (x, self.spacing, self.width, self.height//3))
        
        screen.blit(self.customer_img, (x + self.width//2 - self.customer_img.get_width()//2, self.spacing + (self.height - self.customer_img.get_height())//2))

        # Icones des instruments
        for i, instrument in enumerate(self.instruments):
            icon_x = x + (self.instrument_slot_size + self.spacing)*i
            icon_y = self.spacing*2 + self.height
            pygame.draw.rect(screen, (180, 180, 180), (icon_x, icon_y, self.instrument_slot_size, self.instrument_slot_size)) # Bordure grise
            pygame.draw.rect(screen, (255, 255, 255), (icon_x + 4, icon_y + 4, self.instrument_slot_size - 8, self.instrument_slot_size - 8)) # Fond blanc
            screen.blit(self.instruments_icons[self.instrument_names.index(instrument)], (icon_x + self.instrument_slot_margin//2, icon_y + self.instrument_slot_margin//2)) # Icone