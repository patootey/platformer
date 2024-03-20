from pygame.surface import Surface

from sprite import PlatformSprite


class Tile(PlatformSprite):
    """
    Represents a tile sprite in the game, inheriting from PlatformSprite.

    Attributes:
        image (Surface): The image of the tile sprite.
        rect (Rect): The rectangle representing the position and dimensions of the tile sprite.

    """

    def __init__(self, position, image: Surface):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=position)
