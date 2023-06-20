import pygame 
from pygame.locals import *

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

pygame.init()

clock = pygame.time.Clock()
FPS = 60

width, height = 1000, 500
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Parallax")

scroll = 0

ground_image = pygame.image.load("./Forest/PNG/Background/Layer_0000.png")
ground_image = pygame.transform.scale(ground_image, (width,height))
ground_width = ground_image.get_width()
ground_height = ground_image.get_height()

bg_images = []
for i in range(0, 12):
    n = i // 10
    m = i % 10
    bg_image = pygame.image.load(f"./Forest/PNG/Background/Layer_00{n}{m}.png")
    bg_image = pygame.transform.scale(bg_image, (width,height))
    bg_images.append(bg_image)


def draw_bg():
    for x in range(3):
        speed = 1
        for i in reversed(bg_images):
            window.blit(i, (x * width + scroll * speed, 0))
            speed += 0.2

# def draw_ground():
#     for x in range(15):
#         window.blit(ground_image, ((x * ground_width) - scroll * 2.2, height - ground_height))

i = 0
runing = True
while runing:
    clock.tick(FPS)

    draw_bg()

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
