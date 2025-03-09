import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from models.pacejka import pacejka, pacejka_fit


# Generate slip ratio values (-20% to 20%)
slip_ratio = np.linspace(-0.2, 0.2, 100)

# True Pacejka coefficients (ground truth)
B_true, C_true, D_true, E_true = 12, 1.8, 3500, 0.95

# Example Pacejka coefficients
B, C, D, E = 10, 1.9, 4000, 0.97  # Adjust these values for different behaviors

# Compute longitudinal force
true_forces = pacejka(B_true, C_true, D_true, E_true, slip_ratio)
noisy_forces = true_forces + np.random.normal(scale=150, size=len(slip_ratio))

plt.scatter(slip_ratio, noisy_forces, label="Noisy Data", color='red', alpha=0.6)
plt.plot(slip_ratio, true_forces, label="True Pacejka Model", color='blue', linewidth=2)
plt.xlabel("Slip Ratio")
plt.ylabel("Longitudinal Force (N)")
plt.legend()
plt.title("Simulated Tire Force Data with Noise")
plt.grid()
plt.savefig('src/results/pacejka_tire_model_with_noise.png')
plt.show()





# Initial guesses for B, C, D, E (could be random or based on prior knowledge)
initial_guess = [10, 2, 4000, 1]

# Perform curve fitting
fitted_params, covariance = curve_fit(pacejka_fit, slip_ratio, noisy_forces, p0=initial_guess)

# Extract fitted coefficients
B_fit, C_fit, D_fit, E_fit = fitted_params

print(f"Fitted Parameters: B={B_fit:.2f}, C={C_fit:.2f}, D={D_fit:.2f}, E={E_fit:.2f}")

# Compute fitted curve
fitted_forces = pacejka(B_fit, C_fit, D_fit, E_fit, slip_ratio)

# Plot comparison
plt.scatter(slip_ratio, noisy_forces, label="Noisy Data", color='red', alpha=0.6)
plt.plot(slip_ratio, true_forces, label="True Model", color='blue', linewidth=2)
plt.plot(slip_ratio, fitted_forces, label="Fitted Model", color='green', linestyle='dashed', linewidth=2)
plt.xlabel("Slip Ratio")
plt.ylabel("Longitudinal Force (N)")
plt.legend()
plt.title("Fitting Pacejka Model to Data")
plt.grid()
plt.savefig('src/results/pacejka_tire_model_curve_fit.png')
plt.show()
