import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()

fps = 60

screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Explosion Demo")

bg = (60, 50, 70)


def draw_bg():
    screen.fill(bg)


while True:
    draw_bg()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            break

    pygame.display.update()
    clock.tick(fps)
