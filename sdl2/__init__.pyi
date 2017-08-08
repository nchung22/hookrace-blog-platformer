class SDL_RendererFlip: ...
SDL_FLIP_NONE = ...  # type: SDL_RendererFlip
SDL_FLIP_HORIZONTAL = ...  # type: SDL_RendererFlip


class SDL_RendererFlags:
    def __or__(self, other: SDL_RendererFlags) -> SDL_RendererFlags: ...
SDL_RENDERER_ACCELERATED = ...  # type: SDL_RendererFlags
SDL_RENDERER_PRESENTVSYNC = ...  # type: SDL_RendererFlags


class SDL_Surface: ...


class SDL_Keycode: ...
SDLK_SPACE = ...  # type: SDL_Keycode
SDLK_a = ...  # type: SDL_Keycode
SDLK_d = ...  # type: SDL_Keycode
SDLK_q = ...  # type: SDL_Keycode
SDLK_r = ...  # type: SDL_Keycode


class SDL_Keysym:
    @property
    def sym(self) -> SDL_Keycode: ...


class SDL_KeyboardEvent:
    @property
    def keysym(self) -> SDL_Keysym: ...


class SDL_EventType: ...
SDL_KEYDOWN = ...  # type: SDL_EventType
SDL_KEYUP = ...  # type: SDL_EventType
SDL_QUIT = ...  # type: SDL_EventType


class SDL_Event:
    @property
    def type(self) -> SDL_EventType: ...
    @property
    def key(self) -> SDL_KeyboardEvent: ...
