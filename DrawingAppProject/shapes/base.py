from abc import ABC, abstractmethod
from PySide6.QtGui import QColor, QPolygonF
from math import pi, cos, sin

class Shape(ABC):

    def __init__(self, x: int, y: int, fill_color: QColor, border_color: QColor, border_width: int):
        self.x = x
        self.y = y
        self.fill_color = fill_color
        self.border_color = border_color
        self.border_width = border_width

    @abstractmethod
    def draw(self, painter):
        pass

    @abstractmethod
    def contains_point(self, point):
        pass

    @abstractmethod
    def translate(self, dx, dy):    #no Jennifer, we don't mean literal language translation
        pass

    @abstractmethod
    def scale(self, sx, sy):    #no, I am not trying to get you to start a diet
        pass
