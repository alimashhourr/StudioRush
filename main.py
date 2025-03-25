import pygame
from utils import resize_img
from player import Player
from instrument import Instrument
from instruments.guitar import Guitar
from track import Track

class Game:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.FPS = 60
        self.running = True
        
        # Charger le fond
        self.background = resize_img(pygame.image.load("assets/images/studio.png"), width=screen.get_width())

        # Objet joueur
        self.player = Player(405, 510, self.screen.get_width(), self.screen.get_height())

        self.instruments = [
            Guitar(574, 772),
            Instrument("bass", 1005, 375),
            Instrument("drums", 927, 750),
            Instrument("piano", 679, 440),
        ]

        self.computer = Instrument("computer", 1391, 374)

        # Collision
        self.collisions = [
            pygame.Rect(340, 430, 20, 560),
            pygame.Rect(1600, 430, 20, 560),
            pygame.Rect(340, 430, 1280, 20),
            pygame.Rect(340, 955, 1280, 20)
        ]

        # Pistes
        self.tracks = []
        self.selected_track = 0
        self.max_instruments_per_track = 8
        
        for i in range(5):
            self.tracks.append(Track(["guitar", "bass", "drums", "piano"], "tyler"))

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

    def update(self):
        now = pygame.time.get_ticks() / 1000
        self.player.update(self.dt, self.collisions)
        
        for instrument in self.instruments:
            instrument.update(now, self.dt, self.player)
        
        self.computer.update(now, self.dt, self.player)

    def display(self):
        # Dessiner l'image de fond
        self.screen.blit(self.background, (0, 0))

        # Dessiner les instruments
        for instrument in self.instruments:
            instrument.draw(self.screen, self.player)
        
        self.computer.draw(self.screen, self.player)

        # Dessiner le joueur
        self.player.draw(self.screen)

        # Dessiner l'interface
        for i, track in enumerate(self.tracks):
            track.draw(self.screen, i, i == self.selected_track)

        # for rect in self.collisions:
        #     pygame.draw.rect(self.screen, (255, 0, 0), rect)

        # Mettre à jour l'écran
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handling_events()
            self.update()
            self.display()
            self.dt = self.clock.tick(self.FPS) / 1000

pygame.init()
screen = pygame.display.set_mode((1920, 1080), pygame.SCALED | pygame.FULLSCREEN)

pygame.display.set_caption("Studio Rush")

game = Game(screen)
game.run()

pygame.quit()