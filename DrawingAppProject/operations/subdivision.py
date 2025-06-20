def subdivide_triangle(tri):
    (a, b, c) = tri
    ab = ((a[0]+b[0])/2, (a[1]+b[1])/2)
    bc = ((b[0]+c[0])/2, (b[1]+c[1])/2)
    ca = ((c[0]+a[0])/2, (c[1]+a[1])/2)
    return [
        (a, ab, ca),
        (ab, b, bc),
        (ca, bc, c),
        (ab, bc, ca)
    ]

def subdivide_triangles(tris, n):
    for _ in range(n):
        tris = [t for tri in tris for t in subdivide_triangle(tri)]
    return tris