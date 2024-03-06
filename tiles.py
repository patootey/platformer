from pygame.surface import Surface

from sprite import PlatformSprite


class Tile(PlatformSprite):
    def __init__(self, position, image: Surface):
        super().__init__()
        # self.image = pygame.Surface((size, size))
        # self.image.fill("red")
        self.image = image
        self.rect = self.image.get_rect(topleft=position)
        # self.world_rect = self.image.get_rect(topleft=position)
