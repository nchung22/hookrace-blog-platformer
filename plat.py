import sys
import sdl2.ext

def main():
    sdl2.ext.init()

    window = sdl2.ext.Window("Our own 2D platformer", size=(1280, 720))
    window.show()

    
    renderer = sdl2.ext.Renderer(window, index=-1,
        flags=sdl2.SDL_RENDERER_ACCELERATED | sdl2.SDL_RENDERER_PRESENTVSYNC
    )

    renderer.color = sdl2.ext.Color(r=110, g=132, b=174)
    renderer.clear()
    renderer.present()

    processor = sdl2.ext.TestEventProcessor()
    processor.run(window)

    sdl2.ext.quit()

main()
