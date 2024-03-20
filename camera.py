from pygame.rect import Rect
from pygame.sprite import Sprite


class Camera:
    """
    Represents a camera used to transform the position and dimensions of sprites or rectangles
    based on its own position and dimensions.

    Attributes:
        rect (Rect): A rectangle representing the position and dimensions of the camera.

    Methods:
        transform: Transforms the position of a sprite relative to the camera's position.
        transform_rect: Transforms the position of a rectangle relative to the camera's position.
    """

    def __init__(self, x: float, y: float, width: float, height: float):
        self.rect = Rect(x, y, width, height)

    def transform(self, sprite: Sprite) -> Rect:
        if sprite.rect is None:
            raise Exception("Sprite does not have a rect set")

        return sprite.rect.move(-self.rect.x, -self.rect.y)

    def transform_rect(self, rect: Rect) -> Rect:
        return rect.move(-self.rect.x, -self.rect.y)
