# inspiration from https://github.com/jmcelroy5/Pyglet-Game/blob/master/core.py
from vector import Vector
from collision import is_overlapping


class Environment:
    physics_objects = []  # list of all created physics_objects
    pairs = []

    def __init__(self, window, g=9.8):
        self.g = g  # Gravitational acceleration
        self.window = window

    @classmethod
    def generate_pairs(cls):
        """ Clears cls.pairs and generates new pairs from cls.physics_objects """
        cls.pairs.clear()
        for i, a in enumerate(cls.physics_objects):
            for b in cls.physics_objects[i:]:  # the [i:] slicing skips the same pair in reversed order
                if a == b:  # avoid pairing a with a
                    continue
                cls.pairs.append([a, b])

    @classmethod
    def update(cls, dt):
        if not cls.pairs and cls.physics_objects:  # generate pairs if there are physics_objects but no pairs
            cls.generate_pairs()

        for pair in cls.pairs:
            is_overlapping(*pair)
        for po in cls.physics_objects:
            po.update(dt)

    #     self.draw_floor()
    #
    # def draw_floor(self):
    #     width = self.window.width
    #     height = 40
    #     floor = Floor(width, height)


class Floor:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.v0 = [0, 0]  # bottom left
        self.v1 = [self.width, 0]  # bottom right
        self.v2 = [self.width, self.height]  # top right
        self.v3 = [0, self.height]  # top left

    def vertices_tuple(self):
        """ Returns vertices in tuple format compatible with pyglet """
        vtuple = (*self.v0, *self.v1, *self.v2, *self.v3)
        return vtuple


class PhysicsObject:

    def __init__(self, pos, mass, **kwargs):
        assert isinstance(pos, Vector), "pos must be a Vector"
        self.pos = pos  # Position (x, y)
        self.v = kwargs.get('v', Vector(0, 0))  # Velocity
        self.a = kwargs.get('a', Vector(0, 0))  # Acceleration
        self.theta = kwargs.get('theta', 0)  # Rotational angle
        self.omega = kwargs.get('omega', 0)  # Rotational velocity
        self.alpha = kwargs.get('alpha', 0)  # Rotational acceleration
        self.restitution = kwargs.get('restitution', 1)  # Coefficient of restitution
        self.mass = mass
        self.inv_mass = 1 / self.mass

        # Set environment
        Environment.physics_objects.append(self)

    def __str__(self):
        return "<%s located at %r, %r>" % (type(self).__name__, self.pos.x, self.pos.y)

    def update(self, dt):
        # Update position
        self.pos.x += self.v.x*dt
        self.pos.y += self.v.y*dt
        # Update rotation
        self.theta += self.omega*dt
        # Update linear velocity
        self.v.x += self.a.x*dt
        self.v.y += self.a.y*dt
        # Update rotational velocity
        self.omega += self.alpha*dt


