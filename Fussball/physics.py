import numpy as np

# Konstanten
GRAVITATION = 9.81  # m/s^2
LUFTDICHTE = 1.2041  # kg/m^3
LUFTWIDERSTANDSKOEFFIZIENT = 0.47 #bei 20 grad
QUERSCHNITTSFLAECHE = np.pi * (0.11**2)
REIBUNGSKOEFFIZIENT = 0.3
BALLMASSE = 0.43
BALLRADIUS = 0.11
MAGNUSKOEFFIZIENT = 0.2

def berechne_gravitationskraft(masse):
    return np.array([0, 0, -masse * GRAVITATION], dtype=np.float64)

# Diese Funktion berechnet die Gravitationskraft, die auf den Ball wirkt.
# Sie gibt einen Vektor zurück, der nach unten gerichtet ist, mit einer Stärke von 'masse * GRAVITATION'.

def calculate_drag_force(velocity):
    speed = np.linalg.norm(velocity)
    if speed == 0:
        return np.array([0, 0, 0], dtype=np.float64)
    drag_magnitude = 0.5 * LUFTDICHTE * LUFTWIDERSTANDSKOEFFIZIENT * QUERSCHNITTSFLAECHE * speed**2
    drag_force = -drag_magnitude * (velocity / speed)
    return drag_force

# Diese Funktion berechnet die Luftwiderstandskraft, die auf den Ball wirkt.
# Der Luftwiderstand ist proportional zum Quadrat der Geschwindigkeit und wirkt in die entgegengesetzte Richtung der Bewegung.

def calculate_friction_force(normal_force, velocity):
    if np.linalg.norm(velocity) == 0:
        return np.array([0, 0, 0], dtype=np.float64)
    friction_force = -REIBUNGSKOEFFIZIENT * normal_force * (velocity / np.linalg.norm(velocity))
    return friction_force

# Diese Funktion berechnet die Reibungskraft, die auf den Ball wirkt, wenn er den Boden berührt.
# Die Reibungskraft ist proportional zur Normalkraft und wirkt entgegengesetzt zur Bewegungsrichtung.

def calculate_magnus_force(spin, velocity):
    return MAGNUSKOEFFIZIENT * LUFTDICHTE * QUERSCHNITTSFLAECHE * np.cross(spin, velocity)

# Diese Funktion berechnet die Magnus-Kraft, die auf den Ball wirkt, wenn er rotiert.
# Diese Kraft wird durch den Spin des Balls und seine Geschwindigkeit erzeugt und steht senkrecht zur Bewegungsrichtung.

def update_ball_position(position, velocity, spin, dt, wall_position=30, wall_height=15, wall_width=48):
    gravity = berechne_gravitationskraft(BALLMASSE)
    drag = calculate_drag_force(velocity)
    magnus = calculate_magnus_force(spin, velocity)

    # Berechne die Kräfte, die auf den Ball wirken: Gravitationskraft, Luftwiderstandskraft und Magnus-Kraft.

    if position[2] <= BALLRADIUS:
        normal_force = BALLMASSE * GRAVITATION
        friction = calculate_friction_force(normal_force, velocity)
    else:
        friction = np.array([0, 0, 0], dtype=np.float64)

    # Wende die Bodenreibung nur an, wenn der Ball den Boden berührt (d.h. seine Höhe ist kleiner oder gleich seinem Radius).

    total_force = gravity + drag + friction + magnus
    acceleration = total_force / BALLMASSE
    velocity = velocity.astype(np.float64) + acceleration * dt
    position = position.astype(np.float64) + velocity * dt

    # Berechne die Gesamtkraft, die auf den Ball wirkt, und daraus die Beschleunigung.
    # Aktualisiere die Geschwindigkeit und Position des Balls basierend auf der Beschleunigung und dem Zeitintervall 'dt'.

    if position[2] < BALLRADIUS:
        position, velocity = resolve_collision_with_ground(position, velocity)

    # Überprüfe, ob der Ball den Boden berührt, und wenn ja, löse die Kollision.

    if (position[0] + BALLRADIUS >= wall_position and
            position[0] - BALLRADIUS <= wall_position and
            0 <= position[1] <= wall_width and
            0 <= position[2] <= wall_height):
        print(f"Collision detected with wall at position: {position}")
        print(f"Ball velocity before collision: {velocity}")
        position, velocity = resolve_collision_with_wall(position, velocity, wall_position)
        print(f"Ball velocity after collision: {velocity}")

    # Überprüfe, ob der Ball die Wand berührt, und wenn ja, löse die Kollision und drucke die relevanten Informationen.

    return position, velocity

# Gebe die aktualisierte Position und Geschwindigkeit des Balls zurück.

def check_collision_with_ground(position):
    return position[2] < BALLRADIUS

# Diese Funktion überprüft, ob der Ball den Boden berührt.

def resolve_collision_with_ground(position, velocity):
    position[2] = BALLRADIUS  # Setze die Position des Balls auf den Boden.
    velocity[2] = -velocity[2] * 0.5  # Kehre die vertikale Geschwindigkeit um und reduziere sie, um den Energieverlust zu simulieren.
    return position, velocity

# Diese Funktion löst die Kollision mit dem Boden, indem sie die vertikale Position und Geschwindigkeit des Balls anpasst.

def resolve_collision_with_wall(position, velocity, wall_position):
    if velocity[0] > 0:  # Ball bewegt sich von links auf die Wand zu.
        position[0] = wall_position - BALLRADIUS
    else:  # Ball bewegt sich von rechts auf die Wand zu.
        position[0] = wall_position + BALLRADIUS
    velocity[0] = -velocity[0] * 0.5  # Kehre die horizontale Geschwindigkeit um und reduziere sie, um den Energieverlust zu simulieren.

    return position, velocity

# Diese Funktion löst die Kollision mit der Wand, indem sie die horizontale Position und Geschwindigkeit des Balls anpasst.


