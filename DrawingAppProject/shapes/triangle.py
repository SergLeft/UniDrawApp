from PySide6.QtCore import QPointF
from PySide6.QtGui import QPen, QBrush, QPainterPath
from shapes.base import Shape
from PySide6.QtGui import QColor
import math


class Triangle(Shape):
    def __init__(self, p1, p2, p3, fill_color, border_color=None, border_width=1):
        min_x = min(p1[0], p2[0], p3[0])
        min_y = min(p1[1], p2[1], p3[1])
        max_x = max(p1[0], p2[0], p3[0])
        max_y = max(p1[1], p2[1], p3[1])

        width = max_x - min_x
        height = max_y - min_y

        default_green = QColor(0, 255, 0)
        actual_fill = default_green if fill_color is None else fill_color
        actual_border = border_color if border_color is not None else actual_fill

        super().__init__(min_x, min_y, width, height, actual_border, border_width, actual_fill)

        self.points = [p1, p2, p3]
        self.p1, self.p2, self.p3 = p1, p2, p3

    def draw(self, painter):
        pen = QPen(self.border_color, self.border_width)
        brush = QBrush(self.fill_color)
        painter.setPen(pen)
        painter.setBrush(brush)



        path = QPainterPath()
        path.moveTo(self.p1[0], self.p1[1])
        path.lineTo(self.p2[0], self.p2[1])
        path.lineTo(self.p3[0], self.p3[1])
        path.closeSubpath()
        painter.drawPath(path)

    def contains_point(self, x, y):
        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

        point = (x, y)
        d1 = sign(point, self.p1, self.p2)
        d2 = sign(point, self.p2, self.p3)
        d3 = sign(point, self.p3, self.p1)

        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

        return not (has_neg and has_pos)

    def translate(self, dx, dy):
        self.x += dx
        self.y += dy

        self.p1 = (self.p1[0] + dx, self.p1[1] + dy)
        self.p2 = (self.p2[0] + dx, self.p2[1] + dy)
        self.p3 = (self.p3[0] + dx, self.p3[1] + dy)
        self.points = [self.p1, self.p2, self.p3]

    def scale(self, sx, sy):
        center_x = (self.p1[0] + self.p2[0] + self.p3[0]) / 3
        center_y = (self.p1[1] + self.p2[1] + self.p3[1]) / 3

        self.p1 = (center_x + (self.p1[0] - center_x) * sx,
                   center_y + (self.p1[1] - center_y) * sy)
        self.p2 = (center_x + (self.p2[0] - center_x) * sx,
                   center_y + (self.p2[1] - center_y) * sy)
        self.p3 = (center_x + (self.p3[0] - center_x) * sx,
                   center_y + (self.p3[1] - center_y) * sy)
        self.points = [self.p1, self.p2, self.p3]

        min_x = min(self.p1[0], self.p2[0], self.p3[0])
        min_y = min(self.p1[1], self.p2[1], self.p3[1])
        self.x = min_x
        self.y = min_y
        self.width *= sx
        self.height *= sy

    def describeShape(self):
        return [self]