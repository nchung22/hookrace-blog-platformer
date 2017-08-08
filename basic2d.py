from math import sqrt


class Vector2d:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    @property
    def norm(self):
        return sqrt(self.x * self.x + self.y * self.y)

    def __mul__(self, scalar: float):
        return Vector2d(self.x * scalar, self.y * scalar)

    def __copy__(self):
        return Vector2d(self.x, self.y)


class Point2d:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __sub__(self, other: Vector2d):
        return Point2d(self.x - other.x, self.y - other.y)

    def __add__(self, other: Vector2d):
        return Point2d(self.x + other.x, self.y + other.y)

