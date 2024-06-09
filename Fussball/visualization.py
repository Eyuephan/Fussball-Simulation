import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D, art3d
from constants import FIELD_LENGTH, FIELD_WIDTH, CENTER_CIRCLE_RADIUS, PENALTY_AREA_LENGTH, PENALTY_AREA_WIDTH, GOAL_AREA_LENGTH, GOAL_AREA_WIDTH, PENALTY_SPOT_DISTANCE, CORNER_ARC_RADIUS, GOAL_WIDTH, GOAL_HEIGHT, BALL_RADIUS

def plot_field(ax):
    ax.set_xlim(0, FIELD_LENGTH)
    ax.set_ylim(0, FIELD_WIDTH)
    ax.set_zlim(0, 15)  # Adjust the Z axis to better visualize ball height

    # Draw the outer boundary
    corners = [
        (0, 0), (FIELD_LENGTH, 0), (FIELD_LENGTH, FIELD_WIDTH), (0, FIELD_WIDTH), (0, 0)
    ]
    ax.plot([corner[0] for corner in corners], [corner[1] for corner in corners], 0, color='black')

    # Draw the center line
    ax.plot([FIELD_LENGTH / 2, FIELD_LENGTH / 2], [0, FIELD_WIDTH], 0, color='black')

    # Draw the center circle
    theta = np.linspace(0, 2 * np.pi, 100)
    x = CENTER_CIRCLE_RADIUS * np.cos(theta) + FIELD_LENGTH / 2
    y = CENTER_CIRCLE_RADIUS * np.sin(theta) + FIELD_WIDTH / 2
    ax.plot(x, y, 0, color='black')

    # Draw the center mark
    ax.plot([FIELD_LENGTH / 2], [FIELD_WIDTH / 2], [0], marker='o', color='black')

    # Draw the penalty areas
    penalty_area_coords = [
        (0, (FIELD_WIDTH - PENALTY_AREA_WIDTH) / 2),
        (PENALTY_AREA_LENGTH, (FIELD_WIDTH - PENALTY_AREA_WIDTH) / 2),
        (PENALTY_AREA_LENGTH, (FIELD_WIDTH + PENALTY_AREA_WIDTH) / 2),
        (0, (FIELD_WIDTH + PENALTY_AREA_WIDTH) / 2),
        (0, (FIELD_WIDTH - PENALTY_AREA_WIDTH) / 2)
    ]
    for side in [0, FIELD_LENGTH - PENALTY_AREA_LENGTH]:
        ax.plot([side + coord[0] for coord in penalty_area_coords],
                [coord[1] for coord in penalty_area_coords], 0, color='black')

    # Draw the goal areas
    goal_area_coords = [
        (0, (FIELD_WIDTH - GOAL_AREA_WIDTH) / 2),
        (GOAL_AREA_LENGTH, (FIELD_WIDTH - GOAL_AREA_WIDTH) / 2),
        (GOAL_AREA_LENGTH, (FIELD_WIDTH + GOAL_AREA_WIDTH) / 2),
        (0, (FIELD_WIDTH + GOAL_AREA_WIDTH) / 2),
        (0, (FIELD_WIDTH - GOAL_AREA_WIDTH) / 2)
    ]
    for side in [0, FIELD_LENGTH - GOAL_AREA_LENGTH]:
        ax.plot([side + coord[0] for coord in goal_area_coords],
                [coord[1] for coord in goal_area_coords], 0, color='black')

    # Draw the penalty spots as points
    ax.scatter([PENALTY_SPOT_DISTANCE], [FIELD_WIDTH / 2], [0], color='black')
    ax.scatter([FIELD_LENGTH - PENALTY_SPOT_DISTANCE], [FIELD_WIDTH / 2], [0], color='black')

    # Draw the corner arcs
    corners = [(0, 0), (0, FIELD_WIDTH), (FIELD_LENGTH, 0), (FIELD_LENGTH, FIELD_WIDTH)]
    for corner in corners:
        x = CORNER_ARC_RADIUS * np.cos(theta) + corner[0]
        y = CORNER_ARC_RADIUS * np.sin(theta) + corner[1]
        ax.plot(x, y, 0, color='black')

    # The wall will be drawn dynamically based on the ball position
    ax.set_box_aspect([FIELD_LENGTH, FIELD_WIDTH, 15])  # aspect ratio to correct the z-axis scaling
    ax.set_xlabel('Length (m)')
    ax.set_ylabel('Width (m)')
    ax.set_zlabel('Height (m)')

    # Set Z-axis ticks to show meters in 5 steps
    ax.set_zticks(np.arange(0, 16, 5))  # Display meters from 0 to 15 in steps of 5
    ax.set_zticklabels([str(i) for i in np.arange(0, 16, 5)])  # Label the ticks as meters

