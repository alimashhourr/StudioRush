import pygame

def resize_img(image, width=None, height=None):
    og_width, og_height = image.get_size()
    if width:
        height = int(width * og_height / og_width) # Maintain aspect ratio
    elif height:
        width = int(height * og_width / og_height) # Maintain aspect ratio
    return pygame.transform.scale(image, (width, height))