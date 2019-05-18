from vector import vector_between_points
import math
from pyglet import graphics
from core import PhysicsObject


class Rectangle(PhysicsObject):

    def __init__(self, pos, mass, width, height, **kwargs):
        super(Rectangle, self).__init__(pos, mass, **kwargs)
        self.width = width
        self.height = height
        self.I = self.mass / 12 * (self.width**2 + self.height**2)  # Moment of inertia
        self.v0 = []  # bottom left
        self.v1 = []  # bottom right
        self.v2 = []  # top right
        self.v3 = []  # top left
        self.set_vertices()  # sets vertices to correct value based on rectangle width, height, and angle (theta).
        # Attributes for adding to a pyglet Batch() and drawing the object
        self.vtot = 4
        self.mode = graphics.GL_QUADS
        self.batch_group = None
        self.draw_format = 'v2f'

    def __call__(self):
        # Return the parameters needed for a batch
        return self.vtot, self.mode, self.batch_group, (self.draw_format, self.vertices_tuple())

    def update(self, dt):
        super(Rectangle, self).update(dt)  # update of kinematic variables happen in superclass
        self.set_vertices()

    def set_vertices(self):
        if self.theta == 0:
            self.v0, self.v1, self.v2, self.v3 = self.non_rotated_vertices()
        else:
            self.v0, self.v1, self.v2, self.v3 = self.rotated_vertices()

    def get_vertices(self):
        return [self.v0, self.v1, self.v2, self.v3]

    def get_edges(self):
        """ Returns edges as Vectors """
        edges = []
        vertices = self.get_vertices()
        for i, v in enumerate(vertices):
            edge = vector_between_points(v, vertices[i-1])
            edges.append(edge)
        return edges

    def non_rotated_vertices(self):
        """ Vertices when the rectangle's angle theta == 0 """
        v0 = [self.pos.x - self.width / 2, self.pos.y - self.height / 2]
        v1 = [self.pos.x + self.width / 2, self.pos.y - self.height / 2]
        v2 = [self.pos.x + self.width / 2, self.pos.y + self.height / 2]
        v3 = [self.pos.x - self.width / 2, self.pos.y + self.height / 2]
        return v0, v1, v2, v3

    def rotated_vertices(self):
        """ Calculates coordinates for vertices based on the rectangles angle theta """
        rotated_vertices = []
        for v in self.non_rotated_vertices():
            x, y = v[0], v[1]
            x_rotated = self.pos.x + (x-self.pos.x)*math.cos(self.theta) - (y-self.pos.y)*math.sin(self.theta)
            y_rotated = self.pos.y + (x-self.pos.x)*math.sin(self.theta) + (y-self.pos.y)*math.cos(self.theta)
            rotated_vertices.append([x_rotated, y_rotated])
        return rotated_vertices

    def vertices_tuple(self):
        """ Returns vertices in tuple format compatible with pyglet """
        vtuple = (*self.v0, *self.v1, *self.v2, *self.v3)
        return vtuple

    def draw(self):
        graphics.draw(self.vtot, self.mode, self.batch_group, (self.draw_format, self.vertices_tuple()))




