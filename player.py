import pygame

class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 1

    def __init__(self, x, y, width, height, animation_lists):
       super().__init__()
       self.rect = pygame.Rect(x, y, width, height)
       self.x_vel = 0
       self.y_vel = 0
       self.mask = None
       self.direction = "left"
       self.frame_count = 0
       self.fall_count = 0
       image = pygame.image.load("fall.png").convert_alpha()
       self.image = pygame.transform.scale(image, (width,height))
       self.mode = "walk"
       self.animation_lists = animation_lists
       self.animation_cooldown = 15
    
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, vel):
        self.mode = "walk"
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.frame_count = 0

    def move_right(self, vel):
        self.mode = "walk"
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.frame_count = 0

    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        self.fall_count += 1
        self.update_sprite()

    def update_sprite(self):
        sprites = self.animation_lists[self.direction][self.mode]
        sprite_index = (self.frame_count // self.animation_cooldown) % len(sprites)
        self.sprite = self.animation_lists[self.direction][self.mode][sprite_index]
        self.frame_count += 1

    def draw(self, win, offset_x):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y - 50))

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

    def jump(self):
        self.y_vel = -self.GRAVITY * 8
        self.frame_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0
