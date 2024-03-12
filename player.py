import pygame
from pygame.rect import Rect

from sprite import PlatformSprite


class Player(PlatformSprite):
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
