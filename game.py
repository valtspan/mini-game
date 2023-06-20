from os import listdir
from player import Player
import pygame 
from pygame.locals import *
from os.path import isfile, join

# class App:
#     def __init__(self):
#         self._running = True
#         self._display_surf = None
#         self.size = self.weight, self.height = 640, 400
   
#     # initialize PyGAme modules
#     # create main display
#     # use hardware acceleration
#     def on_init(self):
#         pygame.init()
#         self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
#         self._running = True
#         widndow = pygame
#         self._image_surf = pygame.image.load("./Forest/Preview/Background.png")
 
#     def on_event(self, event):
#         if event.type == pygame.QUIT:
#             self._running = False

#     def on_loop(self):
#         pass

#     def on_render(self):
#         self._display_surf.blit(self._image_surf, (0,0))

#     # quits all pygame modules
#     def on_cleanup(self):
#         pygame.quit()
 
#     def on_execute(self):
#         if self.on_init() == False:
#             self._running = False
 
#         while( self._running ):
#             for event in pygame.event.get():
#                 self.on_event(event)
#             self.on_loop()
#             self.on_render()
#         self.on_cleanup()

# if __name__ == "__main__" :
#     theApp = App()
#     theApp.on_execute()

PLAYER_VEL = 10
scroll = 0
SCROLL_VEL = 5
offset_x = 0

pygame.init()

clock = pygame.time.Clock()
FPS = 60

width, height = 1200, 800
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Parallax")

# Init graphics
ground_image = pygame.image.load("./Forest/PNG/Background/Layer_0000.png")
ground_image = pygame.transform.scale(ground_image, (width,height))
ground_width = ground_image.get_width()
ground_height = ground_image.get_height()

bg_images = []
for i in range(0, 1):
    n = i // 10
    m = i % 10
    bg_image = pygame.image.load("Background.png").convert()
    bg_image = pygame.transform.scale(bg_image, (width,height))
    bg_images.append(bg_image)

def load_sprite_sheets(width, height):
    path = join("sprites")
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        all_sprites[image.replace(".png", "")] = sprites

    return all_sprites

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))


class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

        brighten = 50
        self.image.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_SUB) 

class Cherry(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "cherry")
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

def get_block(size):
    path = join("Terrain.png")
    image = pygame.image.load(path).convert()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96, 0, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)

def draw_bg():
    for x in range(3):
        speed = 1
        for i in reversed(bg_images):
            window.blit(i, (x * width + scroll * speed, 0))
            speed += 0.2

def draw_player(player):
    player.draw(window, offset_x)

def draw(player, objects):
    draw_bg()
    draw_player(player)

    for obj in objects:
        if abs(player.rect.x - obj.rect.x < width): 
            obj.draw(window, offset_x)

    pygame.display.update()

def collide(player, objects, dx):
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_rect(player, obj):
            collided_object = obj
            break

    player.move(-dx, 0)
    player.update()
    return collided_object

def handle_move(player, objects):
    global scroll

    keys = pygame.key.get_pressed()

    player.x_vel = 0

    has_collided_left = collide(player, objects, -PLAYER_VEL)
    has_collided_right = collide(player, objects, PLAYER_VEL)

    if keys[pygame.K_LEFT] and not has_collided_left:
        player.move_left(PLAYER_VEL)
        # if scroll < 0:
        #   scroll += SCROLL_VEL

    if keys[pygame.K_RIGHT] and not has_collided_right:
        player.move_right(PLAYER_VEL)
        # if scroll < -500:
        #     scroll -= SCROLL_VEL

    handle_vertical_collision(player, objects, player.y_vel)


def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_rect(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

            collided_objects.append(obj)

    return collided_objects

player = Player(width * 0.2, height * 0.2, 75, 75)

running = True

while running:
    clock.tick(FPS)

    block_size = 96

    cherries = [Cherry(block_size * 6, height - block_size * 2.5, 32, 32),
                Cherry(block_size * 7, height - block_size * 3.5, 32, 32)
                ]

    floor = [Block(i * block_size, height - block_size, block_size)
             for i in range(0, (width * 2) // block_size)]
    blocks = [Block(block_size * 6, height - block_size * 2, block_size),
               Block(block_size * 7, height - block_size * 3, block_size),
               Block(block_size * 8, height - block_size * 4, block_size),
               Block(block_size * 11, height - block_size * 4, block_size),
               Block(block_size * 13, height - block_size * 4, block_size),
               Block(block_size * 15, height - block_size * 5, block_size)]
    objects = [*floor, *blocks, *cherries]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()

    player.loop(FPS)
    for cherry in cherries:
        cherry.loop()
    handle_move(player, objects)
    draw(player, objects)

    if ((player.rect.right - offset_x > width * 0.8) and player.x_vel > 0) or (
                (player.rect.left - offset_x < width * 0.2) and player.x_vel < 0):
            offset_x += player.x_vel
    
pygame.quit()
