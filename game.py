import pygame 
from pygame.locals import *
import spritesheet

pygame.init()

clock = pygame.time.Clock()
FPS = 60
scroll = 0

width, height = 1000, 500
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Parallax")

# sprite things
sprite_sheet_image = pygame.image.load("./BotWheel/move_with_FX.png").convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)

#create animation list
animation_list = []
animation_steps = 4
last_update = pygame.time.get_ticks()
animation_cooldown = 500
frame = 0

for x in range(animation_steps):
    animation_list.append(sprite_sheet.get_sprite_image(x, 35, 26, 3))


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
while runing:
    clock.tick(FPS)

    draw_bg()

    window.blit(animation_list[frame], (0, 0))

    # update animation
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cooldown:
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
    pygame.display.update()
pygame.quit()
