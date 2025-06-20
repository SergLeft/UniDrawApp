from abc import ABC, abstractmethod

class Shape(ABC):

    def __init__(self, x, y, width, height, border_color, border_width, fill_color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.border_color = border_color
        self.border_width = border_width
        self.fill_color = fill_color

    @abstractmethod
    def draw(self, painter):
        pass

    @abstractmethod
    def contains_point(self, x, y):
        pass

    @abstractmethod
    def translate(self, dx, dy):
        pass

    @abstractmethod
    def scale(self, sx, sy):
        pass


    @abstractmethod
    def describe_triangles(self, n_subdivisions=0):
        pass