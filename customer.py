import pygame
import random
from utils import resize_img
from random import randint

class Customer:
    def __init__(self, name, instrument_names, x, y):
        self.name = name
        self.instrument_names = instrument_names
        self.track = self.generate_track(instrument_names.copy())
        self.time = len(self.track)*30 + 30
        self.points = len(self.track)*10

        self.img = resize_img(pygame.image.load(f"assets/images/customers/{name}.png"), height=80)
        self.rect = self.img.get_rect(x=x, y=y)

        self.start_time = 0
        self.timer_bar_height = self.img.get_height()//3
        self.track_height = 2*self.timer_bar_height
        self.icon_spacing = 8
        self.icon_size = self.track_height - self.icon_spacing*2
        self.track_bar_w = len(self.track)*(self.icon_size + self.icon_spacing) + self.icon_spacing

        self.instruments_icons = [resize_img(pygame.image.load(f"assets/images/instruments/{instrument}.png"), self.icon_size, self.icon_size) for instrument in instrument_names]

        # VOITURE
        self.car = resize_img(pygame.image.load(f"assets/images/cars/car{randint(0,6)}.png"), width=80)
        self.car_rect = self.car.get_rect(x=1555, y=1080)
        self.car_arrived = False
        self.car_arrived_time = 0
        self.car_left = False
    
    def generate_track(self, instrument_names):
        track_length = random.choices([1, 2, 3, 4, 5, 6, 7, 8], weights=[0.1, 0.2, 0.3, 0.2, 0.05, 0.05, 0.05, 0.05], k=1)[0]
        track = random.choices(instrument_names, k=track_length)
        
        # Trier la piste en regroupant les instruments
        random.shuffle(instrument_names)
        instruments_count = {}
        for instrument in instrument_names:
            instruments_count[instrument] = 0
        for instrument in track:
            instruments_count[instrument] += 1
        sorted_track = []
        for instrument in instruments_count.keys():
            for i in range(instruments_count[instrument]):
                sorted_track.append(instrument)
            
        return sorted_track
        
    def update(self, now, dt):
        # Déplacer la voiture
        if not self.car_left:
            if self.car_arrived:
                if now - self.car_arrived_time >= 1:
                    self.car_rect.y -= 600 * dt
                    if self.car_rect.y <= -self.car_rect.height:
                        self.car_left = True
            else:
                self.car_rect.y -= 600 * dt
                if self.car_rect.y <= self.rect.y:
                    self.car_arrived = True
                    self.car_arrived_time = now
                    self.start_time = now

        if self.car_arrived:
            time_left = self.time - (now - self.start_time)
            if time_left <= 0:
                return True
        return False

    def is_right_track(self, sent_track):
        sent_instruments_count = {}
        my_instruments_count = {}
        for instrument in self.instrument_names:
            sent_instruments_count[instrument] = 0
            my_instruments_count[instrument] = 0
        
        for instrument in sent_track:
            sent_instruments_count[instrument] += 1
        
        for instrument in self.track:
            my_instruments_count[instrument] += 1
        
        return sent_instruments_count == my_instruments_count
            

    def draw(self, screen, now):
        # Dessiner la voiture
        if not self.car_left:
            screen.blit(self.car, self.car_rect)
        
        if not self.car_arrived:
            return

        screen.blit(self.img, self.rect)
        x = self.rect.x + 80
        pygame.draw.rect(screen, (180, 180, 180), (x, self.rect.y, self.track_bar_w, self.track_height + self.timer_bar_height)) # Fond gris
        pygame.draw.rect(screen, (255, 255, 255), (x + 4, self.rect.y + 4, self.track_bar_w - 8, self.track_height - 8)) # Fond blanc pour les instruments

        # Dessiner les instruments de la commande
        for i, instrument in enumerate(self.track):
            screen.blit(self.instruments_icons[self.instrument_names.index(instrument)], (x + self.icon_spacing + i*(self.icon_size + self.icon_spacing), self.rect.y + self.icon_spacing))

        # Dessiner la barre de temps
        time_left = self.time - (now - self.start_time)

        # Faire un dégradé du vert au rouge en fonction du temps restant
        color = (0, 255, 0)
        if time_left/self.time <= 0.5:
            color = (255, 200, 0)
        if time_left/self.time <= 0.3:
            color = (255, 0, 0)

        pygame.draw.rect(screen, color, (x + 4, self.rect.y + self.track_height + 4, (self.track_bar_w - 8)*time_left/self.time, self.timer_bar_height - 8))