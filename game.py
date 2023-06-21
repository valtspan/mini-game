import pygame 

from os import listdir
from block import Block
from cherry import Cherry
from player import Player
from pygame.locals import *
from os.path import isfile, join
from pygame import mixer
from trophy import Trophy
from utils import get_sprite_image

# CONFIGURATION
# ---------------------------------------------------------
PLAYER_VEL = 5
scroll = 0
offset_x = 0
FPS = 60
WIDTH, HEIGHT = 1200, 800
# ---------------------------------------------------------

# INITIALIZATION
# ---------------------------------------------------------
pygame.init()
clock = pygame.time.Clock()

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini-Game Day")

# Init graphics
ground_image = pygame.image.load("./Forest/PNG/Background/Layer_0000.png")
ground_image = pygame.transform.scale(ground_image, (WIDTH,HEIGHT))
ground_WIDTH = ground_image.get_width()
ground_HEIGHT = ground_image.get_height()

all_animations = {"right": {}, "left": {} }
last_update = pygame.time.get_ticks()
frame = 0

sprite_WIDTH = 64 
sprite_HEIGHT = 64

dir1 = "./merchant"
paths = ["idle", "walk"]
for path in paths:
    sprite_sheet = pygame.image.load(join(dir1, path) + ".png").convert_alpha()
    animation = []
    animation_flipped = []
    for x in range(sprite_sheet.get_width() // sprite_WIDTH):
        animation.append(get_sprite_image(sprite_sheet, x, 64, 64, 2.6))
        flipped = pygame.transform.flip(get_sprite_image(sprite_sheet, x, 64, 64, 2.6), True, False)
        flipped.set_colorkey((0,0,0))
        animation_flipped.append(flipped)
    all_animations["right"][path] = animation
    all_animations["left"][path] = animation_flipped

# background
bg_images = []
for i in range(0, 1):
    n = i // 10
    m = i % 10
    # bg_image = pygame.image.load(f"./Forest/PNG/Background/Layer_00{n}{m}.png")
    bg_image = pygame.image.load("Background.png").convert()
    bg_image = pygame.transform.scale(bg_image, (WIDTH,HEIGHT))
    bg_images.append(bg_image)
# ---------------------------------------------------------

# SOUND
# ---------------------------------------------------------
mixer.init()
channel0 = mixer.Channel(0)
channel1 = mixer.Channel(1)
channel0.play(mixer.Sound('sound/hiding-in-the-forest.mp3'), -1)
# ---------------------------------------------------------

# DRAWING
def draw_bg():
    for x in range(3):
        speed = 1
        for i in reversed(bg_images):
            window.blit(i, (x * WIDTH + scroll * speed, 0))
            speed += 0.2

def draw_player(player):
    player.draw(window, offset_x)

def draw(player, objects):
    draw_bg()
    draw_player(player)

    for obj in objects:
        if abs(player.rect.x - obj.rect.x < WIDTH): 
            obj.draw(window, offset_x)

    pygame.display.update()
# ---------------------------------------------------------

# COLLISION AND MOVEMENT
# ---------------------------------------------------------
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

    if player.rect.top > HEIGHT:
        exit()

    has_collided_left = collide(player, objects, -PLAYER_VEL)
    has_collided_right = collide(player, objects, PLAYER_VEL)

    removes = []
    for obj in objects:
        if isinstance(obj, Cherry) and pygame.sprite.collide_rect(player, obj):
            removes.append(obj)
            channel1.play(mixer.Sound('sound/item-pickup.mp3'))
        if isinstance(obj, Trophy) and pygame.sprite.collide_rect(player, obj):
            removes.append(obj)
            channel1.play(mixer.Sound('sound/tadaa.mp3'))

    for obj in removes:
        objects.remove(obj)

    if has_collided_left is Cherry:
        mixer.music.load('sound/item-pickup.mp3')
        mixer.music.play()
        
    if keys[pygame.K_LEFT] and not has_collided_left:
        player.move_left(PLAYER_VEL)
        
    if keys[pygame.K_RIGHT] and not has_collided_right:
        player.move_right(PLAYER_VEL)

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
# ---------------------------------------------------------

# GAME WORLD
# ---------------------------------------------------------
player = Player(WIDTH * 0.2, HEIGHT * 0.5, 75, 75, all_animations)

block_size = 96

cherries = [Cherry(block_size * 6, HEIGHT - block_size * 1.5, 32, 32),
            Cherry(block_size * 7, HEIGHT - block_size * 3.5, 32, 32),
            Cherry(block_size * 11, HEIGHT - block_size * 4.5, 32, 32),
            Cherry(block_size * 13, HEIGHT - block_size * 4.5, 32, 32),
            Cherry(block_size * 18, HEIGHT - block_size * 6.5, 32, 32),
            Cherry(block_size * 26, HEIGHT - block_size * 4.5, 32, 32),
            Cherry(block_size * 32, HEIGHT - block_size * 2.5, 32, 32),
            Cherry(block_size * 35, HEIGHT - block_size * 1.5, 32, 32),
            Cherry(block_size * 45, HEIGHT - block_size * 3.5, 32, 32),
            ]

floor = [Block(i * block_size, HEIGHT - block_size, block_size)
            for i in range(0, (WIDTH * 2) // block_size)]
blocks = [Block(block_size * 5, HEIGHT - block_size * 2, block_size),
            Block(block_size * 7, HEIGHT - block_size * 3, block_size),
            Block(block_size * 8, HEIGHT - block_size * 4, block_size),
            Block(block_size * 11, HEIGHT - block_size * 4, block_size),
            Block(block_size * 13, HEIGHT - block_size * 4, block_size),
            Block(block_size * 15, HEIGHT - block_size * 5, block_size),
            Block(block_size * 18, HEIGHT - block_size * 5, block_size),
            Block(block_size * 20, HEIGHT - block_size * 6, block_size),
            Block(block_size * 23, HEIGHT - block_size * 4, block_size),
            Block(block_size * 26, HEIGHT - block_size, block_size),
            Block(block_size * 28, HEIGHT - block_size, block_size),
            Block(block_size * 30, HEIGHT - block_size * 2, block_size),
            Block(block_size * 32, HEIGHT - block_size * 1, block_size),
            Block(block_size * 35, HEIGHT - block_size * 1, block_size),
            Block(block_size * 37, HEIGHT - block_size * 2, block_size),
            Block(block_size * 39, HEIGHT - block_size * 2, block_size),
            Block(block_size * 42, HEIGHT - block_size * 3, block_size),
            Block(block_size * 42, HEIGHT - block_size * 3, block_size),
            Block(block_size * 46, HEIGHT - block_size * 1, block_size),
            Block(block_size * 47, HEIGHT - block_size * 1, block_size),
            Block(block_size * 48, HEIGHT - block_size * 1, block_size),
            Block(block_size * 49, HEIGHT - block_size * 1, block_size),
            Block(block_size * 50, HEIGHT - block_size * 1, block_size)]
objects = [*floor, *blocks, *cherries, Trophy(block_size * 50, HEIGHT - block_size * 2, block_size, block_size)]
# ---------------------------------------------------------


# GAME LOOP
# ---------------------------------------------------------
running = True
while running:
    clock.tick(FPS)

    # key = pygame.key.get_pressed()
    # if key[pygame.K_LEFT] and scroll < 0:
    #     scroll += 5
    # if key[pygame.K_RIGHT] and scroll > -500:
    #     scroll -= 5 

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

    if ((player.rect.right - offset_x > WIDTH * 0.8) and player.x_vel > 0) or (
                (player.rect.left - offset_x < WIDTH * 0.2) and player.x_vel < 0):
            offset_x += player.x_vel
    
pygame.quit()
# ---------------------------------------------------------