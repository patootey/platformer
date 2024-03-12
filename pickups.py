from pygame.surface import Surface
from sprite import PlatformSprite


class PickUpSprite(PlatformSprite):
    def __init__(self, position, image: Surface):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=position)