def add_ball(ax, position, radius=0.22):
    u = np.linspace(0, 2 * np.pi, 20)  # Reduced number of points
    v = np.linspace(0, np.pi, 20)     # Reduced number of points
    x = radius * np.outer(np.cos(u), np.sin(v)) + position[0]
    y = radius * np.outer(np.sin(u), np.sin(v)) + position[1]
    z = radius * np.outer(np.ones(np.size(u)), np.cos(v)) + position[2]

    ball = ax.plot_surface(x, y, z, color='red')
    return ball

def update_ball(ax, position, ball, radius=0.22):
    ball.remove()
    return add_ball(ax, position, radius)

def add_goals(ax):
    goal_depth = -1 # Set the desired depth of the goal
    goal_color = 'blue'
    for x in [0, FIELD_LENGTH]:
        y = FIELD_WIDTH / 2 - GOAL_WIDTH / 2
        goal_coords = [
            [x, y, 0],
            [x, y + GOAL_WIDTH, 0],
            [x, y + GOAL_WIDTH, GOAL_HEIGHT],
            [x, y, GOAL_HEIGHT],
            [x + goal_depth if x == 0 else x - goal_depth, y, 0],
            [x + goal_depth if x == 0 else x - goal_depth, y + GOAL_WIDTH, 0],
            [x + goal_depth if x == 0 else x - goal_depth, y + GOAL_WIDTH, GOAL_HEIGHT],
            [x + goal_depth if x == 0 else x - goal_depth, y, GOAL_HEIGHT]
        ]
        # Draw goal posts
        for i in range(4):
            ax.plot3D(*zip(goal_coords[i], goal_coords[(i+1) % 4]), color=goal_color)
            ax.plot3D(*zip(goal_coords[i + 4], goal_coords[(i+1) % 4 + 4]), color=goal_color)
            ax.plot3D(*zip(goal_coords[i], goal_coords[i + 4]), color=goal_color)
        # Draw goal crossbars
        ax.plot3D(*zip(goal_coords[2], goal_coords[6]), color=goal_color)
        ax.plot3D(*zip(goal_coords[3], goal_coords[7]), color=goal_color)
        # Draw the back of the goal
        for i in range(4, 8):
            ax.plot3D(*zip(goal_coords[i], goal_coords[(i+1) % 4 + 4]), color=goal_color)

def add_wall(ax, wall_x, wall_y_start, wall_y_end, wall_z):
    color = 'green'
    wall_width = wall_y_end - wall_y_start

    # Define the vertices of the wall as a rectangular surface
    vertices = np.array([
        [wall_x, wall_y_start, 0],
        [wall_x, wall_y_end, 0],
        [wall_x, wall_y_end, wall_z],
        [wall_x, wall_y_start, wall_z]
    ])

    # Create a 3D polygon to represent the wall
    wall = art3d.Poly3DCollection([vertices], color=color, alpha=0.5)
    ax.add_collection3d(wall)

    # Add thickness to the wall
    thickness = 0.5  # Set the desired thickness of the wall
    vertices[:, 0] += thickness
    wall = art3d.Poly3DCollection([vertices], color=color, alpha=0.5)
    ax.add_collection3d(wall)