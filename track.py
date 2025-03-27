import pygame
from utils import resize_img

class Track():
    def __init__(self, instrument_names, customer):
        self.instruments = []
        self.instrument_names = instrument_names
        self.width = 250
        self.height = 160
        self.spacing = 10
        self.slots_per_line = 4
        self.slots_spacing = 4
        self.slot_size = self.width//self.slots_per_line - self.slots_spacing
        self.slot_padding = 8
        self.sending = False
        self.send_time = 0
        self.time_to_send = 3

        icon_size = self.width//self.slots_per_line - self.slot_padding*2

        self.customer_img = resize_img(pygame.image.load(f"assets/images/customers/{customer}.png"), 75)
        self.instruments_icons = [resize_img(pygame.image.load(f"assets/images/instruments/{instrument}.png"), icon_size, icon_size) for instrument in instrument_names]
    
    def add(self, instrument):
        self.instruments.append(instrument)
    
    def send(self, now):
        self.sending = True
        self.send_time = now
    
    def is_sent(self, now):
        return self.sending and now-self.send_time > self.time_to_send

    def draw(self, screen, idx, selected, now):
        x = 100 + (self.width + self.spacing)*idx
        if selected:
            pygame.draw.rect(screen, (0, 0, 0), (x - 8, self.spacing - 8, self.width + 16, self.height + 16))
        pygame.draw.rect(screen, (255, 255, 255), (x, self.spacing, self.width, self.height))
        pygame.draw.rect(screen, (180, 180, 180), (x, self.spacing, self.width, self.height//3))
        
        if self.sending:
            time_elapsed = now-self.send_time
            pygame.draw.rect(screen, (255, 0, 86), (x, self.spacing, self.width * time_elapsed/self.time_to_send, self.height//3))
        
        screen.blit(self.customer_img, (x + self.width//2 - self.customer_img.get_width()//2, self.spacing + (self.height - self.customer_img.get_height())//2))
        
        # Icones des instruments
        for i, instrument in enumerate(self.instruments):
            icon_x = x + (self.slot_size + self.slots_spacing)*i
            icon_y = self.spacing*2 + self.height

            if i > self.slots_per_line - 1:
                icon_x = x + (self.slot_size + self.slots_spacing)*(i - self.slots_per_line)
                icon_y += self.slots_spacing + self.slot_size

            pygame.draw.rect(screen, (180, 180, 180), (icon_x, icon_y, self.slot_size, self.slot_size)) # Bordure grise
            pygame.draw.rect(screen, (255, 255, 255), (icon_x + 4, icon_y + 4, self.slot_size - 8, self.slot_size - 8)) # Fond blanc
            screen.blit(self.instruments_icons[self.instrument_names.index(instrument)], (icon_x + self.slot_padding//2, icon_y + self.slot_padding//2)) # Icone