import sys
import sdl2.ext
from time import time
from sdl2 import SDL_RENDERER_ACCELERATED, SDL_RENDERER_PRESENTVSYNC
from sdl2.ext import Color, Renderer, Resources, Window
from basic2d import Point2d, Vector2d
from controller import Input, Controller
from player import Player
from stopwatch import Stopwatch
from tilemap import Map, Tile

FRAMES_PER_SECOND = 50
SECONDS_PER_FRAME = 1.0 / FRAMES_PER_SECOND

# Objective 1: Create the title and size variables
WINDOW_SIZE = (1280, 720)
WINDOW_TITLE = "Our own 2D platformer"


class Game:
    def __init__(self, resources: Resources) -> None:
        self.camera = Vector2d(0, 0)
        # self.camera = Vector2d(self.player.pos.x - WINDOW_SIZE.w / 2, 0)
        self.stopwatch = Stopwatch(resources)

        # Objective 4: Create a Player
        self.player = Player(resources)

        self.map = Map(resources)

    def update(self, controller: Controller) -> None:
        if controller.has_input(Input.RESTART):
            self.stopwatch.reset()

            # Objective 4: Put the player back at the start
            self.player.restart()

        self.player.update(controller, self.map)

        # Objective 8: Call the move_camera function with a focus on the player position
        move_camera(self.camera, self.player.pos)

        # Objective 9: Update the stopwatch according to the player tile
        player_tile = self.map.get_tile(self.player.pos)
        if player_tile == Tile.START:
            self.stopwatch.start()
        elif player_tile == Tile.FINISH:
            self.stopwatch.stop()
        else:
            self.stopwatch.step()

    def render(self, renderer: Renderer) -> None:
        self.player.render(renderer, self.camera)
        self.map.render(renderer, self.camera)
        self.stopwatch.render(renderer)


def move_camera(camera: Vector2d, focus: Point2d) -> None:
    # Objective 8: Find the correct value for half the window width
    win_width, _ = WINDOW_SIZE
    half_win_width = win_width / 2

    # Objective 8: Uncomment and try out the different camera movements
    # 1. always in center:
    # camera.x = focus.x - half_win_width

    # 2. follow once leaves center:
    # left_area = focus.x - half_win_width - 100
    # right_area = focus.x - half_win_width + 100
    # camera.x = min(max(camera.x, left_area), right_area)

    # 3. fluid
    dist = camera.x - focus.x + half_win_width
    camera.x -= 0.05 * dist


def main() -> int:
    sdl2.ext.init()
    resources = Resources(__file__, "resources")
    controller = Controller()

    window = Window(WINDOW_TITLE, size=WINDOW_SIZE)
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
