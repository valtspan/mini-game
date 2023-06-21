from object import Object
import pygame

class Trophy(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "trophy")
        image = pygame.image.load("sprites/trophy.png").convert_alpha()
        self.image = pygame.transform.scale(image, (width,height))