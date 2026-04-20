import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML

# --- SETTINGS FOR THE SUPERFLUID UNIVERSE ---
# Increase N to see more complex vortex structures (filaments)
N_particles = 400
box_size = 10.0
dt = 0.04              # Simulation step (smoothness of motion)
steps = 400

# --- THE "HYPOTHESIS" PARAMETERS ---
# 1. ATTRACTION (Bjerknes Force / Gravity)
# This represents the low-pressure zones or cavitation collapse
k_attr = 100.0
soft_attr = 2.0        # "Blurring" of gravity at the center

# 2. REPULSION (Orbital Resonance / Electric Charge)
# IMPORTANT: Using Power 2 (1/r^2) to match Attraction power.
# This balance creates the "Matter as a Process" effect from the paper.
k_repel = 10.0
soft_repel = 0.1       # Repulsion is "sharper" than attraction to create a core

# 3. ENVIRONMENT
R_max = 22.0           # Reach of interaction (defines filament length)
damping = 0.98         # Higher value = less friction (more "Superfluid")
thermal_noise = 10.0    # Initial "Heat" to trigger the vortex formation

# --- INITIALIZATION ---
# Starting with random positions and initial thermal movement
pos = np.random.rand(N_particles, 2) * box_size
vel = (np.random.rand(N_particles, 2) - 0.5) * thermal_noise

fig, ax = plt.subplots(figsize=(8, 8), facecolor='#000000')
ax.set_xlim(0, box_size)
ax.set_ylim(0, box_size)
ax.set_title("Vortex Matter Evolution (Equal Force Powers 1/r²)", color='white', fontsize=12)
ax.set_axis_off()

# Blue glow for the vortex cores
scatter = ax.scatter(pos[:, 0], pos[:, 1], s=25, c='#00f2ff', edgecolors='white', linewidth=0.2, alpha=0.8)

def update(frame):
    global pos, vel
    forces = np.zeros((N_particles, 2))

    for i in range(N_particles):
        delta = pos - pos[i]
        dist_sq = np.sum(delta**2, axis=1)
        dist = np.sqrt(dist_sq) + 0.001

        # Interaction mask: only particles within R_max see each other
        mask = (dist > 0) & (dist < R_max)

        r_sq = dist_sq[mask]
        d_vec = delta[mask] / dist[mask, np.newaxis]

        # EQUAL POWER CALCULATION (Both are 1/r^2)
        # Attraction represents cavitation (Bjerknes)
        f_attr = k_attr / (r_sq + soft_attr)

        # Repulsion represents orbital dipoles (Coulomb)
        # Higher k_repel makes the "atom" larger
        f_repel = -k_repel / (r_sq + soft_repel)

        # Combine forces into a single vector
        forces[i] = np.sum(d_vec * (f_attr + f_repel)[:, np.newaxis], axis=0)

    # ADDING THE "PROCESS": Tiny random fluctuations like in real superfluid
    random_vibration = (np.random.rand(N_particles, 2) - 0.5) * 0.2

    # Physics step: momentum + forces + heat
    vel = vel * damping + forces * dt + random_vibration

    # Preventing "Hyper-speed" errors
    v_speed = np.linalg.norm(vel, axis=1, keepdims=True)
    vel = np.where(v_speed > 14.0, vel * (14.0 / v_speed), vel)

    pos += vel * dt

    # BOUNCE OFF WALLS
    for d in range(2):
        out_min, out_max = pos[:, d] < 0, pos[:, d] > box_size
        if np.any(out_min): pos[out_min, d], vel[out_min, d] = 0, -vel[out_min, d] * 0.5
        if np.any(out_max): pos[out_max, d], vel[out_max, d] = box_size, -vel[out_max, d] * 0.5

    scatter.set_offsets(pos)
    return scatter,

plt.close()
anim = FuncAnimation(fig, update, frames=steps, interval=30, blit=True)
HTML(anim.to_jshtml())
