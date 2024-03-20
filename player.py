import pygame
from pygame.rect import Rect

from sprite import PlatformSprite


class Player(PlatformSprite):
    """
    Represents the player character in the game, inheriting from PlatformSprite.

    Attributes:
        height (int): The height of the player sprite.
        width (int): The width of the player sprite.
        idle_frames_right (List[Surface]): Frames for the idle animation facing right.
        idle_frames_left (List[Surface]): Frames for the idle animation facing left.
        walking_frames_right (List[Surface]): Frames for the walking animation facing right.
        walking_frames_left (List[Surface]): Frames for the walking animation facing left.
        jump_frame_right (Surface): Frame for the jumping animation facing right.
        jump_frame_left (Surface): Frame for the jumping animation facing left.
        falling_frame_right (Surface): Frame for the falling animation facing right.
        falling_frame_left (Surface): Frame for the falling animation facing left.
        image (Surface): The current image of the player sprite.
        rect (Rect): The rectangle representing the position and dimensions of the player sprite.
        next_pos (Rect): The next position of the player sprite.
        is_on_ground (bool): Indicates if the player is currently on the ground.
        jump_speed (float): The initial jump speed of the player.
        gravity (float): The gravitational acceleration affecting the player.
        direction (Vector2): The direction of movement of the player.
        look_direction (int): The direction the player is facing (-1 for left, 1 for right).
        speed (int): The movement speed of the player.
        debug_history (List[Rect]): History of debug positions of the player.
        state (str): The current state of the player (e.g., "idle", "walking", "jumping").
        jump_counter (int): Counter for the duration of the jump.
        imageindex (int): Index of the current frame in the animation.
        animation_time (float): The time elapsed since the start of the animation.
        frame_time_idle (int): The time interval between frames for idle animation.
        frame_time_walking (int): The time interval between frames for walking animation.

    Methods:
        debug_push_position: Adds the current position to the debug history.
        movement: Handles player movement based on input.
        jump: Initiates a jump for the player.
        apply_gravity: Applies gravitational force to the player.
        apply_position: Applies the next position to the player sprite.
        update: Updates the state and animation of the player sprite.
    """

    def __init__(self, pos: tuple[float, float] = (0, 0)):
        super().__init__()
        # self.path()
        self.height = 32
        self.width = 32
        image_idle = pygame.image.load(
            "sprites/simple_character_by_Brysia/idle_strip3-sheet.png"
        )
        self.idle_frames_right = [
            image_idle.subsurface(0, 0, 10, 14),
            image_idle.subsurface(10, 0, 10, 14),
            image_idle.subsurface(20, 0, 10, 14),
        ]
        self.idle_frames_left = [
            pygame.transform.flip(self.idle_frames_right[0], True, False),
            pygame.transform.flip(self.idle_frames_right[1], True, False),
            pygame.transform.flip(self.idle_frames_right[2], True, False),
        ]

        image_walk = pygame.image.load(
            "sprites/simple_character_by_Brysia/walk_strip8-sheet.png"
        )
        self.walking_frames_right = [
            image_walk.subsurface(0, 0, 10, 14),
            image_walk.subsurface(10, 0, 10, 14),
            image_walk.subsurface(20, 0, 10, 14),
            image_walk.subsurface(30, 0, 10, 14),
            image_walk.subsurface(40, 0, 10, 14),
            image_walk.subsurface(50, 0, 10, 14),
            image_walk.subsurface(60, 0, 10, 14),
            image_walk.subsurface(70, 0, 10, 14),
        ]
        self.walking_frames_left = [
            pygame.transform.flip(self.walking_frames_right[0], True, False),
            pygame.transform.flip(self.walking_frames_right[1], True, False),
            pygame.transform.flip(self.walking_frames_right[2], True, False),
            pygame.transform.flip(self.walking_frames_right[3], True, False),
            pygame.transform.flip(self.walking_frames_right[4], True, False),
            pygame.transform.flip(self.walking_frames_right[5], True, False),
            pygame.transform.flip(self.walking_frames_right[6], True, False),
            pygame.transform.flip(self.walking_frames_right[7], True, False),
        ]
        self.jump_frame_right = pygame.image.load(
            "sprites/simple_character_by_Brysia/look_up-sheet.png"
        )
        self.jump_frame_left = pygame.transform.flip(self.jump_frame_right, True, False)

        self.falling_frame_right = pygame.image.load(
            "sprites/simple_character_by_Brysia/look_down-sheet.png"
        )
        self.falling_frame_left = pygame.transform.flip(
            self.falling_frame_right, True, False
        )

        self.image = self.idle_frames_right[0]
        self.rect = self.image.get_rect(topleft=pos)
        self.next_pos: Rect = self.rect.copy()
        self.is_on_ground = False

        self.jump_speed = -3
        self.gravity = 0.4
        self.direction = pygame.math.Vector2(0.0, 0.0)
        self.look_direction = 1
        self.speed = 2

        self.debug_history = []

        self.state = "idle"
        self.jump_counter = 0

        self.imageindex = 0
        self.animation_time: float = 0.0
        self.frame_time_idle = 250
        self.frame_time_walking = 100

    def debug_push_position(self):
        self.debug_history.append(self.rect.copy())

        if len(self.debug_history) > 30:
            self.debug_history = self.debug_history[-30:]

    def movement(self, delta_time: int):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.direction.x = 1
            self.look_direction = 1
            if self.state == "idle" or self.state == "walking":
                if self.state == "idle":
                    self.animation_time = 0.0
                self.state = "walking"

        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.look_direction = -1
            if self.state == "idle" or self.state == "walking":
                if self.state == "idle":
                    self.animation_time = 0.0
                self.state = "walking"
        else:
            self.direction.x = 0
            if self.state == "idle" or self.state == "walking":
                if self.state == "walking":
                    self.animation_time = 0.0
                self.state = "idle"

        if self.state == "idle" or self.state == "walking":
            if keys[pygame.K_SPACE] and self.is_on_ground:
                self.animation_time = 0.0
                self.state = "jumping"
                self.is_on_ground = False
                self.jump()
                self.jump_counter = 0
        elif self.state == "jumping":
            if keys[pygame.K_SPACE]:
                self.jump_counter += delta_time
                if self.jump_counter > 300:
                    self.animation_time = 0.0
                    self.state = "falling"
                else:
                    self.jump()
            else:
                self.animation_time = 0.0
                self.state = "falling"

    def jump(self):
        self.direction.y = self.jump_speed

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.next_pos.y += self.direction.y  # type: ignore

    def apply_position(self):
        if self.rect != self.next_pos:
            self.debug_push_position()
            self.rect = self.next_pos.copy()

    def update(self, delta_time: int):
        self.next_pos = self.rect.copy()
        self.movement(delta_time=delta_time)
        self.apply_gravity()
        self.animation_time += delta_time

        if self.state == "idle":
            if self.look_direction == 1:
                idle_frames = self.idle_frames_right
            else:
                idle_frames = self.idle_frames_left
            self.animation_time = self.animation_time % (
                len(idle_frames) * self.frame_time_idle
            )
            self.index = int(self.animation_time / self.frame_time_idle)
            self.image = idle_frames[self.index]

        elif self.state == "walking":
            if self.look_direction == 1:
                walking_frames = self.walking_frames_right
            else:
                walking_frames = self.walking_frames_left
            self.animation_time = self.animation_time % (
                len(walking_frames) * self.frame_time_walking
            )
            self.index = int(self.animation_time / self.frame_time_walking)
            self.image = walking_frames[self.index]

        elif self.state == "falling":
            self.index = 0
            self.animation_time = 0.0
            if self.look_direction == 1:
                self.image = self.falling_frame_right
            else:
                self.image = self.falling_frame_left

        elif self.state == "jumping":
            self.index = 0
            self.animation_time = 0.0
            if self.look_direction == 1:
                self.image = self.jump_frame_right
            else:
                self.image = self.jump_frame_left
