import pygame
import random

from utils import resize_img
from player import Player
from track import Track
from customer import Customer
from track import Track
from ui import UserInterface
from mainmenu import MainMenu
from instruments.guitar import Guitar
from instruments.drums import Drums
from instruments.piano import Piano
from instruments.bass import  Bass
from instruments.computer import Computer

class Game:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.now = 0
        self.FPS = 30
        self.running = True

        self.playing = False
        self.score = 0
        self.timer = 0
        self.gameover = False
        self.gameover_time = 0
        
        # Interface
        self.menu = MainMenu()
        self.ui = UserInterface()
        
        # Charger le fond
        self.background = resize_img(pygame.image.load("assets/images/studio.png"), width=screen.get_width())
        
        # Touches
        self.keybinds1 = {
            'left': pygame.K_a,
            'right': pygame.K_d,
            'up': pygame.K_w,
            'down': pygame.K_s,
            'interact': pygame.K_e
        }

        self.keybinds2 = {
            'left': pygame.K_LEFT,
            'right': pygame.K_RIGHT,
            'up': pygame.K_UP,
            'down': pygame.K_DOWN,
            'interact': pygame.K_SPACE
        }

        # Joueurs
        self.players = []

        # Instruments
        self.instrument_names = ["guitar", "bass", "drums", "piano"]
        self.instruments = [
            Guitar(374, 772),
            Bass(805, 375),
            Drums(727, 750),
            Piano(479, 440),
            Computer(1191, 374)
        ]

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
        self.customer_names = ["tyler", "drake", "cardib", "travis", "lilwayne", "jcole", "eminem", "xxxtentacion", "2pac", "50cent", "bigpun", "bluerag", "e40", "future", "macmiller", "nicki", "pharrell", "raekwon", "rickross"]
        self.customers = []
        self.max_customers = 7
        self.customers_pos = [300+100*i for i in range(self.max_customers)]
        self.free_customers_pos = [True]*self.max_customers
        self.last_customer = 0
        self.next_customer_interval = 0
        self.served_clients = 0

        # Musique
        pygame.mixer.music.load('assets/sound/soundtrack.mp3')
        pygame.mixer.music.set_volume(0.15)
        pygame.mixer.music.play(-1)

        # Sons
        self.sounds = {
            "points": pygame.mixer.Sound("assets/sound/cash.mp3"),
            "fail": pygame.mixer.Sound("assets/sound/fail.mp3"),
            "10s": pygame.mixer.Sound("assets/sound/clock_ticking_10s.mp3"),
            "gameover": pygame.mixer.Sound("assets/sound/gong.mp3")
        }
        self.played_ticking = False

        self.sounds["points"].set_volume(3)
        self.sounds["fail"].set_volume(0.5)
    
    def start_game(self, players, game_type):
        self.score = 0
        self.served_clients = 0
        self.tracks = []
        self.selected_track = 0
        self.customers = []
        self.free_customers_pos = [True]*self.max_customers
        self.last_customer = self.now
        self.next_customer_interval = 3
        self.played_ticking = False
        
        if game_type == 1:
            self.timer = 60*3 + 1
        else:
            self.timer = 60*6 + 1
        self.playing = True

        if players == 1:
            self.players = [Player(1, 280, 600, self.keybinds1)]
        else:
            self.players = [Player(1, 280, 600, self.keybinds1), Player(2, 360, 600, self.keybinds2)]

    def handling_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if not self.playing:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    start = self.menu.click()
                    if start:
                        self.start_game(self.menu.players, self.menu.game_type)
                return
            
            if self.gameover:
                return
            
            # Touches pour jouer
            if event.type == pygame.KEYDOWN:
                for player in self.players:
                    if event.key == player.keybinds['left'] and not player.playing:
                        player.dir = 'left'
                    elif event.key == player.keybinds['right'] and not player.playing:
                        player.dir = 'right'
                    elif event.key == player.keybinds['interact']:
                        for instrument in self.instruments:
                            if player.rect.colliderect(instrument.rect):
                                if player.playing:
                                    instrument.stop_playing()
                                    player.playing = False
                                elif not instrument.playing:
                                    instrument.play()
                                    player.playing = True

                    # Instrument input
                    for instrument in self.instruments:
                        if instrument.playing:
                            if isinstance(instrument, Computer):
                                instrument.handle_input(event.key, player, self)
                            else:
                                add = instrument.handle_input(event.key, player)
                                if add and len(self.tracks) and len(self.tracks[self.selected_track].instruments) < self.max_instruments_per_track:
                                    self.tracks[self.selected_track].add(instrument.name)
                            break

        # Player movement
        for player in self.players:
            if not player.playing:
                keys = pygame.key.get_pressed()
                if keys[player.keybinds['up']]:
                    player.vel[1] = -1
                elif keys[player.keybinds['down']]:
                    player.vel[1] = 1
                else:
                    player.vel[1] = 0

                if keys[player.keybinds['left']]:
                    player.vel[0] = -1
                elif keys[player.keybinds['right']]:
                    player.vel[0] = 1
                else:
                    player.vel[0] = 0
            else:
                player.vel[0] = 0
                player.vel[1] = 0
    
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
        
        if self.gameover:
            if self.now - self.gameover_time >= 8:
                # Retourner au menu
                self.gameover = False
                self.playing = False
                pygame.mixer.music.play(-1)
            return

        self.timer -= self.dt

        if self.timer <= 10 and not self.played_ticking:
            self.sounds["10s"].play()
            self.played_ticking = True
        if self.timer <= 0:
            self.timer = 0
            self.gameover = True  # Stop
            self.gameover_time = self.now
            pygame.mixer.music.stop()
            self.sounds["gameover"].play()
        
        for player in self.players:
            player.update(self.dt, self.collisions)
        
        for instrument in self.instruments:
            instrument.update(self.now, self.dt)

        despawn_idx = -1
        for i, track in enumerate(self.tracks):
            if track.is_sent(self.now):
                despawn_idx = i
        
        if despawn_idx != -1:
            # Vérifier si la piste est la bonne
            if self.customers[despawn_idx].is_right_track(self.tracks[despawn_idx].instruments):
                self.score += self.customers[despawn_idx].points
                self.served_clients += 1
                self.sounds["points"].play()
            else:
                self.sounds["fail"].play()
            self.remove_customer(despawn_idx)
            

        despawn_idx = -1
        for i, customer in enumerate(self.customers):
            if customer.update(self.now, self.dt):
                despawn_idx = i
        
        if despawn_idx != -1:
            self.remove_customer(despawn_idx)
            self.sounds["fail"].play()
        
        if self.now - self.last_customer >= self.next_customer_interval:
            self.spawn_customer()
            self.last_customer = self.now

            if len(self.players) == 1:
                self.next_customer_interval = random.randint(13, 20)
            else:
                self.next_customer_interval = random.randint(10, 15)
        
    def display(self):
        if not self.playing:
            self.menu.draw_menu(self.screen)
            pygame.display.flip()
            return
        
        # Dessiner l'image de fond
        self.screen.blit(self.background, (0, 0))

        # Dessiner les instruments
        for instrument in self.instruments:
            instrument.draw(self.screen, self.players)

        # Dessiner les joueurs
        for player in self.players:
            player.draw(self.screen)

        # Dessiner les clients
        for customer in self.customers:
            customer.draw(self.screen, self.now)

        # Dessiner l'interface
        for instrument in self.instruments:
            if instrument.playing:
                instrument.draw_interface(self.screen)
                break

        for i, track in enumerate(self.tracks):
            track.draw(self.screen, i, i == self.selected_track, self.now)
        
        self.ui.draw(self.screen, self.score, self.timer, self.gameover, self.served_clients)

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
        if len(self.customers) == self.max_customers:
            return
        
        name = random.choice(self.customer_names)
        while name in [customer.name for customer in self.customers]:
            name = random.choice(self.customer_names)
        
        pos = self.free_customers_pos.index(True)
        self.free_customers_pos[pos] = False
        self.customers.append(Customer(name, self.instrument_names, 1430, self.customers_pos[pos], len(self.players)))
        self.tracks.append(Track(self.instrument_names, name))

pygame.init()
screen = pygame.display.set_mode((1920, 1080), pygame.SCALED | pygame.FULLSCREEN)

pygame.display.set_caption("Studio Rush")

game = Game(screen)
game.run()

pygame.quit()