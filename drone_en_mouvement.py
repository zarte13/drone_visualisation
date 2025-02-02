import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import Polygon, Arrow

# Create figure and axis
fig, ax = plt.subplots()
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)
ax.set_aspect('equal')

# Initialize drone components
drone_body, = ax.plot([], [], 'k-', linewidth=2)  # Drone body
rotor1, = ax.plot([], [], 'b-', linewidth=2)  # Rotors
rotor2, = ax.plot([], [], 'b-', linewidth=2)
drone_connector1, = ax.plot([], [], 'k-', linewidth=2)
drone_connector2, = ax.plot([], [], 'k-', linewidth=2)
wire, = ax.plot([], [], 'k--')  # Wire

# Create trapezoid payload
trapezoid_width_top = 0.8
trapezoid_width_bottom = 0.4
trapezoid_height = 0.6
vertices = np.array([
    [-trapezoid_width_top/2, 0],  # Top left
    [trapezoid_width_top/2, 0],   # Top right
    [trapezoid_width_bottom/2, -trapezoid_height],  # Bottom right
    [-trapezoid_width_bottom/2, -trapezoid_height]  # Bottom left
])
payload = Polygon(vertices, facecolor='red', edgecolor='darkred')
ax.add_patch(payload)

# Animation parameters
drone_size = 1.3
wire_length = 1.6

# Initialize acceleration arrow (it will be updated in animate)
accel_arrow = None
payload_arrow = None

def init():
    drone_body.set_data([], [])
    rotor1.set_data([], [])
    rotor2.set_data([], [])
    drone_connector1.set_data([], [])
    drone_connector2.set_data([], [])
    wire.set_data([], [])
    payload.set_xy(vertices)
    return drone_body, rotor1, rotor2, wire, payload, drone_connector1, drone_connector2

def animate(frame):
    global accel_arrow, payload_arrow
    
    # Drone motion parameters
    t = frame / 50
    x = 0  # Horizontal motion
    y = 2 + 1 * np.cos(2*t)  # Vertical motion
    
    # Calculate acceleration (second derivative of position)
    acceleration = -4 * np.cos(2*t)  # Second derivative of y
    
    # Scale factor for the arrow length
    arrow_scale = 0.2
    arrow_length = acceleration * arrow_scale
    
    # Update acceleration arrow
    if accel_arrow is not None:
        accel_arrow.remove()
    accel_arrow = Arrow(x, y, 0, arrow_length, 
                       width=0.3, 
                       color='green' if arrow_length > 0 else 'green')
    ax.add_patch(accel_arrow)
    
    # Drone body coordinates
    drone_x = [x - drone_size/2, x + drone_size/2]
    drone_y = [y, y]

    # Rotor coordinates
    rotor1_x = [x - drone_size/2-0.5, x - drone_size/2]
    rotor1_y = [y+0.2, y+0.2]
    
    rotor2_x = [x + drone_size/2, x + drone_size/2+0.5]
    rotor2_y = [y+0.2, y+0.2]

    drone_connector1_x = [x - drone_size/2, (x - drone_size/2-0.5+x - drone_size/2)/2]
    drone_connector1_y = [y, y+0.2]

    drone_connector2_x = [x + drone_size/2,(x + drone_size/2+ x + drone_size/2+0.5)/2]
    drone_connector2_y = [y, y+0.2]
    
    # Payload motion (with delay and swing effect)
    payload_x = x + 0 * np.sin(t - 0.5)
    payload_y = y - wire_length + 0.1 * np.cos(2*t - 0.5)
    
    # Update trapezoid vertices
    new_vertices = vertices + [payload_x, payload_y]
    payload.set_xy(new_vertices)
    
    # Update plot components
    drone_body.set_data(drone_x, drone_y)
    rotor1.set_data(rotor1_x, rotor1_y)
    rotor2.set_data(rotor2_x, rotor2_y)
    drone_connector1.set_data(drone_connector1_x, drone_connector1_y)
    drone_connector2.set_data(drone_connector2_x, drone_connector2_y)
    wire.set_data([x, payload_x], [y, payload_y])
    
    if payload_arrow is not None:
        payload_arrow.remove()
    payload_arrow = Arrow(payload_x, payload_y-trapezoid_height, 0, -0.5,  # Fixed length of -0.5
                         width=0.2, 
                         color='blue')
    ax.add_patch(payload_arrow)
    
    return drone_body, rotor1, rotor2, wire, payload, accel_arrow,drone_connector2,drone_connector1, payload_arrow

# Create animation
anim = FuncAnimation(fig, animate, init_func=init,
                    frames=200, interval=20, blit=True)


plt.grid(False)
plt.title('Drone avec payload')
plt.xlabel('Position en X')
plt.ylabel('Position en Y')
plt.show()

writer = PillowWriter(fps=30, metadata=dict(
    title='Drone avec payload',
    author='Philippe Lebel',
    description='Animation de drone avec payload et acceleration du drone et flèche affiché'
))
anim.save('drone_animation_2.gif', writer=writer)