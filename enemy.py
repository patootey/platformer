import pygame

from sprite import PlatformSprite


class Enemy(PlatformSprite):
    """
    Represents an enemy character in the game, inheriting from PlatformSprite.

    Attributes:
        height (int): The height of the enemy sprite.
        width (int): The width of the enemy sprite.
        state (str): The current state of the enemy, such as "idle" or "walking".
        idle_frames (List[Surface]): A list of frames for the idle animation of the enemy.
        image (Surface): The current image of the enemy sprite.
        rect (Rect): The rectangle representing the position and dimensions of the enemy sprite.
        animation_time (float): The time elapsed since the start of the animation.
        frame_time_idle (int): The time interval between frames for the idle animation.
        frame_time_walking (int): The time interval between frames for the walking animation.

    Methods:
        update: Updates the state and animation of the enemy sprite based on the elapsed time.
    """

    def __init__(self, pos: tuple[float, float] = (0, 0)):
        super().__init__()
        # self.path()
        self.height = 32
        self.width = 32

        self.state = "idle"
        image_idle = pygame.image.load(
            "sprites/GreenSlime_byBrysia/slime_idle-Sheet-sheet.png"
        )
        self.idle_frames = [
            image_idle.subsurface(0, 0, 18, 12),
            image_idle.subsurface(18, 0, 18, 12),
            image_idle.subsurface(36, 0, 18, 12),
            image_idle.subsurface(54, 0, 18, 12),
        ]
        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect(topleft=pos)

        self.animation_time: float = 0.0
        self.frame_time_idle = 250
        self.frame_time_walking = 100

    def update(self, delta_time: int):
        self.animation_time += delta_time
        if self.state == "idle":
            frames = self.idle_frames
            self.animation_time = self.animation_time % (
                len(frames) * self.frame_time_idle
            )
            self.index = int(self.animation_time / self.frame_time_idle)
            self.image = frames[self.index]
