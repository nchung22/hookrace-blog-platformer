from basic2d import Point2d, Vector2d
from controller import Controller, Input
from copy import copy
from sdl2 import SDL_FLIP_HORIZONTAL, SDL_FLIP_NONE
from sdl2.ext import Renderer, Resources, SpriteFactory, TextureSprite
from tilemap import Map
from typing import Optional


PLAYER_SIZE = Vector2d(64, 64)
INITIAL_POS = Point2d(170, 500)
ZERO_VEL = Vector2d(0, 0)


class Player:
    def __init__(self, resources: Resources) -> None:
        self.texture = None
        self.texture_path = resources.get_path("player.png")
        self.pos = copy(INITIAL_POS)
        self.vel = copy(ZERO_VEL)
        self.restart()

    def restart(self) -> None:
        self.pos = copy(INITIAL_POS)
        self.vel = copy(ZERO_VEL)

    def update(self, controller: Controller, tilemap: Map) -> None:
        ground = tilemap.on_ground(self.pos, PLAYER_SIZE)
        new_vel = copy(self.vel)

        # new y velocity...
        if controller.has_input(Input.JUMP):
            if ground:
                new_vel.y = -21
        new_vel.y += 0.75  # gravity

        # new x velocity...
        direction = float(controller.direction)
        if ground:
            new_vel.x = 0.5 * new_vel.x + 4.0 * direction
        else:
            new_vel.x = 0.95 * new_vel.x + 2.0 * direction
        new_vel.x = min(max(new_vel.x, -8), 8)

        # Objective 6: Use the tilemap to shift the player position by velocity
        # YOUR CODE HERE...
        self.pos, self.vel = tilemap.move_box(self.pos, new_vel, PLAYER_SIZE)
        self.pos.x = int(self.pos.x)
        self.pos.y = int(self.pos.y)

    def render(self, renderer: Renderer, camera: Vector2d) -> None:
        if self.texture is None:
            factory = SpriteFactory(renderer=renderer)
            self.texture = factory.from_image(self.texture_path)
        texture = self.texture  # type: TextureSprite

        # Objective 4: Use the camera and player position to find the screen position
        #             |--1--2--3--4--| <-- x-axis screen (int)
        #             |     *        | <-- player
        # 0--1--2--3--|--5--6--7--8--| <-- x-axis world (float)
        #             ^                <-- camera
        # YOUR CODE HERE...
        pos = self.pos - camera
        x = int(pos.x)
        y = int(pos.y)

        # We need to cut up the player sheet into an array of tuples
        # The upper left is (0, 0). The total size is 256x128.
        #
        # If you divide the sections into 32x32 squares it looks like:
        #
        # |a a a|b b b|-|-|  a = body
        # |a a a|b b b|c c|  b = body shadow
        # |a a a|b b b|d d|  c = foot
        # |   |e|-|-|-|-|-|  d = foot shadow
        #                    e = basic eye (left)
        #
        # We take the pieces and overlay them on top of each other:
        #                           ( dx,  dy,   w,  h)
        # 1. foot shadow (back)  -> (-60,   0,  96, 48) <-- 3/2 scale
        # 2. foot (back)         -> (-60,   0,  96, 48) <-- 3/2 scale
        # 3. body shadow         -> (-48, -48,  96, 96)
        # 4. body                -> (-48, -48,  96, 96)
        # 5. foot shadow (front) -> (-36,   0,  96, 48) <-- 3/2 scale
        # 6. foot (front)        -> (-36,   0,  96, 48) <-- 3/2 scale
        # 7. basic eye (left)    -> (-18, -21,  36, 36) <-- 9/8 scale
        # 8. basic eye (right)   -> ( -6, -21,  36, 36) <-- 9/8 scale *FLIPPED*
        body_parts = [
            ((192, 64, 64, 32), (x - 60, y, 96, 48), SDL_FLIP_NONE),
            ((192, 32, 64, 32), (x - 60, y, 96, 48), SDL_FLIP_NONE),
            ((96, 0, 96, 96), (x - 48, y - 48, 96, 96), SDL_FLIP_NONE),
            ((0, 0, 96, 96), (x - 48, y - 48, 96, 96), SDL_FLIP_NONE),
            ((192, 64, 64, 32), (x - 36, y, 96, 48), SDL_FLIP_NONE),
            ((192, 32, 64, 32), (x - 36, y, 96, 48), SDL_FLIP_NONE),
            ((64, 96, 32, 32), (x - 18, y - 21, 36, 36), SDL_FLIP_NONE),
            ((64, 96, 32, 32), (x - 6, y - 21, 36, 36), SDL_FLIP_HORIZONTAL)
        ]

        # Objective 4: Iterate over the body parts and render each one
        # YOUR CODE HERE...
        for source, destination, flip in body_parts:
            renderer.copy(texture, source, destination, flip=flip)


