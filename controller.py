from enum import Enum, IntEnum
from sdl2 import SDL_Keycode, SDL_KEYDOWN, SDL_KEYUP, SDL_QUIT, \
    SDLK_SPACE, SDLK_a, SDLK_d, SDLK_q, SDLK_r
from sdl2.ext import get_events


class Input(Enum):
    NONE = 1
    LEFT = 2
    RIGHT = 3
    JUMP = 4
    RESTART = 5
    QUIT = 6


class Direction(IntEnum):
    LEFT = -1
    NONE = 0
    RIGHT = 1


class Controller:
    inputs = {
        Input.NONE: False,
        Input.LEFT: False,
        Input.RIGHT: False,
        Input.JUMP: False,
        Input.RESTART: False,
        Input.QUIT: False
    }

    def handle_input(self) -> None:
        events = get_events()
        for event in events:
            if event.type == SDL_QUIT:
                self.inputs[Input.QUIT] = True
            elif event.type == SDL_KEYDOWN:
                self.inputs[to_input(event.key.keysym.sym)] = True
            elif event.type == SDL_KEYUP:
                self.inputs[to_input(event.key.keysym.sym)] = False

    @property
    def direction(self) -> Direction:
        return Direction((1 if self.inputs[Input.RIGHT] else 0)
                         - (1 if self.inputs[Input.LEFT] else 0))

    def has_input(self, input: Input) -> bool:
        return self.inputs[input]


def to_input(key: SDL_Keycode) -> Input:
    if key == SDLK_a:
        return Input.LEFT
    elif key == SDLK_d:
        return Input.RIGHT
    elif key == SDLK_SPACE:
        return Input.JUMP
    elif key == SDLK_r:
        return Input.RESTART
    elif key == SDLK_q:
        return Input.QUIT
    else:
        return Input.NONE
