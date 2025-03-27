import pygame
import random

from utils import resize_img
from player import Player
from track import Track
from customer import Customer
from font import Font
from track import Track
from instrument import Instrument
from instruments.guitar import Guitar
from instruments.drums import Drums
from instruments.piano import Piano
from mainmenu import MainMenu

class Game:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.now = 0
        self.FPS = 30
        self.running = True
        self.score = 0

        self.playing = False
        self.menu = MainMenu()
        
        self.font = Font('assets/images/font', 60)
        
        # Charger le fond
        self.background = resize_img(pygame.image.load("assets/images/studio.png"), width=screen.get_width())
        
        # Objet joueur
        self.player = Player(280, 600, self.screen.get_width(), self.screen.get_height())

        self.instrument_names = ["guitar", "bass", "drums", "piano"]

        self.instruments = [
            Guitar(374, 772),
            Instrument("bass", 805, 375),
            Drums(727, 750),
            Piano(479, 440),
        ]

        self.computer = Instrument("computer", 1191, 374)

        # Collision
        self.collisions = [
            pygame.Rect(140, 430, 20, 560),
            pygame.Rect(1400, 430, 20, 560),
            pygame.Rect(140, 430, 1280, 20),
            pygame.Rect(140, 955, 1280, 20)
        ]

        # Pistes
        self.tracks = []
        self.selected_track = 0
        self.max_instruments_per_track = 8

        # Clients
        self.customer_names = ["tyler", "drake", "cardib", "travis", "lilwayne", "jcole", "eminem", "xxxtentacion"]
        self.customers = []
        self.max_customers = 7
        self.customers_pos = [300+100*i for i in range(self.max_customers)]
        self.free_customers_pos = [True]*self.max_customers
        self.last_customer = 0
        self.next_customer_interval = 5

        # Music
        pygame.mixer.music.load('assets/sound/soundtrack.mp3')
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

    def handling_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.player.dir = 'left'
                elif event.key == pygame.K_d:
                    self.player.dir = 'right'
                elif event.key == pygame.K_SPACE:
                    for instrument in self.instruments:
                        if self.player.rect.colliderect(instrument.rect):
                            instrument.play()
                
                elif event.key == pygame.K_c: # TESTING
                    self.spawn_customer()

                # Instrument input
                for instrument in self.instruments:
                    if instrument.playing:
                        add = instrument.handle_input(event.key)
                        if add and len(self.tracks) and len(self.tracks[self.selected_track].instruments) < self.max_instruments_per_track:
                            self.tracks[self.selected_track].add(instrument.name)
                        break

                # Computer input
                if self.player.rect.colliderect(self.computer.rect):
                    if event.key == pygame.K_RIGHT:
                        self.selected_track += 1
                        if self.selected_track >= len(self.tracks):
                            self.selected_track = 0
                    elif event.key == pygame.K_LEFT:
                        self.selected_track -= 1
                        if self.selected_track < 0:
                            self.selected_track = len(self.tracks) - 1
                    elif event.key == pygame.K_RETURN:
                        if len(self.tracks) and not self.tracks[self.selected_track].sending:
                            self.tracks[self.selected_track].send(self.now)

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.vel[1] = -1
        elif keys[pygame.K_s]:
            self.player.vel[1] = 1
        else:
            self.player.vel[1] = 0

        if keys[pygame.K_a]:
            self.player.vel[0] = -1
        elif keys[pygame.K_d]:
            self.player.vel[0] = 1
        else:
            self.player.vel[0] = 0
    
    def remove_customer(self, idx):
        self.free_customers_pos[self.customers_pos.index(self.customers[idx].rect.y)] = True
        self.customers.pop(idx)
        self.tracks.pop(idx)
        
        if self.selected_track >= idx:
            self.selected_track -= 1
            if self.selected_track < 0:
                self.selected_track = 0

    def update(self):
        if not self.playing:
            self.menu.update()
            return

        self.player.update(self.dt, self.collisions)
        
        for instrument in self.instruments:
            instrument.update(self.now, self.dt, self.player)
        
        self.computer.update(self.now, self.dt, self.player)

        despawn_idx = -1
        for i, track in enumerate(self.tracks):
            if track.is_sent(self.now):
                despawn_idx = i
        
        if despawn_idx != -1:
            # Vérifier si la piste est la bonne
            if self.customers[despawn_idx].is_right_track(self.tracks[despawn_idx].instruments):
                self.score += self.customers[despawn_idx].points
            self.remove_customer(despawn_idx)
            

        despawn_idx = -1
        for i, customer in enumerate(self.customers):
            if customer.update(self.now):
                despawn_idx = i
        
        if despawn_idx != -1:
            self.remove_customer(despawn_idx)
        
        if self.now - self.last_customer >= self.next_customer_interval:
            self.spawn_customer()
            self.last_customer = self.now
            self.next_customer_interval = random.randint(15, 30)
        
    def display(self):
        if not self.playing:
            self.menu.draw_menu(self.screen)
            self.menu.draw_buttons(self.screen)
            pygame.display.flip()
            return
        
        # Dessiner l'image de fond
        self.screen.blit(self.background, (0, 0))

        # Dessiner les instruments
        for instrument in self.instruments:
            instrument.draw(self.screen, self.player)
        
        self.computer.draw(self.screen, self.player)

        # Dessiner le joueur
        self.player.draw(self.screen)

        # Dessiner les clients
        for customer in self.customers:
            customer.draw(self.screen, self.now)

        # Dessiner l'interface
        for i, track in enumerate(self.tracks):
            track.draw(self.screen, i, i == self.selected_track, self.now)
            
        self.font.display(screen, str(self.score), 100, 1000, 2)

        # for rect in self.collisions:
        #     pygame.draw.rect(self.screen, (255, 0, 0), rect)

        # Mettre à jour l'écran
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.now = pygame.time.get_ticks() / 1000
            self.handling_events()
            self.update()
            self.display()
            self.dt = self.clock.tick(self.FPS) / 1000
    
    def spawn_customer(self):
        if len(self.customers) > self.max_customers:
            return
        
        name = random.choice(self.customer_names)
        while name in [customer.name for customer in self.customers]:
            name = random.choice(self.customer_names)
        
        pos = self.free_customers_pos.index(True)
        self.free_customers_pos[pos] = False
        self.customers.append(Customer(name, self.instrument_names, 1430, self.customers_pos[pos], self.now))
        self.tracks.append(Track(self.instrument_names, name))

pygame.init()
screen = pygame.display.set_mode((1920, 1080), pygame.SCALED | pygame.FULLSCREEN)

pygame.display.set_caption("Studio Rush")

game = Game(screen)
game.run()

pygame.quit()