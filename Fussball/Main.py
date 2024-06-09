import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from mpl_toolkits.mplot3d import Axes3D
from visualization import plot_field, add_ball, update_ball, add_goals, add_wall
from physics import update_ball_position, calculate_drag_force, calculate_magnus_force
import numpy as np
import random
from constants import FIELD_LENGTH, FIELD_WIDTH, BALL_RADIUS

def create_window():
    # Create a new window
    root = tk.Tk()
    root.title("3D Football Field Simulation")

    # Create a Figure
    fig = Figure(figsize=(15, 6))
    ax = fig.add_subplot(111, projection='3d')

    # Plot the football field
    plot_field(ax)
    add_goals(ax)

    # Initial ball position
    initial_ball_position = np.array([FIELD_LENGTH - 32, FIELD_WIDTH / 2, BALL_RADIUS], dtype=np.float64)
    ball_position = initial_ball_position.copy()
    ball = add_ball(ax, ball_position)

    # Set static wall position for collision testing
    wall_position = 80  # Static position for testing
    wall_height = 2  # Example wall height
    wall_width = 4   # Example wall width

    # Add the wall to the plot
    add_wall(ax, wall_position, (FIELD_WIDTH / 2) - (wall_width / 2), (FIELD_WIDTH / 2) + (wall_width / 2), wall_height)

    # Create a canvas to embed the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # Add the toolbar for navigation
    toolbar_frame = tk.Frame(root)
    toolbar_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # Add a quit button
    quit_button = tk.Button(root, text="Quit", command=root.quit)
    quit_button.pack(side=tk.BOTTOM)

    # Zoom function centered on the ball
    def zoom(event):
        base_scale = 1.1
        if event.button == 'up':
            scale_factor = base_scale
        elif event.button == 'down':
            scale_factor = 1 / base_scale
        else:
            return

        # Save the current view
        elev = ax.elev
        azim = ax.azim

        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        zlim = ax.get_zlim()

        x_range = (xlim[1] - xlim[0]) * 0.5
        y_range = (ylim[1] - ylim[0]) * 0.5
        z_range = (zlim[1] - zlim[0]) * 0.5

        x_center, y_center, z_center = ball_position

        ax.set_xlim([x_center - x_range / scale_factor, x_center + x_range / scale_factor])
        ax.set_ylim([y_center - y_range / scale_factor, y_center + y_range / scale_factor])
        ax.set_zlim([z_center - z_range / scale_factor, z_center + z_range / scale_factor])

        # Restore the view
        ax.view_init(elev=elev, azim=azim)

        canvas.draw()

    def on_key(event):
        nonlocal ax

        move_step = 5.0  # Define the step size for movement

        if event.keysym == 'Up':
            ax.elev += move_step
        elif event.keysym == 'Down':
            ax.elev -= move_step
        elif event.keysym == 'Left':
            ax.azim -= move_step
        elif event.keysym == 'Right':
            ax.azim += move_step

        ax.view_init(elev=ax.elev, azim=ax.azim)
        canvas.draw()

    # Bind the mouse wheel and keyboard events
    canvas.mpl_connect('scroll_event', zoom)
    root.bind('<KeyPress>', on_key)

    # Add input fields for velocity, horizontal angle, vertical angle, spin components, and initial position
    input_frame = tk.Frame(root)
    input_frame.pack(side=tk.BOTTOM, fill=tk.X)

    # Creating sub-frames for better organization
    frame1 = tk.Frame(input_frame)
    frame1.pack(side=tk.TOP, fill=tk.X)
    frame2 = tk.Frame(input_frame)
    frame2.pack(side=tk.TOP, fill=tk.X)
    frame3 = tk.Frame(input_frame)
    frame3.pack(side=tk.TOP, fill=tk.X)

    tk.Label(frame1, text="Velocity (km/h):").pack(side=tk.LEFT)
    velocity_entry = tk.Entry(frame1, width=5)
    velocity_entry.pack(side=tk.LEFT)
    velocity_entry.insert(0, '0')

    tk.Label(frame1, text="Horizontal Angle (degrees):").pack(side=tk.LEFT)
    angle_horizontal_entry = tk.Entry(frame1, width=5)
    angle_horizontal_entry.pack(side=tk.LEFT)
    angle_horizontal_entry.insert(0, '0')

    tk.Label(frame1, text="Vertical Angle (degrees):").pack(side=tk.LEFT)
    angle_vertical_entry = tk.Entry(frame1, width=5)
    angle_vertical_entry.pack(side=tk.LEFT)
    angle_vertical_entry.insert(0, '0')

    tk.Label(frame2, text="Spin X (rad/s):").pack(side=tk.LEFT)
    spin_x_entry = tk.Entry(frame2, width=5)
    spin_x_entry.pack(side=tk.LEFT)
    spin_x_entry.insert(0, '0')

    tk.Label(frame2, text="Spin Y (rad/s):").pack(side=tk.LEFT)
    spin_y_entry = tk.Entry(frame2, width=5)
    spin_y_entry.pack(side=tk.LEFT)
    spin_y_entry.insert(0, '0')

    tk.Label(frame2, text="Spin Z (rad/s):").pack(side=tk.LEFT)
    spin_z_entry = tk.Entry(frame2, width=5)
    spin_z_entry.pack(side=tk.LEFT)
    spin_z_entry.insert(0, '0')

    tk.Label(frame3, text="Initial Position X:").pack(side=tk.LEFT)
    initial_x_entry = tk.Entry(frame3, width=5)
    initial_x_entry.pack(side=tk.LEFT)
    initial_x_entry.insert(0, str(FIELD_LENGTH - 32))

    tk.Label(frame3, text="Initial Position Y:").pack(side=tk.LEFT)
    initial_y_entry = tk.Entry(frame3, width=5)
    initial_y_entry.pack(side=tk.LEFT)
    initial_y_entry.insert(0, str(FIELD_WIDTH / 2))

    tk.Label(frame3, text="Initial Position Z:").pack(side=tk.LEFT)
    initial_z_entry = tk.Entry(frame3, width=5)
    initial_z_entry.pack(side=tk.LEFT)
    initial_z_entry.insert(0, str(BALL_RADIUS))

    simulation_running = False  # Flag to track if the simulation is running
    update_id = None  # Variable to store the after id for cancelling

    # To store the trajectory
    trajectories = []

    def start_simulation():
        nonlocal ball_position, ball_velocity, ball, simulation_running, update_id, trajectories

        if simulation_running:
            root.after_cancel(update_id)  # Cancel the current update loop

        # Reset ball position and velocity
        initial_x = initial_x_entry.get()
        initial_y = initial_y_entry.get()
        initial_z = initial_z_entry.get()
        ball_position = np.array([
            float(initial_x) if initial_x else initial_ball_position[0],
            float(initial_y) if initial_y else initial_ball_position[1],
            float(initial_z) if initial_z else initial_ball_position[2]
        ], dtype=np.float64)

        ball_velocity = np.array([0, 0, 0], dtype=np.float64)
        ball = update_ball(ax, ball_position, ball)

        # Choose a random color for the new trajectory
        color = (random.random(), random.random(), random.random())
        current_trajectory = {
            'positions': [],
            'color': color
        }

        velocity_kmh = float(velocity_entry.get()) if velocity_entry.get() else 0
        angle_horizontal_deg = float(angle_horizontal_entry.get()) if angle_horizontal_entry.get() else 0
        angle_vertical_deg = float(angle_vertical_entry.get()) if angle_vertical_entry.get() else 0
        spin_x = float(spin_x_entry.get()) if spin_x_entry.get() else 0
        spin_y = float(spin_y_entry.get()) if spin_y_entry.get() else 0
        spin_z = float(spin_z_entry.get()) if spin_z_entry.get() else 0

        angle_horizontal_rad = np.radians(angle_horizontal_deg)  # Convert horizontal angle to radians
        angle_vertical_rad = np.radians(angle_vertical_deg)  # Convert vertical angle to radians

        # Convert velocity from km/h to m/s
        velocity = velocity_kmh * (1000 / 3600)  # Korrekte Umrechnung von km/h in m/s

        # Check if the velocity is zero, if so, do not start the simulation
        if velocity == 0:
            return

        # Calculate the velocity components
        ball_velocity = np.array([
            velocity * np.cos(angle_vertical_rad) * np.cos(angle_horizontal_rad),
            velocity * np.cos(angle_vertical_rad) * np.sin(angle_horizontal_rad),
            velocity * np.sin(angle_vertical_rad)
        ], dtype=np.float64)

        # Set the spin components
        ball_spin = np.array([spin_x, spin_y, spin_z], dtype=np.float64)

        simulation_running = True
        trajectories.append(current_trajectory)
        update_position(ball_spin)

    start_button = tk.Button(input_frame, text="Start Simulation", command=start_simulation)
    start_button.pack(side=tk.LEFT)

    def clear_paths():
        nonlocal trajectories
        trajectories = []
        ax.cla()
        plot_field(ax)
        add_goals(ax)
        add_wall(ax, wall_position, (FIELD_WIDTH / 2) - (wall_width / 2), (FIELD_WIDTH / 2) + (wall_width / 2), wall_height)
        canvas.draw()

    clear_button = tk.Button(input_frame, text="Clear Paths", command=clear_paths)
    clear_button.pack(side=tk.LEFT)

    def reset_ball_position():
        nonlocal ball_position, ball_velocity, ball, trajectories
        ball_position = initial_ball_position.copy()
        ball_velocity = np.array([0, 0, 0], dtype=np.float64)
        ball = update_ball(ax, ball_position, ball)

        # Clear previous trajectories
        trajectories = []
        ax.cla()
        plot_field(ax)
        add_goals(ax)
        add_wall(ax, wall_position, (FIELD_WIDTH / 2) - (wall_width / 2), (FIELD_WIDTH / 2) + (wall_width / 2), wall_height)
        ball = add_ball(ax, ball_position)

        # Clear the entry fields for initial positions
        initial_x_entry.delete(0, tk.END)
        initial_y_entry.delete(0, tk.END)
        initial_z_entry.delete(0, tk.END)

        canvas.draw()

    reset_button = tk.Button(input_frame, text="Reset Ball Position", command=reset_ball_position)
    reset_button.pack(side=tk.LEFT)

    # Initialize ball velocity
    ball_velocity = np.array([0, 0, 0], dtype=np.float64)

    # Update the ball position
    def update_position(spin):
        nonlocal ball_position, ball_velocity, ball, update_id, simulation_running

        dt = 0.1  # time step, you can increase this to slow down the simulation
        prev_ball_position = ball_position.copy()
        ball_position, ball_velocity = update_ball_position(ball_position, ball_velocity, spin, dt, wall_position, wall_height, wall_width)

        # Check if the velocity is close to zero
        if np.linalg.norm(ball_velocity) < 1e-2:  # Adjust the threshold as needed
            simulation_running = False
            return

        for traj in trajectories:
            traj['positions'].append(ball_position.copy())

        # Plot all trajectories
        for traj in trajectories:
            positions = traj['positions']
            if len(positions) > 1:
                ax.plot([p[0] for p in positions], [p[1] for p in positions], [p[2] for p in positions], color=traj['color'])

        ball = update_ball(ax, ball_position, ball)

        canvas.draw()
        update_id = root.after(50, update_position, spin)  # update every 50ms

    # Functions to set the ball to Messi's and Ronaldo's positions
    def set_position_messi():
        initial_x_entry.delete(0, tk.END)
        initial_y_entry.delete(0, tk.END)
        initial_z_entry.delete(0, tk.END)
        initial_x_entry.insert(0, '73')  # Example position
        initial_y_entry.insert(0,34)  # Example position
        initial_z_entry.insert(0, str(BALL_RADIUS))

    def set_position_ronaldo():
        initial_x_entry.delete(0, tk.END)
        initial_y_entry.delete(0, tk.END)
        initial_z_entry.delete(0, tk.END)
        initial_x_entry.insert(0, '78')  # Example position
        initial_y_entry.insert(0,28)  # Example position
        initial_z_entry.insert(0, str(BALL_RADIUS))

    # Buttons for setting positions
    messi_button = tk.Button(input_frame, text="Messi Position", command=set_position_messi)
    messi_button.pack(side=tk.LEFT)

    ronaldo_button = tk.Button(input_frame, text="Ronaldo Position", command=set_position_ronaldo)
    ronaldo_button.pack(side=tk.LEFT)

    # Start the Tkinter main loop
    root.mainloop()

if __name__ == "__main__":
    create_window()
