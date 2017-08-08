from sdl2 import SDL_FLIP_NONE
from sdl2.ext import Color, FontManager, Renderer, SpriteFactory, TextureSprite
from typing import Optional


class CacheLine:
    def __init__(self, text: str, texture: TextureSprite, w: int, h: int) -> None:
        self.text = text
        self.texture = texture
        self.w = w
        self.h = h


class TextBox:
    def __init__(self, font: FontManager, x: int, y: int, color: Color) -> None:
        self.text = ""
        self.font = font
        self.x = x
        self.y = y
        self.color = color
        self.cache = None  # type: Optional[CacheLine]

    def render(self, renderer: Renderer):
        if self.cache is None or self.text != self.cache.text:
            # TODO: tc.cache.texture.destroy()
            self.cache = self.create_text_texture(renderer)

        source = (0, 0, self.cache.w, self.cache.h)
        dest = (self.x, self.y, self.cache.w, self.cache.h)
        renderer.copy(self.cache.texture, source, dest, angle=0, center=None, flip=SDL_FLIP_NONE)

    def create_text_texture(self, renderer: Renderer) -> CacheLine:
        surface = self.font.render(self.text, color=self.color)
        # TODO: surface.setSurfaceAlphaMod

        width = surface.w
        height = surface.h
        factory = SpriteFactory(renderer=renderer)
        texture = factory.from_surface(surface, free=True)

        return CacheLine(self.text, texture, width, height)

