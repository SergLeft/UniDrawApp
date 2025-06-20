from PySide6.QtGui import QPen, QPolygonF
from PySide6.QtCore import QPointF
from math import pi, cos, sin
from shapes.base import Shape
from shapes.triangle import Triangle
from operations.subdivision import subdivide_triangles
import math

class Star(Shape):
    def __init__(self, x, y, width, height, border_color, border_width, fill_color):
        super().__init__(x, y, width, height, border_color, border_width, fill_color)

    def draw(self, painter):
        painter.setPen(QPen(self.border_color, self.border_width))
        painter.setBrush(self.fill_color)
        cx = self.x + self.width / 2
        cy = self.y + self.height / 2
        outer_r = min(self.width, self.height) / 2
        inner_r = outer_r / 2.5
        points = []
        for i in range(10):
            angle = pi/2 + i * pi/5
            r = outer_r if i % 2 == 0 else inner_r
            px = cx + r * cos(angle)
            py = cy - r * sin(angle)
            points.append(QPointF(px, py))
        painter.drawPolygon(QPolygonF(points))

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


    def describe_triangles(self, n_subdivisions=0, n_points=5):
        cx = self.x + self.width / 2
        cy = self.y + self.height / 2
        outer_r = min(self.width, self.height) / 2
        inner_r = outer_r / 2.5
        points = []
        for i in range(n_points * 2):
            angle = math.pi / 2 + i * math.pi / n_points
            r = outer_r if i % 2 == 0 else inner_r
            px = cx + r * math.cos(angle)
            py = cy - r * math.sin(angle)
            points.append((px, py))
        tris = [[(cx, cy), points[i], points[(i + 1) % len(points)]] for i in range(len(points))]
        return subdivide_triangles(tris, n_subdivisions)