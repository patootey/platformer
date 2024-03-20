import json
from dataclasses import dataclass
from pathlib import Path

import pygame.draw
import pygame.image
from pygame.font import SysFont
from pygame.surface import Surface

from camera import Camera
from player import Player
from enemy import Enemy
from settings import screen_width, tile_size
from sprite import PlatformSprite, PlayerGroup, TileGroup
from tiles import Tile
from pickups import PickUpSprite
import os


@dataclass
class LevelData:
    tiles: list[list[int]]
    width: int
    height: int


if os.name == "nt":
    pygame_dir = os.path.split(pygame.__file__)[0]
    os.add_dll_directory(pygame_dir)


def load_level(file_name: Path) -> LevelData:
    with open(file_name) as level_file:
        level_data = json.load(level_file)
        if not isinstance(level_data, dict):
            raise TypeError(f"Level did not contain a dictonary: {file_name}")
        layers = level_data.get("layers")
        if not isinstance(layers, list):
            raise TypeError(f"Layers entry in level is not a list: {file_name}")
        tile_layers: list[dict] = []
        for layer in layers:
            if not isinstance(layer, dict):
                raise TypeError(f"Layer did not contain a dictonary: {file_name}")
            layer_type = layer.get("type")
            if layer_type == "tilelayer":
                tile_layers.append(layer)
        if len(tile_layers) != 1:
            raise ValueError(f"Level has more than one tile layer: {file_name}")
        layer = tile_layers[0]
        data = layer.get("data")
        if not isinstance(data, list):
            raise TypeError(f"Data entry in level is not a list: {file_name}")
        width = layer.get("width")
        if not isinstance(width, int):
            raise TypeError(f"Width entry in level is not an int: {file_name}")
        height = layer.get("height")
        if not isinstance(height, int):
            raise TypeError(f"Height entry in level is not an int: {file_name}")

        tiles: list[list[int]] = []
        offset = 0
        for _ in range(height):
            tiles.append(data[offset : offset + width])
            offset += width

        return LevelData(tiles=tiles, width=width, height=height)


def hasCollided(a, b) -> bool:
    """
    Checks collision between object a and b, returns true if collided, false if not.
    Objects must have x, y, width and height.

    Code from:
    "https://stackoverflow.com/questions/2440377/javascript-collision-detection"
    """
    return not (
        ((a.y + a.height) < b.y)
        or (a.y > (b.y + b.height))
        or ((a.x + a.width) < b.x)
        or (a.x > (b.x + b.width))
    )


