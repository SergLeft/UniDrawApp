from PySide6.QtGui import QPen, QPolygonF
from PySide6.QtCore import QRect, QPointF
from shapes.base import Shape
from math import pi, cos, sin

class Rectangle(Shape):
    def __init__(self, x, y, width, height, fill_color, border_color, border_width=1):
        super().__init__(x, y, fill_color, border_color, border_width)
        self.width = width
        self.height = height

    def draw(self, painter):
        painter.setPen(QPen(self.border_color, self.border_width))
        painter.setBrush(self.fill_color)
        painter.drawRect(QRect(self.x, self.y, self.width, self.height))

    def contains_point(self, point):
        return(self.x <= point.x() <= self.x + self.width and
               self.y <= point.y() <= self.y + self.height)

    def translate(self, dx, dy):
        self.x += dx
        self.y += dy

    def scale(self, sx, sy):
        self.width *= sx
        self.height *= sy
        self.x *= sx
        self.y *= sy
