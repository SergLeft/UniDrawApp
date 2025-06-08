from PySide6.QtGui import QPen, QColor, QPainter, QPolygon
from PySide6.QtCore import QPoint, QPointF, QRect
from math import pi, cos, sin
from shapes.base import Shape

class Star(Shape):
    def __init__(self, x: int, y: int, size: int, points: int, border_color: QColor, border_width: int, fill_color: QColor):
        super().__init__(x, y, fill_color, border_color, border_width)
        self.size = size
        self.points = points
        self.x = x - size // 2
        self.y = y - size // 2

    def draw(self, painter: QPainter):
        pen = QPen(self.border_color, self.border_width)
        painter.setPen(pen)
        painter.setBrush(self.fill_color)
        polygon = []
        for i in range(self.points * 2):
            radius = self.size if i % 2 == 0 else self.size / 2
            angle = (i / (self.points * 2)) * 2 * pi + pi / self.points
            px = self.x + int(radius * cos(angle))
            py = self.y + int(radius * sin(angle))
            polygon.append(QPoint(px, py))
        painter.drawPolygon(QPolygon(polygon))

    def contains_point(self, point):
        return (
            self.x - self.size <= point.x() <= self.x + self.size and
            self.y - self.size <= point.y() <= self.y + self.size
        )

    def translate(self, dx, dy):
        self.x += dx
        self.y += dy

    def scale(self, sx, sy):
        self.size = int(self.size * max(sx, sy))
        self.x = int(self.x * sx)
        self.y = int(self.y * sy)