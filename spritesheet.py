import pygame

class SpriteSheet():
    def __init__(self, image):
        self.sheet = image

    def get_sprite_image(self, frame, width, height, scale):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), (0, (frame * height), width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        # make background transparent
        image.set_colorkey((0, 0, 0))

        return image
