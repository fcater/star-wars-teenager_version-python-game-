import pygame
from pygame.locals import *
import sys

pygame.init()
pygame.mixer.init()
bg_size = width, height = 500, 600
screen = pygame.display.set_mode(bg_size)
bg = pygame.image.load("image/background.png").convert()
key_pressed = pygame.key.get_pressed()
while 1:
    screen.blit(pygame.transform.scale(bg, bg_size), (0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    for each in key_pressed:
        print(each[K_SPACE])
