import pygame
from pygame.surface import Surface


tile_size = 16
screen_width: int = 640
screen_height: int = 480

fps = 60


def init_screen():
    display = pygame.display.set_mode(
        (screen_width, screen_height),
        flags=pygame.SCALED,
    )
    pygame.display.set_caption("Platformer")
    return display


def draw_screen(display: Surface):
    display.fill((0, 0, 0))
