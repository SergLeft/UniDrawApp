from shapes.base import Shape
from shapes.rectangle import Rectangle
from shapes.circle import Circle
from shapes.star import Star
from math import pi, cos, sin
from PySide6.QtGui import QColor

class Scene:
    def __init__(self, canvas_width=800, canvas_height=600):
        self.shapes = []
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.center_x = canvas_width // 2
        self.center_y = canvas_height // 2

        self.view_x = 0 #View offset for X
        self.view_y = 0 #View offset for Y
        self.zoom = 1.0 #Zoom factor

    def add_shape(self, shape):
        self.shapes.append(shape)

    def get_max_x(self):
        return max((shape.x + getattr(shape, 'width', getattr(shape, 'size', 0)) for shape in self.shapes), default=self.canvas_width)

    def get_max_y(self):
        return max((shape.y + getattr(shape, 'height', getattr(shape, 'size', 0)) for shape in self.shapes), default=self.canvas_height)

    def generate_test_scene(self, scene_id: int):
        """Generiert vordefinierte Test-Szenen mit automatischer Zentrierung."""
        self.shapes.clear()

        if scene_id == 1:
            self.add_shape(Rectangle(self.center_x - 50, self.center_y - 50, 100, 200, QColor(255, 255, 255, 0), QColor(0, 0, 255)))
            self.add_shape(Circle(self.center_x - 100, self.center_y - 100, 100, QColor(0, 255, 0, 0), QColor(255, 0, 0)))

        elif scene_id == 2:
            self.add_shape(Rectangle(self.center_x - 200, self.center_y - 125, 200, 200, QColor(0, 0, 255), QColor(0, 0, 255)))
            self.add_shape(Rectangle(self.center_x, self.center_y - 125, 200, 200, QColor(0, 0, 255), QColor(0, 0, 255)))

            self.add_shape(Rectangle(self.center_x - 200, self.center_y + 175, 200, 200, QColor(0, 0, 255), QColor(0, 0, 255)))
            self.add_shape(Rectangle(self.center_x, self.center_y + 175, 200, 200, QColor(0, 0, 255), QColor(0, 0, 255)))

            self.add_shape(Circle(self.center_x - 100, self.center_y - 125, 64, QColor(255, 0, 0), QColor(255, 0, 0)))
            self.add_shape(Circle(self.center_x - 100, self.center_y + 175, 64, QColor(255, 0, 0), QColor(255, 0, 0)))

            self.add_shape(Circle(self.center_x + 100, self.center_y - 125, 64, QColor(255, 0, 0), QColor(255, 0, 0)))
            self.add_shape(Circle(self.center_x + 100, self.center_y + 175, 64, QColor(255, 0, 0), QColor(255, 0, 0)))

        elif scene_id == 3:
            star_size = 50
            star_x = self.center_x
            star_y = self.center_y
            self.add_shape(Star(star_x, star_y, star_size, 5, QColor(255, 255, 0), QColor(255, 0, 0)))

        else:
            print(f"Warnung: Szenen-ID {scene_id} ist ungültig.")
