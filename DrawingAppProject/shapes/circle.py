from PySide6.QtGui import QPen
from shapes.base import Shape
from shapes.triangle import Triangle
from operations.subdivision import subdivide_triangles
import math

class Circle(Shape):
    def __init__(self, x, y, width, height, border_color, border_width, fill_color):
        super().__init__(x, y, width, height, border_color, border_width, fill_color)

    def draw(self, painter):
        painter.setPen(QPen(self.border_color, self.border_width))
        painter.setBrush(self.fill_color)
        painter.drawEllipse(self.x, self.y, self.width, self.height)

    def contains_point(self, x, y):
        return (self.x <= x <= self.x + self.width) and (self.y <= y <= self.y + self.height)

    def translate(self, dx, dy):
        self.x += dx
        self.y += dy

    def scale(self, sx, sy):
        self.width *= sx
        self.height *= sy
        self.x *= sx
        self.y *= sy


    def describe_triangles(self, n_subdivisions=0, n_points=24):
        cx, cy = self.x + self.width / 2, self.y + self.height / 2
        r = min(self.width, self.height) / 2
        points = [
            (cx + r * math.cos(2 * math.pi * i / n_points),
             cy + r * math.sin(2 * math.pi * i / n_points))
            for i in range(n_points)
        ]
        tris = [[(cx, cy), points[i], points[(i + 1) % n_points]] for i in range(n_points)]
        return subdivide_triangles(tris, n_subdivisions)