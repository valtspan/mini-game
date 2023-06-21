from object import Object
import pygame 
from os.path import join

class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

        brighten = 50
        self.image.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_SUB) 

def get_block(size):
    path = join("sprites/Terrain.png")
    image = pygame.image.load(path).convert()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(16, 16, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)
