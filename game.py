from pathlib import Path

import pygame

from level import Level, load_level
from settings import draw_screen, fps, init_screen


def main():
    # screen = Screen()
    display = init_screen()
    level_data = load_level(Path("map/test_2.tmj"))
    level = Level(level_data, display)
    clock = pygame.time.Clock()
    delta_time = 0
    done = False
    debug_enabled = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    if debug_enabled:
                        debug_enabled = False
                    else:
                        debug_enabled = True
                if event.key == pygame.K_F2:
                    level.music("audio/screen/EarthTongue - 07 - Earthtongue.mp3")
        draw_screen(display)
        display.fill((135, 206, 235))
        level.update(delta_time=delta_time)
        level.draw()
        if debug_enabled:
            level.debug_draw()

        pygame.display.flip()
        delta_time = clock.tick(fps)


if __name__ == "__main__":
    pygame.init()
    main()
    pygame.quit()
