class SVGExporter:
    @staticmethod
    def export_to_svg(shapes, filename, width=800, height=600):
        with open(filename, 'w') as f:
            #header
            f.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
            f.write(f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">\n')

            #shape processing?
            for shape in shapes:
                triangles = shape.describeShape()
                for triangle in triangles:
                    fill_color = triangle.fill_color.name() if hasattr(triangle.fill_color, 'name') else "black"
                    points = f"{triangle.p1[0]},{triangle.p1[1]} {triangle.p2[0]},{triangle.p2[1]} {triangle.p3[0]},{triangle.p3[1]}"
                    f.write(f'  <polygon points="{points}" fill="{fill_color}" />\n')

            #close down
            f.write('</svg>\n')