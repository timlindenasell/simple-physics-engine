"""
The functions in collision.py use a simple notation for polygons, calling them 'a' and
'b'.

Thanks to the sources below for mathematical theory and inspiration:
- https://gdcvault.com/play/1017646/Physics-for-Game-Programmers-The
- https://gamedevelopment.tutsplus.com/tutorials/how-to-create-a-custom-2d-physics-engine-oriented-rigid-bodies--gamedev-8032
- http://chrishecker.com/images/e/e7/Gdmphys3.pdf
- Erin Catto GDC talk 2007 PowerPoint

"""

from vector import Vector
from vector import vector_between_points
from impulse_resolution import resolve_collision
import math


def perpendicular_axis(vec):
    """ Returns a normalized vector perpendicular (rotated -90 degrees) to the vector vec  """
    axis = vec.rotate(-math.pi / 2)  # rotate vector -90 degrees
    axis = axis.norm()  # turn axis vector into unit vector
    return axis


def get_support(a, direction):
    """ Returns support point """
    vertices = a.get_vertices()
    best_projection = float('-inf')
    best_vertex = None
    for vertex in vertices:
        vertex_vector = Vector(*vertex)
        projection = vertex_vector.dot(direction)
        if projection > best_projection:
            best_projection = projection
            best_vertex = vertex

    return Vector(*best_vertex)


def find_axis_least_penetration(a, b):
    best_distance = float('-inf')
    best_index = None
    a_edges = a.get_edges()
    a_vertices = a.get_vertices()

    for i, a_edge in enumerate(a_edges):
        normal = perpendicular_axis(a_edge)
        support = get_support(b, -normal)
        a_vertex_vector = Vector(*a_vertices[i])
        distance = normal.dot(support - a_vertex_vector)

        if distance > best_distance:
            best_distance = distance
            best_index = i

    return best_distance, best_index


def is_overlapping(a, b):
    contact_points = None
    penetration = None

    a_best_distance, a_best_index = find_axis_least_penetration(a, b)
    if a_best_distance > 0.0:
        return None, None

    b_best_distance, b_best_index = find_axis_least_penetration(b, a)
    if b_best_distance > 0.0:
        return None, None

    # If polygon a and b overlap:

    # If true: Polygon b becomes the reference face
    if a_best_distance <= b_best_distance: # TODO: Possibly set separate condition for a_best_distance == b_best_distance
        contact_points, penetration = get_contact_penetration(a, b, b_best_index)

    # If true: Polygon a becomes the reference face
    elif a_best_distance > b_best_distance:  # TODO: possibly replace with else statement
        contact_points, penetration = get_contact_penetration(b, a, a_best_index)

    return contact_points, penetration


def get_incident_face(normal, edges, vertices):
    incident_face = []
    incident_index = None
    max_magnitude = float('inf')

    for i, edge in enumerate(edges):
        other_normal = perpendicular_axis(edge)
        resultant = normal + other_normal
        magnitude = resultant.mag()

        if magnitude < max_magnitude:
            max_magnitude = magnitude
            incident_face = [vertices[i-1], vertices[i]]
            incident_index = i

    return incident_face, incident_index


def lerp(start, end, alpha):
    """ Linear interpolation """
    return (end - start)*alpha + start


def clip(side_plane, side_norm, incident_face):
    sp = 0
    # Distances from the endpoints of the incident face (e1 and e2) to the side plane
    # Distance formula: d = n dot (p1 - p2)
    incident_e1 = incident_face[0]
    incident_e2 = incident_face[1]

    # Turn into vectors
    if not isinstance(incident_face[0], Vector):
        incident_e1 = Vector(*incident_face[0])
        incident_e2 = Vector(*incident_face[1])

    edges = [incident_e1, incident_e2]

    d1 = side_norm.dot(incident_e1) - side_plane
    d2 = side_norm.dot(incident_e2) - side_plane

    # If edge point is behind plane
    if d1 <= 0.0:
        sp += 1
    if d2 <= 0.0:
        sp += 1

    # If edge points are on different sides of the plane
    if d1*d2 < 0.0:
        alpha = d1/(d1 - d2)
        edges[sp] = lerp(incident_e1, incident_e2, alpha)
        sp += 1

    assert sp != 3

    return edges[0], edges[1]


def get_contact_penetration(a, b, best_index):
    contact_points = []
    penetration = 0

    a_vertices = a.get_vertices()
    a_edges = a.get_edges()
    b_vertices = b.get_vertices()
    b_edges = b.get_edges()

    reference_face = [b_vertices[best_index], b_vertices[best_index-1]]  # reference face as list of 2 vertices
    reference_normal = perpendicular_axis(vector_between_points(*reference_face))  # vector normal to reference face
    # Store incident face as list of 2 vertices. incident_index is the index of the first vertex in incident_face
    incident_face, incident_index = get_incident_face(reference_normal, a_edges, a_vertices)

    # c is the distance from the reference vertex to the origin
    reference_v = Vector(*reference_face[0])
    reference_c = reference_normal.dot(reference_v)

    # Get side plane normal
    left_norm = b_edges[best_index].norm()
    right_norm = -left_norm

    # Get side plane
    side_plane_left = -left_norm.dot(Vector(*reference_face[0]))
    side_plane_right = right_norm.dot(Vector(*reference_face[1]))

    # Clip incident face against side planes of reference face
    incident_face[0], incident_face[1] = clip(side_plane_left, left_norm, incident_face)
    incident_face[0], incident_face[1] = clip(side_plane_right, right_norm, incident_face)

    # Keep incident_face points below reference face
    separation = reference_normal.dot(incident_face[0]) - reference_c

    if separation <= 0.0:
        contact_points.append(incident_face[0])
        penetration = -separation

    separation = reference_normal.dot(incident_face[1]) - reference_c
    if separation <= 0.0:
        contact_points.append(incident_face[1])
        penetration += -separation

    resolve_collision(a, b, contact_points, reference_normal, reference_face, penetration)

    return contact_points, penetration


def broad_phase():
    pass

