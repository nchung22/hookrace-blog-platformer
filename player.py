from basic2d import Point2d, Vector2d
from sdl2 import SDL_RendererFlip, SDL_FLIP_HORIZONTAL, SDL_FLIP_NONE
from sdl2.ext import Renderer, TextureSprite
from typing import Tuple


Rect = Tuple[int, int, int, int]


class BodyPart:
    def __init__(self, source: Rect, dest: Rect, flip: SDL_RendererFlip) -> None:
        self.source = source
        self.dest = dest
        self.flip = flip


class Time:
    def __init__(self):
        self.begin = -1
        self.finish = -1
        self.best = -1


class Player:
    def __init__(self, texture: TextureSprite) -> None:
        self.texture = texture
        self.time = Time()
        self.pos = None  # type: Point2d
        self.vel = None  # type: Vector2d
        self.restart()

    def restart(self):
        self.pos = Point2d(170, 500)
        self.vel = Vector2d(0, 0)
        self.time.begin = -1
        self.time.finish = -1

    def render(self, renderer: Renderer, camera: Vector2d):
        texture = self.texture
        pos = self.pos - camera
        x = int(pos.x)
        y = int(pos.y)

        body_parts = [
            BodyPart((192, 64, 64, 32), (x - 60, y, 96, 48),
                     SDL_FLIP_NONE),  # back feet shadow
            BodyPart((96, 0, 96, 96), (x - 48, y - 48, 96, 96),
                     SDL_FLIP_NONE),  # body shadow
            BodyPart((192, 64, 64, 32), (x - 36, y, 96, 48),
                     SDL_FLIP_NONE),  # front feet shadow
            BodyPart((192, 32, 64, 32), (x - 60, y, 96, 48),
                     SDL_FLIP_NONE),  # back feet
            BodyPart((0, 0, 96, 96), (x - 48, y - 48, 96, 96),
                     SDL_FLIP_NONE),  # body
            BodyPart((192, 32, 64, 32), (x - 36, y, 96, 48),
                     SDL_FLIP_NONE),  # front feet
            BodyPart((64, 96, 32, 32), (x - 18, y - 21, 36, 36),
                     SDL_FLIP_NONE),  # left eye
            BodyPart((64, 96, 32, 32), (x - 6, y - 21, 36, 36),
                     SDL_FLIP_HORIZONTAL)  # right eye
        ]
        for part in body_parts:
            renderer.copy(texture, part.source, part.dest, angle=0,
                          center=None, flip=part.flip)
