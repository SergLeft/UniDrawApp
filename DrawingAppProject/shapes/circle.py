from PySide6.QtGui import QPen, QColor, QPainter, QPolygonF
from PySide6.QtCore import QPoint, QPointF, QRect
from shapes.base import Shape
from math import pi, cos, sin

class Circle(Shape):
    def __init__(self, x: int, y: int, radius: int, border_color: QColor, border_width: int, fill_color: QColor):
        super().__init__(x, y, fill_color, border_color, border_width)
        self.radius = radius

    def draw(self, painter: QPainter):
        pen = QPen(self.border_color, self.border_width)
        painter.setPen(pen)
        painter.setBrush(self.fill_color)
        painter.drawEllipse(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )

    def contains_point(self, point: QPoint):
        return (
            self.x - self.radius <= point.x() <= self.x + self.radius and
            self.y - self.radius <= point.y() <= self.y + self.radius
        )

    def translate(self, dx, dy):
        self.x += dx
        self.y += dy

    def scale(self, sx, sy):
        self.radius = int(self.radius * max(sx, sy))
        self.x = int(self.x * sx)
        self.y = int(self.y * sy)