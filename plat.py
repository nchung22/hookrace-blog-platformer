import sys
import sdl2.ext
from time import time
from enum import Enum
from sdl2 import SDL_FLIP_NONE, SDL_KEYDOWN, SDL_KEYUP, SDL_QUIT,\
    SDL_RENDERER_ACCELERATED, SDL_RENDERER_PRESENTVSYNC, SDLK_SPACE, SDLK_a, SDLK_d, SDLK_q, SDLK_r
from sdl2.ext import Color, FontManager, Renderer, Resources, SpriteFactory, TextureSprite, Window
from basic2d import Vector2d
from player import Player
from tilemap import Map, Tile


class Input(Enum):
    NONE = 1
    LEFT = 2
    RIGHT = 3
    JUMP = 4
    RESTART = 5
    QUIT = 6


class CacheLine:
    def __init__(self, texture: TextureSprite, w: int, h: int) -> None:
        self.texture = texture
        self.w = w
        self.h = h


class TextCache:
    def __init__(self):
        self.text = ""
        self.cache = None  # type: CacheLine


PLAYER_SIZE = Vector2d(64, 64)
WINDOW_SIZE = (1280, 720)


class Game:
    def __init__(self, renderer: Renderer) -> None:
        self.renderer = renderer

        self.inputs = {
            Input.NONE: False,
            Input.LEFT: False,
            Input.RIGHT: False,
            Input.JUMP: False,
            Input.RESTART: False,
            Input.QUIT: False
        }

        # load resources
        resources = Resources(__file__, "resources")
        self.font = FontManager(resources.get_path("DejaVuSans.ttf"), size=28)
        factory = SpriteFactory(renderer=renderer)
        self.player = Player(factory.from_image(resources.get_path("player.png")))
        self.map = Map(factory.from_image(resources.get_path("grass.png")),
                       resources.get_path("default.map"))
        self.camera = Vector2d(0, 0)
        # self.camera.x = self.player.pos.x - WINDOW_SIZE.w / 2
        self.tc_timer = TextCache()
        self.tc_best_time = TextCache()

    def handle_input(self) -> None:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == SDL_QUIT:
                self.inputs[Input.QUIT] = True
            elif event.type == SDL_KEYDOWN:
                self.inputs[to_input(event.key.keysym.sym)] = True
            elif event.type == SDL_KEYUP:
                self.inputs[to_input(event.key.keysym.sym)] = False

    def physics(self) -> None:
        if self.inputs[Input.RESTART]:
            self.player.restart()

        ground = self.map.on_ground(self.player.pos, PLAYER_SIZE)

        if self.inputs[Input.JUMP]:
            if ground:
                self.player.vel.y = -21

        direction = ((1 if self.inputs[Input.RIGHT] else 0)
                     - (1 if self.inputs[Input.LEFT] else 0))

        self.player.vel.y += 0.75  # gravity
        if ground:
            self.player.vel.x = 0.5 * self.player.vel.x + 4.0 * direction
        else:
            self.player.vel.x = 0.95 * self.player.vel.x + 2.0 * direction
        self.player.vel.x = min(max(self.player.vel.x, -8), 8)

        self.player.pos, self.player.vel = self.map.move_box(
            self.player.pos, self.player.vel, PLAYER_SIZE
        )

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
        player_time = self.player.time
        player_tile = self.map.get_tile(self.player.pos)
        if player_tile == Tile.START:
            player_time.begin = tick
        elif player_tile == Tile.FINISH:
            if player_time.begin >= 0:
                player_time.finish = tick - player_time.begin
                player_time.begin = -1
                if player_time.best < 0 or player_time.finish < player_time.best:
                    player_time.best = player_time.finish

    def __render_text(self, text: str, x: int, y: int, color: Color, tc: TextCache):
        if text != tc.text:
            # TODO: tc.cache.texture.destroy()
            tc.cache = render_text(self.renderer, self.font, text, color)
            tc.text = text

        source = (0, 0, tc.cache.w, tc.cache.h)
        dest = (x, y, tc.cache.w, tc.cache.h)
        self.renderer.copy(tc.cache.texture, source, dest, angle=0, center=None, flip=SDL_FLIP_NONE)

    def render(self, tick: int) -> None:
        # Draw over all drawings of the last frame with the default color
        self.renderer.clear()

        # Actual drawing here
        self.player.render(self.renderer, self.camera)
        self.map.render(self.renderer, self.camera)

        player_time = self.player.time
        white = Color(r=255, g=255, b=255)
        if player_time.begin >= 0:
            self.__render_text(format_time_exact(tick - player_time.begin), 50, 100, white, self.tc_timer)
        elif player_time.finish >= 0:
            self.__render_text("Finished in: " + format_time_exact(player_time.finish), 50, 100, white, self.tc_timer)
        if player_time.best >= 0:
            self.__render_text("Best time: " + format_time_exact(player_time.best), 50, 150, white, self.tc_best_time)

        # Show the result on screen
        self.renderer.present()


def format_time(ticks: int) -> str:
    mins = int(int(ticks / 50) / 60)
    secs = int(ticks / 50) % 60
    return f"{mins:02}:{secs:02}"


def format_time_exact(ticks: int) -> str:
    cents = (ticks % 50) * 2
    return f"{format_time(ticks)}:{cents:02}"


def render_text(
        renderer: Renderer, font: FontManager,
        text: str, color: Color) -> CacheLine:
    surface = font.render(text, color=color)
    # TODO: surface.setSurfaceAlphaMod

    width = surface.w
    height = surface.h
    factory = SpriteFactory(renderer=renderer)
    texture = factory.from_surface(surface, free=True)

    return CacheLine(texture, width, height)


def to_input(key):
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

    game = Game(renderer)

    start_time = time()
    last_tick = 0
    # Game loop, draws each frame
    while not game.inputs[Input.QUIT]:
        game.handle_input()

        new_tick = int((time() - start_time) * 50)
        for tick in range(last_tick + 1, new_tick + 1):
            game.physics()
            game.move_camera()
            game.logic(tick)
        last_tick = new_tick

        game.render(last_tick)

    sdl2.ext.quit()
    return 0


if __name__ == "__main__":
    sys.exit(main())
