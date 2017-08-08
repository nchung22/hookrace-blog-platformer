from basic2d import Point2d, Vector2d
from sdl2 import SDL_FLIP_HORIZONTAL, SDL_FLIP_NONE
from sdl2.ext import Renderer, Resources, SpriteFactory, TextureSprite
from tilemap import Map
from typing import Tuple


Rect = Tuple[int, int, int, int]


PLAYER_SIZE = Vector2d(64, 64)


class Player:
    def __init__(self, resources: Resources) -> None:
        self.texture = None  # type: TextureSprite
        self.texture_path = resources.get_path("player.png")
        self.pos = None  # type: Point2d
        self.vel = None  # type: Vector2d
        self.restart()

    def restart(self) -> None:
        self.pos = Point2d(170, 500)
        self.vel = Vector2d(0, 0)

    def on_ground(self, tilemap: Map) -> bool:
        return tilemap.on_ground(self.pos, PLAYER_SIZE)

    def update_position(self, tilemap: Map, new_vel: Vector2d) -> None:
        self.pos, self.vel = tilemap.move_box(
            self.pos, new_vel, PLAYER_SIZE
        )

    def render(self, renderer: Renderer, camera: Vector2d) -> None:
        if self.texture is None:
            factory = SpriteFactory(renderer=renderer)
            print(f"loading texture: {self.texture_path}")
            self.texture = factory.from_image(self.texture_path)  # type: TextureSprite
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
            renderer.copy(self.texture, source, dest, angle=0,
                          center=None, flip=flip)
