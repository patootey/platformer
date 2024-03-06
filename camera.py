from pygame.rect import Rect
from pygame.sprite import Sprite


class Camera:
    def __init__(self, x: float, y: float, width: float, height: float):
        self.rect = Rect(x, y, width, height)

    def transform(self, sprite: Sprite) -> Rect:
        if sprite.rect is None:
            raise Exception("Sprite does not have a rect set")

        return sprite.rect.move(-self.rect.x, -self.rect.y)

    def transform_rect(self, rect: Rect) -> Rect:
        return rect.move(-self.rect.x, -self.rect.y)
