import pygame as pg
from FLAMEACID.flameacid.window.consts import *

def load(path):
    return pg.image.load(path)

def is_convex(prev, curr, next):
    x1, y1 = prev
    x2, y2 = curr
    x3, y3 = next
    return (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1) > 0


def point_in_triangle(p, a, b, c):
    det_t = lambda p1, p2, p3: (p2[0]-p1[0])*(p3[1]-p1[1]) - (p2[1]-p1[1])*(p3[0]-p1[0])
    b1 = det_t(p, a, b) < 0.0
    b2 = det_t(p, b, c) < 0.0
    b3 = det_t(p, c, a) < 0.0
    return (b1 == b2) and (b2 == b3)


def remove_consecutive_duplicates(polygon):
    return [pt for i, pt in enumerate(polygon) if i == 0 or pt != polygon[i-1]]


def is_convex_polygon(polygon):
    n = len(polygon)
    if n < 4:
        return True

    Sign = None

    for i in range(n):
        prev, curr, next = polygon[i-1], polygon[i], polygon[(i+1) % n]
        cross = (curr[0]-prev[0])*(next[1]-prev[1]) - (curr[1]-prev[1])*(next[0]-prev[0])

        if cross != 0:
            if Sign is None:
                Sign = cross > 0
            elif (cross > 0) != Sign:
                return False

    return True


def triangulate_convex(polygon):
    return [[polygon[0], polygon[i], polygon[i+1]] for i in range(1, len(polygon)-1)]


def ear_clipping(polygon):
    Verts = polygon[:]
    Triangles = []

    while len(Verts) > 3:
        Ear_Found = False
        n = len(Verts)

        for i in range(n):
            prev = Verts[i - 1]
            curr = Verts[i]
            next = Verts[(i + 1) % n]

            if is_convex(prev, curr, next):
                if not any(point_in_triangle(p, prev, curr, next) for j, p in enumerate(Verts) if j not in [i-1, i, (i+1) % n]):
                    Triangles.append([prev, curr, next])
                    del Verts[i]
                    Ear_Found = True
                    break

        if not Ear_Found:
            raise ValueError("Polygon triangulation failed — might be malformed or not simple")

    Triangles.append([Verts[0], Verts[1], Verts[2]])
    return Triangles


def triangulate_polygon(polygon):
    polygon = remove_consecutive_duplicates(polygon)

    if len(polygon) < 3:
        return []
    if len(polygon) == 3:
        return [polygon]
    if is_convex_polygon(polygon):
        return triangulate_convex(polygon)

    return ear_clipping(polygon)


# ─── Math Utils ───────────────────────────────────────────────────────────────

def pixel_to_ndc(x, y, w, h):
    Ndc_X = (x / w) * 2 - 1
    Ndc_Y = 1 - (y / h) * 2
    return Ndc_X, Ndc_Y


def line_points(start, end):
    x0, y0 = start
    x1, y1 = end
    Line_Points = []

    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        Line_Points.append((x0, y0))

        if x0 == x1 and y0 == y1:
            break

        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

    return Line_Points


def fill_triangle(p1, p2, p3):
    Vertices = sorted([p1, p2, p3], key=lambda v: v[1])
    x1, y1 = Vertices[0]
    x2, y2 = Vertices[1]
    x3, y3 = Vertices[2]
    Triangle_Points = []

    def interp(y, y0, x0, y1, x1):
        if y1 == y0:
            return x0
        return int(x0 + (x1 - x0) * (y - y0) / (y1 - y0))

    for y in range(y1, y2 + 1):
        xa = interp(y, y1, x1, y3, x3)
        xb = interp(y, y1, x1, y2, x2)
        if xa > xb:
            xa, xb = xb, xa
        for x in range(xa, xb + 1):
            Triangle_Points.append((x, y))

    for y in range(y2, y3 + 1):
        xa = interp(y, y1, x1, y3, x3)
        xb = interp(y, y2, x2, y3, x3)
        if xa > xb:
            xa, xb = xb, xa
        for x in range(xa, xb + 1):
            Triangle_Points.append((x, y))

    return Triangle_Points


# ─── Color Utils ──────────────────────────────────────────────────────────────

def color_swap(color):
    if color in COLORS_LIST:
        return COLORS[color]
    return color


# ─── Input Utils ──────────────────────────────────────────────────────────────

def get_mouse_pos():
    return pg.mouse.get_pos()


def has_clicked():
    return pg.mouse.get_pressed()


def has_pressed(key):
    key = KEY_MAPPING.get(key.lower(), key)
    return pg.key.get_pressed()[key]


def has_just_pressed(key):
    key = KEY_MAPPING.get(key.lower(), key)
    return pg.key.get_just_pressed()[key]