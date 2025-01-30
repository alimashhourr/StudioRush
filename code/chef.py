import pygame

class Chef(pygame.sprite.Sprite):
    def __init__(self, idle_animation, run_animations, x, y, screen_width, screen_height):
        super().__init__()  
        self.idle_animation = idle_animation 
        self.run_animations = run_animations  
        self.current_animation = idle_animation  
        self.current_frame = 0  
        self.image = self.current_animation[self.current_frame]  
        self.rect = self.image.get_rect(topleft=(x, y))  
        self.screen_width = screen_width  
        self.screen_height = screen_height 
        self.speed = 5 
        self.direction = "down" 
        self.is_moving = False  
        self.animation_speed = 0.1  # Speed of animation 
        self.time_since_last_frame = 0  
        

    def move(self, dx, dy):
        self.rect.x += dx  # Move horizontally
        self.rect.y += dy  # Move vertically
        # Stay on screen
        self.rect.x = max(0, min(self.rect.x, self.screen_width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, self.screen_height - self.rect.height))

    def update(self, keys, dt):
        dx, dy = 0, 0
        self.is_moving = False

        # Movement
        if keys[pygame.K_w]: 
            dy -= self.speed
            self.direction = "up"
            self.is_moving = True
        if keys[pygame.K_s]:  
            dy += self.speed
            self.direction = "down"
            self.is_moving = True
        if keys[pygame.K_a]: 
            dx -= self.speed
            self.direction = "left"
            self.is_moving = True
        if keys[pygame.K_d]:
            dx += self.speed
            self.direction = "right"
            self.is_moving = True

        # Update position
        self.rect.x += dx
        self.rect.y += dy

        # Prevent player from going out of bounds
        self.rect.x = max(0, min(self.rect.x, self.screen_width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, self.screen_height - self.rect.height))

        # Update animation
        self.time_since_last_frame += dt
        if self.is_moving:
            # Switch to running animation for the current direction
            self.current_animation = self.run_animations[self.direction]
        else:
            # Switch to idle animation
            self.current_animation = self.idle_animation

        # Advance animation frame
        if self.time_since_last_frame >= self.animation_speed:
            self.current_frame = (self.current_frame + 1) % len(self.current_animation)
            self.image = self.current_animation[self.current_frame]
            self.time_since_last_frame = 0