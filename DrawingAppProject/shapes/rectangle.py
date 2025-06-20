from PySide6.QtGui import QPen
from shapes.base import Shape
from shapes.triangle import Triangle
from PySide6.QtGui import QColor
from operations.subdivision import subdivide_triangles


class Rectangle(Shape):
    def __init__(self, x, y, width, height, border_color, border_width, fill_color):
        super().__init__(x, y, width, height, border_color, border_width, fill_color)
        self.width = width
        self.height = height

    def draw(self, painter):
        painter.setPen(QPen(self.border_color, self.border_width))
        painter.setBrush(self.fill_color)

        painter.drawRect(self.x, self.y, self.width, self.height)

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


    def describe_triangles(self, n_subdivisions=0):
        p1 = (self.x, self.y)
        p2 = (self.x + self.width, self.y)
        p3 = (self.x + self.width, self.y + self.height)
        p4 = (self.x, self.y + self.height)
        tris = [[p1, p2, p3], [p1, p3, p4]]
        return subdivide_triangles(tris, n_subdivisions)