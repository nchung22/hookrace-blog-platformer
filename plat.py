import sys
import sdl2.ext
from time import time
from copy import copy
from sdl2 import SDL_RENDERER_ACCELERATED, SDL_RENDERER_PRESENTVSYNC
from sdl2.ext import Color, Renderer, Resources, Window
from basic2d import Vector2d
from controller import Input, Controller
from player import Player
from stopwatch import Stopwatch
from tilemap import Map, Tile


WINDOW_SIZE = (1280, 720)


class Game:
    def __init__(self, resources: Resources) -> None:
        self.controller = Controller()
        self.player = Player(resources)
        self.map = Map(resources)
        self.camera = Vector2d(0, 0)
        # self.camera = Vector2d(self.player.pos.x - WINDOW_SIZE.w / 2, 0)
        self.stopwatch = Stopwatch(resources)

    def physics(self) -> None:
        ground = self.player.on_ground(self.map)
        new_vel = copy(self.player.vel)

        # new y velocity...
        if self.controller.has_input(Input.JUMP):
            if ground:
                new_vel.y = -21
        new_vel.y += 0.75  # gravity

        # new x velocity...
        direction = self.controller.direction
        if ground:
            new_vel.x = 0.5 * new_vel.x + 4.0 * direction
        else:
            new_vel.x = 0.95 * new_vel.x + 2.0 * direction
        new_vel.x = min(max(new_vel.x, -8), 8)

        self.player.update_position(self.map, new_vel)

    def move_camera(self) -> None:
        win_width, _ = WINDOW_SIZE
        half_win_width = win_width / 2
        # 1. always in center:
        # self.camera.x = self.player.pos.x - half_win_width
        # 2. follow once leaves center:
        left_area = self.player.pos.x - half_win_width - 100
        right_area = self.player.pos.x - half_win_width + 100
        # self.camera.x = min(max(self.camera.x, left_area), right_area)
        # 3. fluid
        dist = self.camera.x - self.player.pos.x + half_win_width
        self.camera.x -= 0.05 * dist

    def logic(self, tick: int) -> None:
        player_tile = self.map.get_tile(self.player.pos)
        if player_tile == Tile.START:
            self.stopwatch.start(tick)
        elif player_tile == Tile.FINISH:
            self.stopwatch.stop(tick)

    def update(self, tick: int) -> None:
        if self.controller.has_input(Input.RESTART):
            self.player.restart()
            self.stopwatch.reset()

        self.physics()
        self.move_camera()
        self.logic(tick)

    def render(self, renderer: Renderer, tick: int) -> None:
        # Draw over all drawings of the last frame with the default color
        renderer.clear()

        # Actual drawing here
        self.player.render(renderer, self.camera)
        self.map.render(renderer, self.camera)
        self.stopwatch.render(renderer, tick)

        # Show the result on screen
        renderer.present()


def main() -> int:
    sdl2.ext.init()

    window = Window("Our own 2D platformer", size=WINDOW_SIZE)
    window.show()

    renderer = Renderer(
        window,
        index=-1,
        flags=SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC
    )

    renderer.color = Color(r=110, g=132, b=174)

    resources = Resources(__file__, "resources")
    game = Game(resources)

    start_time = time()
    last_tick = 0
    # Game loop, draws each frame
    while not game.controller.has_input(Input.QUIT):
        game.controller.handle_input()

        new_tick = int((time() - start_time) * 50)
        for tick in range(last_tick + 1, new_tick + 1):
            game.update(tick)
        last_tick = new_tick

        game.render(renderer, last_tick)

    sdl2.ext.quit()
    return 0


if __name__ == "__main__":
    sys.exit(main())
