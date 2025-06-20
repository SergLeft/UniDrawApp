import math

def deform_point(x, y, a=30, b=1/200, c=0):
    return (x, y + a * math.sin(2 * math.pi * b * x + c))

def deform_triangles(tris, a=30, b=1/200, c=0):
    return [[deform_point(*p, a, b, c) for p in tri] for tri in tris]