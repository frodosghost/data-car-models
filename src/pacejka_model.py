import numpy as np
import matplotlib.pyplot as plt
from models.pacejka import pacejka


# Generate slip ratio values (-20% to 20%)
slip_ratio = np.linspace(-0.2, 0.2, 100)

# Example Pacejka coefficients
B, C, D, E = 10, 1.9, 4000, 0.97  # Adjust these values for different behaviors

# Compute longitudinal force
Fx = pacejka(B, C, D, E, slip_ratio)

# Plot the Pacejka curve
plt.figure(figsize=(8, 5))
plt.plot(slip_ratio, Fx, 'b', linewidth=2)
plt.xlabel("Slip Ratio")
plt.ylabel("Longitudinal Force (N)")
plt.title("Pacejka Tire Model - Longitudinal Force")
plt.grid()
plt.savefig('src/results/pacejka_tire_model_longitudinal_force.png')
plt.show()
