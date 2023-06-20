import pygame 
from pygame.locals import *
from os.path import join

pygame.init()

clock = pygame.time.Clock()
FPS = 60
scroll = 0

def get_sprite_image(sheet, frame, width, height, scale):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), (0, (frame * height), width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    # make background transparent
    image.set_colorkey((0, 0, 0))

    return image

width, height = 1000, 500
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Parallax")

# sprite things
# sprite_sheet_image = pygame.image.load("./BotWheel/move_with_FX.png").convert_alpha()
# sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)

#create animation list
all_animations = {}
animation_steps = 4
last_update = pygame.time.get_ticks()
animation_cooldown_wake = 700
animation_cooldown = 1000
frame = 0

# load animation for number of steps
sprite_width = 45
sprite_height = 26

dir1 = "./BotWheel"
paths = ["move", "wake", "shoot", "damaged", "death"]
for path in paths:
    sprite_sheet = pygame.image.load(join(dir1, path) + ".png").convert_alpha()
    animation = []
    for x in range(sprite_sheet.get_height() // sprite_height):
        animation.append(get_sprite_image(sprite_sheet, x, 65, 26, 3))
    all_animations[path] = animation

# background
bg_images = []
for i in range(0, 12):
    n = i // 10
    m = i % 10
    bg_image = pygame.image.load(f"./Forest/PNG/Background/Layer_00{n}{m}.png").convert_alpha()
    bg_image = pygame.transform.scale(bg_image, (width,height))
    bg_images.append(bg_image)

def draw_bg():
    for x in range(3):
        speed = 1
        for i in reversed(bg_images):
            window.blit(i, (x * width + scroll * speed, 0))
            speed += 0.2

# game loop
i = 0
runing = True
mode = "wake"
while runing:
    clock.tick(FPS)
    animation_cooldown_wake = 700
    animation_cooldown = 1000

    draw_bg()
    
    window.blit(all_animations[mode][frame], (0, 0))

    # update animation
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cooldown_wake:
        frame += 1
        last_update = current_time
        if frame == animation_steps:
            frame = 0
        

    # move background
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and scroll < 0:
        scroll += 5
    if key[pygame.K_RIGHT] and scroll > -500:
        scroll -= 5

    for event in pygame.event.get():
        if event.type == QUIT:
            runing = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                mode = "shoot"
            if event.key == pygame.K_RIGHT:
                mode = "move"
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                mode = "wake"
            if event.key == pygame.K_RIGHT:
                mode = "wake"


    pygame.display.update()
pygame.quit()
