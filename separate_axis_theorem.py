""" Most basic version of SAT without returning contact points. """

from vector import Vector
from vector import vector_between_points
from collision import perpendicular_axis

import math


def projected_points_mag(points, axis):
    """
    Takes a list of points (x, y) and projects them onto the axis
    (represented by a unit vector). It then returns the magnitudes of the projected
    vectors.
    """
    magnitudes = []
    for point in points:
        vec = Vector(*point)  # turn point into vector
        vec = vec.proj(axis)  # project vector onto axis
        magnitudes.append(vec.mag())  # append the magnitude of projected vector
    return magnitudes


def overlap(a_magnitudes, b_magnitudes):
    """
    Returns True if there's overlap between the projected polygons on an axis
    by using the magnitudes of the projected vertices' vectors.
    """
    a_max = max(a_magnitudes)
    a_min = min(a_magnitudes)
    b_max = max(b_magnitudes)
    b_min = min(b_magnitudes)
    return a_max >= b_min and a_min <= b_max


def projected_deepness(a_magnitudes, b_magnitudes):
    a_max = max(a_magnitudes)
    a_min = min(a_magnitudes)
    b_max = max(b_magnitudes)
    b_min = min(b_magnitudes)

    # prototype version
    return min(a_max - b_min, b_max - a_min)


def sat(a, b):
    """
    Separating Axis Theorem
    explanation: https://www.sevenson.com.au/actionscript/sat/
    """
    a_vertices = a.get_vertices()
    b_vertices = b.get_vertices()

    deepnesses = []
    axes = []
    for i, v in enumerate(a_vertices):
        edge = vector_between_points(v, a_vertices[i-1])
        axis = perpendicular_axis(edge)
        axes.append(axis)

    for i, v in enumerate(b_vertices):
        edge = vector_between_points(v, b_vertices[i-1])
        axis = perpendicular_axis(edge)
        axes.append(axis)

    # Remove parallel axes
    for axis in axes:
        for other_axis in axes:
            if axis is other_axis:
                continue
            elif axis == other_axis or axis.rotate(angle=math.pi) == other_axis:  # True if axes are parallel
                axes.remove(other_axis)

    for axis in axes:
        a_projected = projected_points_mag(a_vertices, axis)
        b_projected = projected_points_mag(b_vertices, axis)
        # If projections don't overlap a collision is impossible
        if not overlap(a_projected, b_projected):
            return False

        deepness = projected_deepness(a_projected, b_projected)
        deepnesses.append([deepness, axis])

    # If the loop continues without encountering any overlap, the polygons must collide
    sat_response(a, b, deepnesses)
    return True


def sat_response(a, b, deepnesses):
    # Get minimum deepness value and its axis
    min_deepness = float('+inf')
    min_deepness_axis = None
    for lst in deepnesses:
        new_minimum = min(min_deepness, lst[0])
        if new_minimum < min_deepness:
            min_deepness = new_minimum
            min_deepness_axis = lst[1]

    # Set new position
    displacement_vector = min_deepness*min_deepness_axis

    direction_vector = a.pos - b.pos
    if displacement_vector.dot(direction_vector) > 0:
        displacement_vector *= -1

    a.v = Vector(0, 0)
    a.pos -= displacement_vector