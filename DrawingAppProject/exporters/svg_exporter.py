def export_scene_to_svg(scene, filename, n_subdivisions=2, deform_params=None):

    width, height = scene.canvas_width, scene.canvas_height
    svg = [f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">']
    for shape in scene.shapes:
        tris = shape.describe_triangles(n_subdivisions)
        if deform_params:
            from core.deformation import deform_triangles
            tris = deform_triangles(tris, **deform_params)
        color = f'rgb({shape.fill_color.red()},{shape.fill_color.green()},{shape.fill_color.blue()})'
        for tri in tris:
            points = " ".join([f"{x},{y}" for (x, y) in tri])
            svg.append(f'<polygon points="{points}" fill="{color}" stroke="none"/>')
    svg.append('</svg>')
    with open(filename, 'w') as f:
        f.write('\n'.join(svg))