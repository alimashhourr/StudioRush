import pygame
from utils import resize_img

class Player():
    def __init__(self, x, y, screen_width, screen_height):

        self.idle_animation = [resize_img(pygame.image.load(f"assets/images/player/player_idle_{i}.png"), height=100) for i in range(4)]
        self.walk_animation = [resize_img(pygame.image.load(f"assets/images/player/player_walk_{i}.png"), height=100) for i in range(6)]
        self.current_animation = self.idle_animation
        self.current_frame = 0
        self.animation_speed = 0.1  # Temps entre chaque frame de l'animation
        self.time_since_last_frame = 0
        self.image = self.current_animation[self.current_frame]
        self.dir = 'right'
        self.rect = self.image.get_rect(topleft=(x, y))
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.speed = 200
        self.is_moving = False

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

        # Empêcher le joueur de sortir de l'écran
        self.rect.x = max(0, min(self.rect.x, self.screen_width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, self.screen_height - self.rect.height))

    def update(self, keys, dt):
        dx, dy = 0, 0
        self.is_moving = False

        # Mouvement
        if keys[pygame.K_w]:
            dy -= self.speed * dt
            self.is_moving = True
        if keys[pygame.K_s]:
            dy += self.speed * dt
            self.is_moving = True
        if keys[pygame.K_a]:
            dx -= self.speed * dt
            self.is_moving = True
        if keys[pygame.K_d]:
            dx += self.speed * dt
            self.is_moving = True
        
        # Vitesse de déplacement diagonale
        if dx != 0 and dy != 0:
            dx /= 1.4142 # sqrt(2)
            dy /= 1.4142 # sqrt(2)
        
        self.move(dx, dy)

        # Animation
        self.time_since_last_frame += dt

        if self.time_since_last_frame >= self.animation_speed:
            self.current_frame += 1
            if self.current_frame >= len(self.current_animation):
                self.current_frame = 0
            self.image = self.current_animation[self.current_frame]
            self.time_since_last_frame = 0
        
        if self.is_moving:
            self.current_animation = self.walk_animation
        else:
            self.current_animation = self.idle_animation
    
    def draw(self, screen):
        if self.dir == 'right':
            screen.blit(self.image, self.rect)
        else:
            screen.blit(pygame.transform.flip(self.image, True, False), self.rect)