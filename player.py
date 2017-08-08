from basic2d import Point2d, Vector2d
from copy import copy
from sdl2 import SDL_FLIP_HORIZONTAL, SDL_FLIP_NONE
from sdl2.ext import Renderer, Resources, SpriteFactory, TextureSprite
from tilemap import Map
from typing import Optional


PLAYER_SIZE = Vector2d(64, 64)
INITIAL_POS = Point2d(170, 500)
INITIAL_VEL = Vector2d(0, 0)


class Player:
    def __init__(self, resources: Resources) -> None:
        self.texture = None  # type: Optional[TextureSprite]
        self.texture_path = resources.get_path("player.png")
        self.pos = copy(INITIAL_POS)
        self.vel = copy(INITIAL_VEL)
        self.restart()

    def restart(self) -> None:
        self.pos = copy(INITIAL_POS)
        self.vel = copy(INITIAL_VEL)

    def on_ground(self, tilemap: Map) -> bool:
        return tilemap.on_ground(self.pos, PLAYER_SIZE)

    def update_position(self, tilemap: Map, new_vel: Vector2d) -> None:
        self.pos, self.vel = tilemap.move_box(
            self.pos, new_vel, PLAYER_SIZE
        )

    def render(self, renderer: Renderer, camera: Vector2d) -> None:
        if self.texture is None:
            factory = SpriteFactory(renderer=renderer)
            self.texture = factory.from_image(self.texture_path)
        texture = self.texture  # type: TextureSprite

        pos = self.pos - camera
        x = int(pos.x)
        y = int(pos.y)

        body_parts = [
            ((192, 64, 64, 32), (x - 60, y, 96, 48),
             SDL_FLIP_NONE),  # back feet shadow
            ((96, 0, 96, 96), (x - 48, y - 48, 96, 96),
             SDL_FLIP_NONE),  # body shadow
            ((192, 64, 64, 32), (x - 36, y, 96, 48),
             SDL_FLIP_NONE),  # front feet shadow
            ((192, 32, 64, 32), (x - 60, y, 96, 48),
             SDL_FLIP_NONE),  # back feet
            ((0, 0, 96, 96), (x - 48, y - 48, 96, 96),
             SDL_FLIP_NONE),  # body
            ((192, 32, 64, 32), (x - 36, y, 96, 48),
             SDL_FLIP_NONE),  # front feet
            ((64, 96, 32, 32), (x - 18, y - 21, 36, 36),
             SDL_FLIP_NONE),  # left eye
            ((64, 96, 32, 32), (x - 6, y - 21, 36, 36),
             SDL_FLIP_HORIZONTAL)  # right eye
        ]
        for source, dest, flip in body_parts:
            renderer.copy(texture, source, dest, angle=0,
                          center=None, flip=flip)
