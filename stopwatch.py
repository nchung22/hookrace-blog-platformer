from sdl2.ext import Color, FontManager, Renderer, Resources
from textbox import TextBox


class Stopwatch:
    def __init__(self, resources: Resources) -> None:
        self.begin = -1
        self.finish = -1
        self.best = -1

        font = FontManager(resources.get_path("DejaVuSans.ttf"), size=28)
        white = Color(r=255, g=255, b=255)
        self.timer_textbox = TextBox(font, 50, 100, white)
        self.best_time_textbox = TextBox(font, 50, 150, white)

    def reset(self) -> None:
        self.begin = -1
        self.finish = -1

    def start(self, tick: int) -> None:
        self.begin = tick

    def stop(self, tick: int) -> None:
        if self.begin >= 0:
            self.finish = tick - self.begin
            self.begin = -1
            if self.best < 0 or self.finish < self.best:
                self.best = self.finish

    def render(self, renderer: Renderer, tick: int) -> None:
        if self.begin >= 0:
            self.timer_textbox.text = format_time_exact(tick - self.begin)
            self.timer_textbox.render(renderer)
        elif self.finish >= 0:
            self.timer_textbox.text = f"Finished in: {format_time_exact(self.finish)}"
            self.timer_textbox.render(renderer)
        if self.best >= 0:
            self.best_time_textbox.text = f"Best time: {format_time_exact(self.best)}"
            self.best_time_textbox.render(renderer)


def format_time(ticks: int) -> str:
    mins = int(int(ticks / 50) / 60)
    secs = int(ticks / 50) % 60
    return f"{mins:02}:{secs:02}"


def format_time_exact(ticks: int) -> str:
    cents = (ticks % 50) * 2
    return f"{format_time(ticks)}:{cents:02}"


