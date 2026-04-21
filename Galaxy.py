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
k_repel = 60.0
soft_repel = 1.0

# 2. TANGENTIAL FORCE (The Fundamental Spin)
k_spin = 30.0          # How strongly a particle's spin drags the surrounding superfluid
soft_spin = 3.0        # Softening core for the spin effect

R_max = 60.0
damping = 0.99
thermal_noise = 3.0

# --- INITIALIZATION ---
center = box_size / 2.0
# The cloud starts with NO macro-rotation, just random thermal motion
pos = (np.random.randn(N_particles, 2) * 20.0) + center
vel = (np.random.rand(N_particles, 2) - 0.5) * thermal_noise

# ASSIGNING FUNDAMENTAL SPIN
# In a proto-galactic cloud, spontaneous symmetry breaking gives a slight dominance to one spin direction.
# Here, each particle has an intrinsic spin, mostly positive, but with individual variation.
spins = np.random.randn(N_particles) * 0.5 + 1.0

fig, ax = plt.subplots(figsize=(8, 8), facecolor='#000000')
ax.set_xlim(0, box_size); ax.set_ylim(0, box_size)
ax.set_title("Emergent Macro-Vortex from Microscopic Spin", color='white', fontsize=14)
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
        
        # Radial vector (points directly from particle i to particle j)
        d_vec = delta[mask] / dist[mask, np.newaxis]
        
        # Tangential vector (rotated 90 degrees: [-y, x])
        t_vec = np.column_stack((-d_vec[:, 1], d_vec[:, 0]))

        # Calculate Radial Forces (Push/Pull)
        f_attr = k_attr / (r_sq + soft_attr)
        f_repel = -k_repel / (r_sq + soft_repel)
        f_radial = f_attr + f_repel
        
        # Calculate Tangential Force (Spin Drag / Magnus Effect)
        # Neighboring particle j's spin creates a sweeping force on particle i
        f_spin = k_spin * spins[mask] / (r_sq + soft_spin)

        # Sum vectors: Radial Push/Pull + Tangential Swirl
        forces[i] = np.sum(d_vec * f_radial[:, np.newaxis] + t_vec * f_spin[:, np.newaxis], axis=0)

    # Apply thermodynamics
    random_vibration = (np.random.rand(N_particles, 2) - 0.5) * 0.1
    vel = vel * damping + forces * dt + random_vibration

    # Speed limit
    v_speed = np.linalg.norm(vel, axis=1, keepdims=True)
    vel = np.where(v_speed > 25.0, vel * (25.0 / v_speed), vel)

    pos += vel * dt

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
