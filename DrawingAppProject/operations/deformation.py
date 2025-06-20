import math
from shapes.triangle import Triangle

class Deformation:
    @staticmethod
    def apply(triangles, a=20, b=0.005, c=0):
        result = []

        for triangle in triangles:
            #vertex transformation
            new_p1 = (triangle.p1[0],
                     triangle.p1[1] + a * math.sin(2 * math.pi * b * triangle.p1[0] + c))
            new_p2 = (triangle.p2[0],
                     triangle.p2[1] + a * math.sin(2 * math.pi * b * triangle.p2[0] + c))
            new_p3 = (triangle.p3[0],
                     triangle.p3[1] + a * math.sin(2 * math.pi * b * triangle.p3[0] + c))

            # Change this line in deformation.py
            result.append(
                Triangle(new_p1, new_p2, new_p3, triangle.fill_color, triangle.border_color, triangle.border_width))

        return result