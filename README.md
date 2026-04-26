# Newtonian-Superfluid-Simulation

## Demo






  <img src="./YouCut_20260426_134604731 (1).gif" alt="emergent universe simulation" width="700">
</p>


## Emergent Universe Simulator 
This is a model of a fluid consisting of particles interacting through attraction, repulsion and spin. The change in the overall balance of forces leads to the formation of different dynamic patterns from micro to macro space. The concept is based on experimental research into fluid dynamics.  Codes are several options for setting up the mode.  


## Physics

Particle-based simulation (N = 600) with the following local forces:

### Radial Forces
- **Attraction**: $F_{attr} = \frac{k_{attr}}{r^2 + s_{attr}}$
- **Repulsion**: $F_{repel} = -\frac{k_{repel}}{r^2 + s_{repel}}$, $F_{repel} = -\frac{k_{repel}}{r^4 + s_{repel}}$

### Tangential Spin Force (with proportional damping)
- Tangential direction: perpendicular to radial vector
- $F_{spin} = \frac{k_{spin} \cdot spin_i \cdot m}{r^2 + s_{spin}}$
- where damping multiplier $m = \min\left(\frac{r}{r_{damp}}, 1.0\right)$


### Scientific Background:
This simulation is based on the experimental research regarding the fluid dynamics and quantum physics. 
**Full paper:** [Hydrodynamic model of gravity as a secondary effect of electromagnetic dipoles and the hypothesis of superfluid space-time. (Zenodo)](https://doi.org/10.5281/zenodo.15752936)

---

## How to Run
1. Ensure you have `numpy` and `matplotlib` installed.
2. Run `simulation.py` to see the animated output.

## Try it Online

You can try for free online open source version: 

**[🌌 Universum Space Simulator](https://www.masterogon.art/index.php/universum-space-simulator/)**




