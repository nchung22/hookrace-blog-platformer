from math import sqrt


class Point2d:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __sub__(self, other):
        return Point2d(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Point2d(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar: float):
        return Point2d(self.x * scalar, self.y * scalar)

    def len(self):
        return sqrt(self.x * self.x + self.y * self.y)


Vector2d = Point2d
