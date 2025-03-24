import pygame
from utils import resize_img

class Player():
    def __init__(self, x, y, screen_width, screen_height):
        self.idle_animation = [resize_img(pygame.image.load(f"assets/images/player/player_idle_{i}.png"), height=120) for i in range(4)]
        self.walk_animation = [resize_img(pygame.image.load(f"assets/images/player/player_walk_{i}.png"), height=120) for i in range(6)]
        self.current_animation = self.idle_animation
        self.current_frame = 0
        self.animation_speed = 0.08  # Temps entre chaque frame de l'animation
        self.time_since_last_frame = 0
        self.image = self.current_animation[self.current_frame]
        self.rect = self.image.get_rect(x=x, y=y)
        self.dir = 'right'

        self.hitbox = pygame.Rect(0, 0, self.rect.width*0.8, self.rect.height/4) # Seuls les pieds du joueur sont en collision avec les tiles
        self.hitbox.midbottom = self.rect.midbottom
        
        self.speed = 200
        self.vel = [0, 0]
        self.is_moving = False

        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self, dt, collisions):
        # MOUVEMENT
        if self.vel[0] != 0 or self.vel[1] != 0:
            self.is_moving = True
        else:
            self.is_moving = False

        dx = self.vel[0] * self.speed * dt
        dy = self.vel[1] * self.speed * dt

        # Vitesse de déplacement diagonale
        if self.vel[0] != 0 and self.vel[1] != 0:
            dx /= 1.41 # sqrt(2)
            dy /= 1.41 # sqrt(2)
        
        # Déplacement horizontal
        self.hitbox.x += dx

        # Collisions
        for rect in collisions:
            if self.hitbox.colliderect(rect):
                if dx > 0:
                    self.hitbox.right = rect.left
                elif dx < 0:
                    self.hitbox.left = rect.right

        # Déplacement vertical
        self.hitbox.y += dy

        # Collision avec les tiles
        for rect in collisions:
            if self.hitbox.colliderect(rect):
                if dy > 0:
                    self.hitbox.bottom = rect.top
                elif dy < 0:
                    self.hitbox.top = rect.bottom
                
        # Empêcher le joueur de sortir de l'écran
        self.hitbox.x = max(0, min(self.hitbox.x, self.screen_width - self.rect.width))
        self.hitbox.y = max(0, min(self.hitbox.y, self.screen_height - self.rect.height))

        # Placer le rect du joueur sur la hitbox
        self.rect.midbottom = self.hitbox.midbottom

        # ANIMATION
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