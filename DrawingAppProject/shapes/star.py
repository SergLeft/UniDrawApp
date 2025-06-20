from PySide6.QtGui import QPen, QPolygonF
from PySide6.QtCore import QPointF
from math import pi, cos, sin
from shapes.base import Shape
from shapes.triangle import Triangle

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

    def describeShape(self):
        x, y = self.x, self.y
        outer_r = self.radius
        inner_r = self.radius * 0.4
        points = 5
        triangles = []

        for i in range(points * 2):
            angle1 = math.pi / 2 + 2 * math.pi * i / (points * 2)
            angle2 = math.pi / 2 + 2 * math.pi * (i + 1) / (points * 2)

            radius1 = outer_r if i % 2 == 0 else inner_r
            radius2 = outer_r if (i + 1) % 2 == 0 else inner_r

            p1 = (x, y)
            p2 = (x + radius1 * math.cos(angle1), y + radius1 * math.sin(angle1))
            p3 = (x + radius2 * math.cos(angle2), y + radius2 * math.sin(angle2))

            triangles.append(Triangle(p1, p2, p3, self.fill_color, self.border_color, self.border_width))

        return triangles