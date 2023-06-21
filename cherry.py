from object import Object
from utils import load_sprite_sheets
import pygame

class Cherry(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "sprites/cherry")
        self.cherry = load_sprite_sheets(width, height)
        self.image = self.cherry["Cherries"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "Cherries"

    def on(self):
        self.animation_name = "Cherries"

    def off(self):
        self.animation_name = "Cherries"

    def loop(self):
        sprites = self.cherry[self.animation_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0