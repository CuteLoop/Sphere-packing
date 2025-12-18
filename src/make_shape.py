import math
from shapely.geometry import Polygon

def make_polygon(coordinates):
    """
    Create a polygon from a list of (x, y) tuples.
    """
    return Polygon(coordinates)


def make_circle(center, radius, num_points=100):
    """
    Approximate a circle by a polygon.
    """
    points = []
    for i in range(num_points):
        angle = 2 * math.pi * i / num_points
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        points.append((x, y))
    return Polygon(points)
