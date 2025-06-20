from PySide6.QtGui import QPainter, QPen, QPolygonF
from shapes.base import Shape
from math import pi, cos, sin

class Renderer:
    def __init__(self, painter, viewport_width, viewport_height, world_x_min, world_y_min, world_x_max, world_y_max, scale):
        self.painter = painter
        self.viewport_width = viewport_width
        self.viewport_height = viewport_height
        self.world_x_min = world_x_min
        self.world_y_min = world_y_min
        self.world_x_max = world_x_max
        self.world_y_max = world_y_max
        self.scale = scale

        self.scene = None #Will start setting when rendering

    def world_to_viewport(self, x: float, y: float):
        scale_x = self.viewport_width / (self.world_x_max - self.world_x_min)
        scale_y = self.viewport_height / (self.world_y_max - self.world_y_min)
        scale = min(scale_x, scale_y)  # Einheitliche Skalierung

        screen_x = int((x - self.world_x_min - self.scene.view_x) * scale * self.scene.zoom)
        screen_y = int((y - self.world_y_min - self.scene.view_y) * scale * self.scene.zoom)

        return screen_x, screen_y

    def render_scene(self, scene):
        """Zeichnet die gesamte Szene mit QPainter."""
        self.scene = scene #stores scene reference

        for shape in scene.shapes:
            shape.draw(self.painter) #considering the changes further down, this should work well with the abstract class?

    def draw_rectangle(self, rect):
        x, y = self.world_to_viewport(rect.x, rect.y)

        self.painter.setBrush(rect.fill_color)
        self.painter.setPen(rect.border_color)

        self.painter.drawRect(x, y, rect.width, rect.height)

    def draw_circle(self, circle):
        x, y = self.world_to_viewport(circle.x, circle.y)
        radius = circle.radius  # Direkt nutzen, nicht skalieren!

        self.painter.setBrush(circle.fill_color)
        self.painter.setPen(circle.border_color)

        self.painter.drawEllipse(x - radius, y - radius, radius * 2, radius * 2)

    def draw_star(self, star):
        """Zeichnet einen Stern anhand mathematischer Berechnung der Spitzen."""
        x, y = self.world_to_viewport(star.x, star.y)
        scale = min(self.viewport_width / (self.world_x_max - self.world_x_min),
                    self.viewport_height / (self.world_y_max - self.world_y_min))
        size = int(star.size * scale)

        polygon = []
        for i in range(star.points * 2):
            radius = size if i % 2 == 0 else size / 2  # Abwechselnd Spitzen und innere Punkte
            angle = (i / (star.points * 2)) * 2 * pi + pi / star.points  # Winkelberechnung
            px = x + int(radius * cos(angle))
            py = y + int(radius * sin(angle))
            polygon.append((px, py))

        self.painter.setBrush(star.fill_color)
        self.painter.setPen(star.border_color)
        self.painter.drawPolygon([QPoint(p[0], p[1]) for p in polygon])