class Level:
    """
    Represents a level in the game, managing its setup, collision detection, camera movement,
    and updating/drawing of sprites.

    Attributes:
        display_surface (Surface): The surface where the level is displayed.
        camera_speed_x (int): The speed of horizontal camera movement.
        camera (Camera): The camera object used for viewport transformation.
        font (Font): The font used for text rendering.
        tile_sheet (Surface): The sprite sheet containing tiles for the level.
        pickup_coins_sprite_sheet (Surface): The sprite sheet containing pickup coins.
        points (int): The total points collected in the level.

    Methods:
        level_setup: Sets up the level based on the layout of tiles.
        camera_movement: Manages camera movement based on player position.
        collision: Handles collision detection between player and pickups.
        collision_x: Handles collision detection along the x-axis.
        collision_y: Handles collision detection along the y-axis.
        music: Plays background music for the level.
        update: Updates the state of the level.
        draw: Draws the level on the display surface.
        debug_draw: Draws debug information on the display surface.
    """

    def __init__(self, level_data: LevelData, surface: Surface):
        # level setup
        self.display_surface = surface
        self.camera_speed_x = 0
        # self.camera_x = 0
        self.camera = Camera(0, 0, surface.get_width(), surface.get_height())
        self.font = SysFont("Arial", 20)
        self.tile_sheet = pygame.image.load(
            "sprites/platformer_tileset_by_Brysia/Tileset_by_Brysia.png"
        )
        self.tile_2 = self.tile_sheet.subsurface(16, 0, 16, 16)
        self.pickup_coins_sprite_sheet = pygame.image.load(
            "sprites/pickups/gold_coin_strip4.png"
        )
        self.pickup_coin = self.pickup_coins_sprite_sheet.subsurface(0, 0, 12, 12)
        self.tile_9 = self.tile_sheet.subsurface(16, 16, 16, 16)
        self.tile_16 = self.tile_sheet.subsurface(16, 32, 16, 16)
        self.tile_8 = self.tile_sheet.subsurface(0, 16, 16, 16)
        self.tile_10 = self.tile_sheet.subsurface(32, 16, 16, 16)
        self.tile_15 = self.tile_sheet.subsurface(0, 32, 16, 16)
        self.tile_17 = self.tile_sheet.subsurface(32, 32, 16, 16)

        self.tile_27 = self.tile_sheet.subsurface(80, 48, 16, 16)
        self.level_setup(level_data.tiles)
        self.level_data = level_data

        self.points = 0

    def level_setup(self, layout: list[list[int]]):
        self.tiles = TileGroup(self.camera)
        self.pickups = TileGroup(self.camera)
        self.player = Player()
        self.enemy = Enemy()
        self.player_group = PlayerGroup(self.camera, self.player)
        # enumarate (index, information), tells which row we are on
        for row_index, row in enumerate(layout):
            for column_index, tile_id in enumerate(row):
                x = column_index * tile_size
                y = row_index * tile_size

                if tile_id == 2:
                    tile = Tile((x, y), self.tile_2)
                    self.tiles.add(tile)
                if tile_id == 8:
                    tile = Tile((x, y), self.tile_8)
                    self.tiles.add(tile)
                if tile_id == 9:
                    tile = Tile((x, y), self.tile_9)
                    self.tiles.add(tile)
                if tile_id == 10:
                    tile = Tile((x, y), self.tile_10)
                    self.tiles.add(tile)
                if tile_id == 15:
                    tile = Tile((x, y), self.tile_15)
                    self.tiles.add(tile)
                if tile_id == 16:
                    tile = Tile((x, y), self.tile_16)
                    self.tiles.add(tile)
                if tile_id == 17:
                    tile = Tile((x, y), self.tile_17)
                    self.tiles.add(tile)
                if tile_id == 27:
                    tile = Tile((x, y), self.tile_27)
                    self.tiles.add(tile)

                if tile_id == 7:
                    pickup = PickUpSprite((x, y), self.pickup_coin)
                    self.pickups.add(pickup)

                if tile_id == 1:
                    # player_sprite = Player((x, y))
                    self.player_start_position = self.player.rect.topleft = (x, y)

    def camera_movement(self):
        # player_group = self.player_group.sprite
        player_x = self.player.rect.centerx
        direction_x = self.player.direction.x

        if player_x < self.camera.rect.x + screen_width / 4 and direction_x < 0:  # left
            self.camera_speed_x = -self.player.speed

        elif (
            player_x > self.camera.rect.x + screen_width - (screen_width / 4)
            and direction_x > 0
        ):  # right
            self.camera_speed_x = self.player.speed
        else:
            self.camera_speed_x = 0

        self.camera.rect.x += self.camera_speed_x

        width_pixels = self.level_data.width * 16
        if self.camera.rect.x < 0:
            self.camera.rect.x = 0
        if self.camera.rect.right > width_pixels:
            self.camera.rect.right = width_pixels

    def collision(self):
        for sprite in self.pickups.sprites():
            if not isinstance(sprite, PlatformSprite):
                continue
            if sprite.rect.colliderect(self.player.next_pos):
                if isinstance(sprite, PickUpSprite):
                    sprite.kill()
                    self.points += 1

    def collision_x(self):
        self.player.next_pos.x += int(self.player.direction.x * self.player.speed)

        width_pixels = self.level_data.width * 16
        if self.player.next_pos.x < 0:
            self.player.next_pos.x = 0
        elif self.player.next_pos.right > width_pixels:
            self.player.next_pos.right = width_pixels

        for sprite in self.tiles.sprites():
            if not isinstance(sprite, PlatformSprite):
                continue
            if sprite.rect.colliderect(self.player.next_pos):
                if isinstance(sprite, Tile):
                    if self.player.direction.x < 0:  # left
                        self.player.next_pos.left = sprite.rect.right
                    elif self.player.direction.x > 0:  # right
                        self.player.next_pos.right = sprite.rect.left

    def collision_y(self):
        height_pixels = self.level_data.height * 16
        if self.player.next_pos.top > height_pixels:
            self.player.next_pos.topleft = self.player_start_position

        for sprite in self.tiles.sprites():
            if not isinstance(sprite, PlatformSprite):
                continue
            if sprite.rect.colliderect(self.player.next_pos):
                if isinstance(sprite, Tile):
                    if self.player.direction.y > 0:  # down
                        if (
                            self.player.state == "falling"
                            or self.player.state == "jumping"
                        ):
                            self.player.animation_time = 0.0
                            self.player.state = "idle"
                        self.player.next_pos.bottom = sprite.rect.top
                        self.player.is_on_ground = True
                        self.player.direction.y = 0
                    elif self.player.direction.y < 0:  # up
                        self.player.next_pos.top = sprite.rect.bottom
                        self.player.direction.y = 0

    def music(self, audio: str):
        pygame.mixer.init()
        pygame.mixer.music.load(audio)
        pygame.mixer.music.play()

    def update(self, delta_time: int):
        self.tiles.update()
        self.player_group.update(delta_time=delta_time)
        self.enemy.update(delta_time=delta_time)
        self.collision_y()
        self.collision_x()
        self.collision()

        self.player.apply_position()

        self.camera_movement()

    def draw(self):
        self.tiles.draw(self.display_surface)
        self.pickups.draw(self.display_surface)
        self.player_group.draw(self.display_surface)

    def debug_draw(self):
        counter = 0
        real_time = pygame.time.get_ticks()
        color = (0, 0, 0)
        for rect in self.player.debug_history:
            if counter == 29:
                color = (216, 191, 216)
            elif counter == 28:
                color = (255, 255, 0)
            else:
                color = (250, 250, 250)
            counter += 1
            pygame.draw.rect(
                self.display_surface,
                color,
                self.camera.transform_rect(rect),
                1,
            )

        text = self.font.render(self.player.state, True, (40, 50, 30))
        text2 = self.font.render(str(real_time), True, (60, 50, 30))
        text3 = self.font.render(str(self.points), True, (90, 80, 30))
        self.display_surface.blit(text, text.get_rect().move(10, 10))
        self.display_surface.blit(text2, text2.get_rect().move(50, 10))
        self.display_surface.blit(text3, text3.get_rect().move(100, 10))


if __name__ == "__main__":
    level = load_level(Path("map/test_22.tmj"))
    print(level)
