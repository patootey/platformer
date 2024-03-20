import pygame.sprite
from pygame.rect import Rect
from pygame.sprite import AbstractGroup, Sprite
from pygame.surface import Surface

from camera import Camera


class PlatformSprite(Sprite):
    """
    Represents a sprite in the platformer game.

    Attributes:
        rect (Rect): The rectangle representing the position and dimensions of the sprite.

    """

    rect: Rect

    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.rect = Rect(0, 0, 1, 1)


def camera_draw(group: pygame.sprite.AbstractGroup, camera: Camera, surface: Surface):
    """draw all sprites onto the surface

    Group.draw(surface): return Rect_list

    Draws all of the member sprites onto the given surface.

    """
    sprites = group.sprites()
    if hasattr(surface, "blits"):

        def make_tuple(spr: Sprite):
            if spr.image is None or spr.rect is None:
                raise TypeError("Sprite image or rect is None")
            return (spr.image, camera.transform(spr))

        rects = surface.blits(make_tuple(spr) for spr in sprites)  # type: ignore
        group.spritedict.update(
            zip(
                sprites,
                rects or [],
            )
        )
    else:
        for spr in sprites:
            if spr.image is None or spr.rect is None:
                raise TypeError("Sprite image or rect is None")

            group.spritedict[spr] = surface.blit(spr.image, camera.transform(spr))
    group.lostsprites = []
    dirty = group.lostsprites
    return dirty


class PlayerGroup(pygame.sprite.GroupSingle):
    """
    Represents a group containing a single player sprite.

    Attributes:
        camera (Camera): The camera used to adjust sprite positions during drawing.

    Methods:
        draw: Draws the sprite onto the surface, adjusting for camera position.
    """

    def __init__(self, camera: Camera, sprite: PlatformSprite) -> None:
        super().__init__(sprite)
        self.camera = camera

    def draw(self, surface: Surface):
        """draw all sprites onto the surface

        Group.draw(surface): return Rect_list

        Draws all of the member sprites onto the given surface.

        """
        return camera_draw(self, self.camera, surface)


class TileGroup(pygame.sprite.Group):
    """
    Represents a group containing sprites representing tiles.

    Attributes:
        camera (Camera): The camera used to adjust sprite positions during drawing.

    Methods:
        draw: Draws the sprites onto the surface, adjusting for camera position.
    """

    def __init__(self, camera: Camera, *sprites: PlatformSprite) -> None:
        super().__init__(sprites)
        self.camera = camera

    def draw(self, surface: Surface):
        """draw all sprites onto the surface

        Group.draw(surface): return Rect_list

        Draws all of the member sprites onto the given surface.

        """
        return camera_draw(self, self.camera, surface)
