import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML

# --- SETTINGS FOR EMERGENT GALAXY ---
N_particles = 600
box_size = 150.0
dt = 0.04
steps = 600

# 1. RADIAL FORCES (Hydrodynamic attraction vs Orbital repulsion)
k_attr = 100.0
soft_attr = 5.0
k_repel = 38.0
soft_repel = 1.0

# 2. TANGENTIAL FORCE (The Fundamental Spin)
k_spin = 70.0          # Slightly increased to compensate for damping at the core
soft_spin = 3.0
spin_damping_radius = 15.0 # NEW: Distance at which spin starts proportionally dropping to zero

R_max = 60.0
damping = 0.99
thermal_noise = 3.0

# --- INITIALIZATION ---
# Starting with random positions and initial thermal movement
pos = np.random.rand(N_particles, 2) * box_size
vel = (np.random.rand(N_particles, 2) - 0.5) * thermal_noise

# ASSIGNING FUNDAMENTAL SPIN
spins = np.random.randn(N_particles) * 0.5 + 1.0

fig, ax = plt.subplots(figsize=(8, 8), facecolor='#000000')
ax.set_xlim(0, box_size); ax.set_ylim(0, box_size)
ax.set_title("Emergent Galaxy: Proportional Spin Damping", color='white', fontsize=14)
ax.set_axis_off()

scatter = ax.scatter(pos[:, 0], pos[:, 1], s=15, c='#00f2ff', edgecolors='white', linewidth=0.2, alpha=0.8)

# --- PHYSICS ENGINE ---
def update(frame):
    global pos, vel
    forces = np.zeros((N_particles, 2))

    for i in range(N_particles):
        delta = pos - pos[i]
        dist_sq = np.sum(delta**2, axis=1)
        dist = np.sqrt(dist_sq) + 0.001

        mask = (dist > 0) & (dist < R_max)
        r_sq = dist_sq[mask]
        r_actual = dist[mask]

        # Radial vector
        d_vec = delta[mask] / r_actual[:, np.newaxis]
        # Tangential vector (rotated 90 degrees)
        t_vec = np.column_stack((-d_vec[:, 1], d_vec[:, 0]))

        # Radial Forces
        f_attr = k_attr / (r_sq + soft_attr)
        f_repel = -k_repel / (r_sq + soft_repel)
        f_radial = f_attr + f_repel

        # --- NEW: PROPORTIONAL SPIN DAMPING ---
        # If distance (r_actual) > spin_damping_radius, multiplier is 1.0 (Full spin)
        # If distance gets closer to 0, multiplier drops proportionally to 0.0
        spin_multiplier = np.clip(r_actual / spin_damping_radius, 0.0, 1.0)

        # Calculate Tangential Force with the damping multiplier applied
        f_spin = (k_spin * spins[mask] * spin_multiplier) / (r_sq + soft_spin)

        # Sum vectors
        forces[i] = np.sum(d_vec * f_radial[:, np.newaxis] + t_vec * f_spin[:, np.newaxis], axis=0)

    # Thermodynamics
    random_vibration = (np.random.rand(N_particles, 2) - 0.5) * 0.1
    vel = vel * damping + forces * dt + random_vibration

    # Speed limit
    v_speed = np.linalg.norm(vel, axis=1, keepdims=True)
    vel = np.where(v_speed > 25.0, vel * (25.0 / v_speed), vel)

    pos += vel * dt

    # Boundaries
    for d in range(2):
        out_min, out_max = pos[:, d] < 0, pos[:, d] > box_size
        if np.any(out_min):
            pos[out_min, d] = 0
            vel[out_min, d] *= -0.5
        if np.any(out_max):
            pos[out_max, d] = box_size
            vel[out_max, d] *= -0.5

    scatter.set_offsets(pos)
    return scatter,

plt.close()
anim = FuncAnimation(fig, update, frames=steps, interval=30, blit=True)
HTML(anim.to_jshtml())

