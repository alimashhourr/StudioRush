import pygame
from utils import resize_img
from player import Player
from instrument import Instrument

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
        
        # Instruments
        self.instruments = {
            "guitar": Instrument("guitar", 574, 772),
            "bass": Instrument("bass", 1005, 375),
            "drums": Instrument("drums", 927, 750),
            "piano": Instrument("piano", 679, 440),
            "computer": Instrument("computer", 1391, 374)
        }

        # Collision
        self.collisions = [
            pygame.Rect(340, 430, 20, 560),
            pygame.Rect(1600, 430, 20, 560),
            pygame.Rect(340, 430, 1280, 20),
            pygame.Rect(340, 955, 1280, 20)
        ]

        self.on_guitar = False

    def handling_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.player.dir = 'left'
                elif event.key == pygame.K_d:
                    self.player.dir = 'right'
                if event.key == pygame.K_SPACE:
                    pass

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
        now = pygame.time.get_ticks()
        self.player.update(self.dt, self.collisions)
        print(self.player.hitbox.topleft)
        
        for instrument in self.instruments.values():
            instrument.update()

    def display(self):
        # Dessiner l'image de fond
        self.screen.blit(self.background, (0, 0))

        # Dessiner le instruments
        for instrument in self.instruments.values():
            if self.player.rect.colliderect(instrument.rect):
                screen.blit(instrument.img_highlight, instrument.rect)
            else:
                screen.blit(instrument.img, instrument.rect)

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
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Studio Rush")

game = Game(screen)
game.run()

pygame.quit()