import pygame
from utils import resize_img
from player import Player
from instrument import Instrument
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
            Instrument("guitar", 574, 772),
            Instrument("bass", 1005, 375),
            Instrument("drums", 927, 750),
            Instrument("piano", 679, 440),
            Instrument("computer", 1391, 374)
        ]

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
        
        self.tracks.append(Track(["guitar", "bass", "drums", "piano", "computer"]))

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
                        if self.player.rect.colliderect(instrument.rect) and len(self.tracks):
                            instrument.play()
                            self.tracks[self.selected_track].add(instrument.name)
                elif event.key in [pygame.K_LEFT, pygame.K_DOWN, pygame.K_UP, pygame.K_RIGHT]:
                    for instrument in self.instruments:
                        if instrument.playing:
                            instrument.arrow_key([pygame.K_LEFT, pygame.K_DOWN, pygame.K_UP, pygame.K_RIGHT].index(event.key))
                            break

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
            instrument.update(now, self.dt)

    def display(self):
        # Dessiner l'image de fond
        self.screen.blit(self.background, (0, 0))

        # Dessiner le instruments
        for instrument in self.instruments:
            instrument.draw(self.screen, self.player)

        # Dessiner le joueur
        self.player.draw(self.screen)

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