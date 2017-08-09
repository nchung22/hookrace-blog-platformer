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

FRAMES_PER_SECOND = 50
SECONDS_PER_FRAME = 1.0 / FRAMES_PER_SECOND
WINDOW_SIZE = (1280, 720)


class Game:
    def __init__(self, resources: Resources) -> None:
        self.player = Player(resources)
        self.map = Map(resources)
        self.camera = Vector2d(0, 0)
        # self.camera = Vector2d(self.player.pos.x - WINDOW_SIZE.w / 2, 0)
        self.stopwatch = Stopwatch(resources)

    def physics(self, controller: Controller) -> None:
        ground = self.player.on_ground(self.map)
        new_vel = copy(self.player.vel)

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

    def logic(self) -> None:
        player_tile = self.map.get_tile(self.player.pos)
        if player_tile == Tile.START:
            self.stopwatch.start()
        elif player_tile == Tile.FINISH:
            self.stopwatch.stop()
        else:
            self.stopwatch.step()

    def update(self, controller: Controller) -> None:
        if controller.has_input(Input.RESTART):
            self.player.restart()
            self.stopwatch.reset()

        self.physics(controller)
        self.move_camera()
        self.logic()

    def render(self, renderer: Renderer) -> None:
        self.player.render(renderer, self.camera)
        self.map.render(renderer, self.camera)
        self.stopwatch.render(renderer)


def main() -> int:
    sdl2.ext.init()
    resources = Resources(__file__, "resources")
    controller = Controller()

    window = Window("Our own 2D platformer", size=WINDOW_SIZE)
    window.show()

    renderer = Renderer(
        window,
        index=-1,
        flags=SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC
    )

    renderer.color = Color(r=110, g=132, b=174)

    game = Game(resources)

    # Game Loop, draws each frame
    last_time = time()
    lag = 0.0
    while True:
        now = time()
        lag += now - last_time
        last_time = now

        controller.handle_input()
        if controller.has_input(Input.QUIT):
            break

        while lag >= SECONDS_PER_FRAME:
            game.update(controller)
            lag -= SECONDS_PER_FRAME

        renderer.clear()
        game.render(renderer)
        renderer.present()

    sdl2.ext.quit()
    return 0


if __name__ == "__main__":
    sys.exit(main())
