from shapes.triangle import Triangle

class Subdivision:
    @staticmethod
    def apply(triangles, iterations=1):
        result = triangles

        for _ in range(iterations):
            new_result = []
            for triangle in result:
                #midpoints
                mid1 = ((triangle.p1[0] + triangle.p2[0]) / 2,
                       (triangle.p1[1] + triangle.p2[1]) / 2)
                mid2 = ((triangle.p2[0] + triangle.p3[0]) / 2,
                       (triangle.p2[1] + triangle.p3[1]) / 2)
                mid3 = ((triangle.p3[0] + triangle.p1[0]) / 2,
                       (triangle.p3[1] + triangle.p1[1]) / 2)

                # Change these lines in subdivision.py
                t1 = Triangle(triangle.p1, mid1, mid3, triangle.fill_color, triangle.border_color,
                              triangle.border_width)
                t2 = Triangle(mid1, triangle.p2, mid2, triangle.fill_color, triangle.border_color,
                              triangle.border_width)
                t3 = Triangle(mid3, mid2, triangle.p3, triangle.fill_color, triangle.border_color,
                              triangle.border_width)
                t4 = Triangle(mid1, mid2, mid3, triangle.fill_color, triangle.border_color, triangle.border_width)

                new_result.extend([t1, t2, t3, t4])

            result = new_result

        return result