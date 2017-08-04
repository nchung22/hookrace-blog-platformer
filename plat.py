import sys
import sdl2.ext
from enum import Enum, auto
from sdl2 import SDL_FLIP_NONE, SDL_FLIP_HORIZONTAL
from collections import namedtuple

RESOURCES = sdl2.ext.Resources(__file__, "resources")


Rect = namedtuple('Rect', ['x', 'y', 'w', 'h'])


BodyPart = namedtuple('BodyPart', ['source', 'dest', 'flip'])


class Point2d:
    x: int
    y: int

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, other):
        return Point2d(self.x - other.x, self.y - other.y)


class Input(Enum):
    NONE = auto()
    LEFT = auto()
    RIGHT = auto()
    JUMP = auto()
    RESTART = auto()
    QUIT = auto()


class Player:
    texture: sdl2.ext.TextureSprite
    pos = Point2d(0, 0)
    vel = Point2d(0, 0)

    def __init__(self, texture: sdl2.ext.TextureSprite) -> None:
        self.texture = texture
        self.restart()

    def restart(self):
        self.pos = Point2d(170, 500)
        self.vel = Point2d(0, 0)


class Map:
    texture: sdl2.ext.TextureSprite
    width: int
    height: int
    tiles = []

    def __init__(self, texture: sdl2.ext.TextureSprite, file_name: str) -> None:
        self.texture = texture
        self.tiles = []
        self.width = 0
        self.height = 0

        file = open(file_name, "r")
        for line in file.readlines():
            width = 0
            for word in line.split(' '):
                if word == "":
                    continue
                value = int(word)
                self.tiles.append(value)
                width += 1

            if self.width > 0 and self.width != width:
                raise "Incompatible line length in map" + file_name
            self.width = width
            self.height += 1


class Game:
    inputs = {
        Input.NONE: False,
        Input.LEFT: False,
        Input.RIGHT: False,
        Input.JUMP: False,
        Input.RESTART: False,
        Input.QUIT: False
    }
    renderer: sdl2.ext.Renderer
    player: Player
    camera: Point2d

    def __init__(self, renderer: sdl2.ext.Renderer) -> None:
        self.renderer = renderer
        factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer)
        self.player = Player(factory.from_image(RESOURCES.get_path("player.png")))
        self.map = Map(factory.from_image(RESOURCES.get_path("grass.png")),
                       RESOURCES.get_path("default.map"))
        self.camera = Point2d(0, 0)

    def handle_input(self) -> None:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                self.inputs[Input.QUIT] = True
            elif event.type == sdl2.SDL_KEYDOWN:
                self.inputs[to_input(event.key.keysym.sym)] = True
            elif event.type == sdl2.SDL_KEYUP:
                self.inputs[to_input(event.key.keysym.sym)] = False

    def render(self) -> None:
        # Draw over all drawings of the last frame with the default color
        self.renderer.clear()
        # Actual drawing here
        render_tee(
            self.renderer,
            self.player.texture,
            self.player.pos - self.camera
        )
        # Show the result on screen
        self.renderer.present()


def render_tee(renderer: sdl2.ext.Renderer, texture: sdl2.ext.TextureSprite,
               pos: Point2d):
    x = pos.x
    y = pos.y

    body_parts = [
        BodyPart(Rect(192, 64, 64, 32), Rect(x - 60, y, 96, 48),
                 SDL_FLIP_NONE),  # back feet shadow
        BodyPart(Rect(96, 0, 96, 96), Rect(x - 48, y - 48, 96, 96),
                 SDL_FLIP_NONE),  # body shadow
        BodyPart(Rect(192, 64, 64, 32), Rect(x - 36, y, 96, 48),
                 SDL_FLIP_NONE),  # front feet shadow
        BodyPart(Rect(192, 32, 64, 32), Rect(x - 60, y, 96, 48),
                 SDL_FLIP_NONE),  # back feet
        BodyPart(Rect(0, 0, 96, 96), Rect(x - 48, y - 48, 96, 96),
                 SDL_FLIP_NONE),  # body
        BodyPart(Rect(192, 32, 64, 32), Rect(x - 36, y, 96, 48),
                 SDL_FLIP_NONE),  # front feet
        BodyPart(Rect(64, 96, 32, 32), Rect(x - 18, y - 21, 36, 36),
                 SDL_FLIP_NONE),  # left eye
        BodyPart(Rect(64, 96, 32, 32), Rect(x - 6, y - 21, 36, 36),
                 SDL_FLIP_HORIZONTAL)  # right eye
    ]
    for part in body_parts:
        renderer.copy(texture, part.source, part.dest, angle=0.0,
                      center=None, flip=part.flip)


def to_input(key):
    if key == sdl2.SDLK_a:
        return Input.LEFT
    elif key == sdl2.SDLK_d:
        return Input.RIGHT
    elif key == sdl2.SDLK_SPACE:
        return Input.JUMP
    elif key == sdl2.SDLK_r:
        return Input.RESTART
    elif key == sdl2.SDLK_q:
        return Input.QUIT
    else:
        return Input.NONE


def main() -> int:
    sdl2.ext.init()

    window = sdl2.ext.Window("Our own 2D platformer", size=(1280, 720))
    window.show()

    renderer = sdl2.ext.Renderer(
        window,
        index=-1,
        flags=sdl2.SDL_RENDERER_ACCELERATED | sdl2.SDL_RENDERER_PRESENTVSYNC
    )

    renderer.color = sdl2.ext.Color(r=110, g=132, b=174)

    game = Game(renderer)

    # Game loop, draws each frame
    while not game.inputs[Input.QUIT]:
        game.handle_input()
        game.render()

    sdl2.ext.quit()
    return 0


if __name__ == "__main__":
    sys.exit(main())
