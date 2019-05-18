from vector import Vector
from vector import midpoint


def resolve_collision(a, b, contact_points, n, reference_face, penetration):
    k_slop = 0.05
    percent = 0.4
    correction = max(penetration - k_slop, 0) / (a.inv_mass + b.inv_mass) * percent * n

    a.pos += a.inv_mass * correction
    b.pos -= b.inv_mass * correction

    if len(contact_points) == 2:
        mp = midpoint(Vector(*reference_face[0]), Vector(*reference_face[1]))
        r_ap = a.pos - mp
        r_bp = b.pos - mp

    else:
        r_ap = a.pos - contact_points[0]
        r_bp = b.pos - contact_points[0]

    v_ap = a.v + r_ap.cross(a.omega)
    v_bp = b.v + r_bp.cross(b.omega)

    relative_v = v_ap - v_bp

    rv_along_normal = n.dot(relative_v)

    if rv_along_normal > 0:
        return

    e = min(a.restitution, b.restitution)

    j = -(1 + e) * rv_along_normal
    j /= a.inv_mass + b.inv_mass + (r_ap.cross(n))**2 / a.I + (r_bp.cross(n))**2 / b.I

    impulse = j * n

    a.v += a.inv_mass * impulse
    b.v -= b.inv_mass * impulse

    a.omega += 1 / a.I * r_bp.cross(impulse)

    b.omega -= 1 / b.I * r_ap.cross(impulse)



