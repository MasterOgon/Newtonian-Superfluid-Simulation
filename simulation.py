import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML

# --- Parameters ---
N_particles = 350
box_size = 50.0
dt = 0.04
steps = 200

# Constants 
k_gravity = 100.0     # Attraction 
k_repel = 100.0       # Repulsion 
softening = 1.2      # Smoothness 
R_max = 10.0         # Interaction radius  
damping = 0.95       # Viscosity = 5
max_vel = 12.0       # Velocity 

# --- Initialization ---
pos = np.random.rand(N_particles, 2) * box_size
vel = np.zeros((N_particles, 2))

fig, ax = plt.subplots(figsize=(8, 8), facecolor='#000000')
ax.set_xlim(0, box_size)
ax.set_ylim(0, box_size)
ax.set_title("Pulsating Superfluid Medium", color='white', fontsize=14)
ax.set_axis_off()

# Particle Size  
scatter = ax.scatter(pos[:, 0], pos[:, 1], s=30, c='#00f2ff', edgecolors='white', linewidth=0.1)

def update(frame):
    global pos, vel
    forces = np.zeros((N_particles, 2))

    # Calculation of interactions
    for i in range(N_particles):
        delta = pos - pos[i]
        dist_sq = np.sum(delta**2, axis=1)
        dist = np.sqrt(dist_sq) + 0.001
        mask = (dist > 0) & (dist < R_max)

        for j in np.where(mask)[0]:
            d_sq = dist_sq[j]
            d_vec = delta[j] / dist[j]

            # Newton's gravity: 1/r^2
            f_grav = k_gravity / (d_sq + softening)

            # Repulsion: 1/r^4 
            f_repel = -k_repel / (d_sq**2 + 0.1)

            forces[i] += d_vec * (f_grav + f_repel)

    # Physics 
    vel = vel * damping + forces * dt
    # Speed limit 
    v_speed = np.linalg.norm(vel, axis=1, keepdims=True)
    vel = np.where(v_speed > max_vel, vel * (max_vel / v_speed), vel)
    pos += vel * dt

    # Reflection from boundaries  
    for d in range(2):
        out_min, out_max = pos[:, d] < 0, pos[:, d] > box_size
        if np.any(out_min): pos[out_min, d], vel[out_min, d] = 0, -vel[out_min, d] * 0.5
        if np.any(out_max): pos[out_max, d], vel[out_max, d] = box_size, -vel[out_max, d] * 0.5

    scatter.set_offsets(pos)
    return scatter,

plt.close()
anim = FuncAnimation(fig, update, frames=steps, interval=30, blit=True)
HTML(anim.to_jshtml())

