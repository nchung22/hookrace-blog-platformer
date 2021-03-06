import sys
import sdl2.ext
from time import time
from sdl2.ext import Color, Renderer, Resources, Window
from basic2d import Point2d, Vector2d
from controller import Input, Controller
from stopwatch import Stopwatch

# Objective 4: Import Player from player module

from player import Player
# Objective 5: Import Map and Tile from tilemap module

from tilemap import Map, Tile

UPDATES_PER_SECOND = 50
SECONDS_PER_UPDATE = 1.0 / UPDATES_PER_SECOND

# Objective 1: Create the title and size variables
# YOUR CODE HERE...
WINDOW_SIZE = (10000,6000)
WINDOW_TITLE = "Timed Run"


class Game:
    def __init__(self, resources: Resources) -> None:
        self.camera = Vector2d(0, 0)
        self.stopwatch = Stopwatch(resources)

        # Objective 4: Create a Player

        self.player = Player(resources)
        # Objective 5: Create a Map

        self.map = Map(resources)

    def update(self, controller: Controller) -> None:
        if controller.has_input(Input.RESTART):
            self.stopwatch.reset()

            # Objective 4: Put the player back at the start

            self.player.restart()
        # Objective 6: Call the player update method
        # YOUR CODE HERE...
        self.player.update(controller, self.map)

        # Objective 7: Call the move_camera function with a focus on the player position
        # YOUR CODE HERE...
        move_camera(self.camera, self.player.pos)

        # Objective 8: Update the stopwatch according to the player tile
        # YOUR CODE HERE...
        value = self.map.get_tile(self.player.pos)
        if value == Tile.START:
            self.stopwatch.start()
        elif value == Tile.FINISH:
            self.stopwatch.stop()
        else:
            self.stopwatch.step()



    def render(self, renderer: Renderer) -> None:
        # Objective 4: Render the player
        # YOUR CODE HERE...
        self.player.render(renderer, self.camera)
        # Objective 5: Render the tilemap
        # YOUR CODE HERE...
        self.map.render(renderer, self.camera)

        self.stopwatch.render(renderer)


def move_camera(camera: Vector2d, focus: Point2d) -> None:
    # Objective 7: Find the correct value for half the window width
    # YOUR CODE HERE...
    half_win_width = 500

    # Objective 7: Uncomment and try out the different camera movements

    #1. always in center:
    camera.x = focus.x - half_win_width

    # 2. follow once leaves center:
    #left_area = focus.x - half_win_width - 100
    #right_area = focus.x - half_win_width + 100
    #camera.x = min(max(camera.x, left_area), right_area)

    # 3. fluid
    # dist = camera.x - focus.x + half_win_width
    # camera.x -= 0.05 * dist


def main() -> int:
    sdl2.ext.init()
    resources = Resources(__file__, "resources")
    controller = Controller()

    # Objective 1: Create and show the Window
    # YOUR CODE HERE...
    window = Window(WINDOW_TITLE, WINDOW_SIZE)
    window.show()

    # Objective 2: Create the Renderer with a background color
    # YOUR CODE HERE...
    renderer = Renderer(window)
    color = Color(110, 132, 174)
    renderer.color = color

    # Objective 3: Set up the game
    # YOUR CODE HERE...
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

        # Objective 3: Update the game the appropriate number of frames
        # YOUR CODE HERE...
        while lag >= SECONDS_PER_UPDATE:
            game.update(controller)
            lag -= SECONDS_PER_UPDATE

        # Objective 2: Draw over all drawings of the last frame with the default color
        # YOUR CODE HERE...
        renderer.clear()

        # Objective 3: Render the game
        # YOUR CODE HERE...
        game.render(renderer)
        # Objective 2: Show the result on screen
        # YOUR CODE HERE...
        renderer.present()
    sdl2.ext.quit()
    return 0


if __name__ == "__main__":
    sys.exit(main())
