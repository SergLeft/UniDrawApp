from PySide6.QtGui import QPen
from shapes.base import Shape
from shapes.triangle import Triangle

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

    def describeShape(self):
        x, y = self.x, self.y
        r = self.radius
        triangles = []

        #make circle out of triangles ca.
        segments = 24
        for i in range(segments):
            angle1 = 2 * math.pi * i / segments
            angle2 = 2 * math.pi * (i + 1) / segments

            p1 = (x, y)
            p2 = (x + r * math.cos(angle1), y + r * math.sin(angle1))
            p3 = (x + r * math.cos(angle2), y + r * math.sin(angle2))

            triangles.append(Triangle(p1, p2, p3, self.fill_color, self.border_color, self.border_width))

        return triangles