from shapes.rectangle import Rectangle
from shapes.circle import Circle
from shapes.star import Star
from PySide6.QtGui import QColor
from operations.deformation import deform_triangles
import math

class Scene:
    def __init__(self, canvas_width=800, canvas_height=600):
        self.shapes = []
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.center_x = canvas_width // 2
        self.center_y = canvas_height // 2

        self.view_x = 0  # View offset for X
        self.view_y = 0  # View offset for Y
        self.zoom = 1.0  # Zoom factor

    def add_shape(self, shape):
        if shape is not None:
            self.shapes.append(shape)

    def get_max_x(self):
        return max((shape.x + getattr(shape, 'width', getattr(shape, 'size', 0)) for shape in self.shapes), default=self.canvas_width)

    def get_max_y(self):
        return max((shape.y + getattr(shape, 'height', getattr(shape, 'size', 0)) for shape in self.shapes), default=self.canvas_height)

    def generate_test_scene(self, scene_id: int):
        """Generates predefined test scenes with automatic centering."""
        self.shapes.clear()

        if scene_id == 1:
            # Rectangle(x, y, width, height, border_color, border_width, fill_color)
            self.add_shape(Rectangle(self.center_x - 50, self.center_y - 50, 100, 200, QColor(0, 0, 255), 2, QColor(255, 255, 255, 0)))
            # Circle(x, y, width, height, border_color, border_width, fill_color)
            self.add_shape(Circle(self.center_x - 100, self.center_y - 100, 100, 100, QColor(255, 0, 0), 2, QColor(0, 255, 0, 0)))

        elif scene_id == 2:
            self.add_shape(Rectangle(self.center_x - 200, self.center_y - 125, 200, 200, QColor(0, 0, 255), 2, QColor(0, 0, 255)))
            self.add_shape(Rectangle(self.center_x, self.center_y - 125, 200, 200, QColor(0, 0, 255), 2, QColor(0, 0, 255)))

            self.add_shape(Rectangle(self.center_x - 200, self.center_y + 175, 200, 200, QColor(0, 0, 255), 2, QColor(0, 0, 255)))
            self.add_shape(Rectangle(self.center_x, self.center_y + 175, 200, 200, QColor(0, 0, 255), 2, QColor(0, 0, 255)))

            self.add_shape(Circle(self.center_x - 100, self.center_y - 125, 64, 64, QColor(255, 0, 0), 2, QColor(255, 0, 0)))
            self.add_shape(Circle(self.center_x - 100, self.center_y + 175, 64, 64, QColor(255, 0, 0), 2, QColor(255, 0, 0)))

            self.add_shape(Circle(self.center_x + 100, self.center_y - 125, 64, 64, QColor(255, 0, 0), 2, QColor(255, 0, 0)))
            self.add_shape(Circle(self.center_x + 100, self.center_y + 175, 64, 64, QColor(255, 0, 0), 2, QColor(255, 0, 0)))

        elif scene_id == 3:
            star_size = 100
            star_x = self.center_x - star_size // 2
            star_y = self.center_y - star_size // 2
            # Star(x, y, width, height, border_color, border_width, fill_color)
            self.add_shape(Star(star_x, star_y, star_size, star_size, QColor(255, 0, 0), 2, QColor(255, 255, 0)))

        else:
            print(f"Warnung: Szenen-ID {scene_id} ist ungültig.")


    def all_triangles(self, n_subdivisions=2, deform=False, deform_params=None):
        tris = []
        for shape in self.shapes:
            s_tris = shape.describe_triangles(n_subdivisions)
            if deform:
                if deform_params is None:
                    deform_params = {}
                s_tris = deform_triangles(s_tris, **deform_params)
            tris.extend(s_tris)
        return tris