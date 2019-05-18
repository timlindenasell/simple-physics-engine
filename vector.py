# inspired by vpython's vector class
# TODO: Add more vector functionality for usability in SAT collision detection
import math


class Vector:
    def __init__(self, *args):
        if len(args) == 2:
            self.x = float(args[0])
            self.y = float(args[1])
        # Make copy of Vector
        elif len(args) == 1 and isinstance(args[0], Vector):
            other = args[0]
            self.x = other.x
            self.y = other.y
        else:
            raise TypeError('A vector needs 2 components (x, y).')

    def __str__(self):
        return '<%f, %f>' % (self.x, self.y)

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector(self.x*other, self.y*other)
        raise TypeError('a vector can only be multiplied by a scalar')

    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            return Vector(self.x*other, self.y*other)
        raise TypeError('a vector can only be multiplied by a scalar')

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Vector(self.x/other, self.y/other)
        raise TypeError('a vector can only be divided by a scalar')

    def __eq__(self, other):
        """ Because of float value, math.isclose is used to allow for very small errors """
        if isinstance(other, self.__class__):
            return math.isclose(self.x, other.x, rel_tol=1e-12, abs_tol=1e-12) and\
                   math.isclose(self.y, other.y, rel_tol=1e-12, abs_tol=1e-12)
        else:
            return False

    def rotate(self, angle=0):
        sn = math.sin(angle)
        cs = math.cos(angle)
        rotated_x = self.x*cs - self.y*sn
        rotated_y = self.x*sn + self.y*cs
        return Vector(rotated_x, rotated_y)

    def norm(self):
        mag = self.mag()
        return Vector(self.x/mag, self.y/mag)

    def mag(self):
        return (self.x**2 + self.y**2)**(1/2)

    def dot(self, other):
        return self.x*other.x + self.y*other.y

    def cross(self, other):
        """
        Cross product is not defined for 2D vectors but for simplicity in physics calculations
        we use the analog to the cross product for 2D vectors.
        """
        if isinstance(other, float):
            return Vector(other*self.y, -other*self.x)

        if isinstance(other, Vector):
            return self.x*other.y - self.y*other.x

    def proj(self, other):
        norm_b = other.norm()
        return self.dot(norm_b)*norm_b


def sum_vectors(vectors):
    """ sum() for Vectors """
    vector_sum = Vector(0, 0)
    for vec in vectors:
        vector_sum += vec
    return vector_sum


def vector_between_points(a, b):
    """ Return vector going from point a to b """
    vector_1 = Vector(*a)
    vector_2 = Vector(*b)
    return vector_1 - vector_2


def midpoint(a, b):
    """ Return vector pointing to midpoint between vector a and b """
    mp = [(a.x + b.x) / 2, (a.y + b.y) / 2]
    return Vector(*mp)
