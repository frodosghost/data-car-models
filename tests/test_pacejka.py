import numpy as np
import pytest
from models.pacejka import pacejka

# Define test coefficients
B, C, D, E = 10, 1.9, 4000, 0.97

def test_pacejka_zero_slip():
    """Test if the force is zero when slip is zero."""
    assert pacejka(B, C, D, E, 0) == pytest.approx(0, abs=1e-3)

def test_pacejka_positive_slip():
    """Test if the function returns a reasonable force for a small positive slip."""
    slip = 0.05  # 5% slip
    force = pacejka(B, C, D, E, slip)
    assert force > 0, "Force should be positive for positive slip"

def test_pacejka_negative_slip():
    """Test if the function returns a negative force for a small negative slip."""
    slip = -0.05  # -5% slip
    force = pacejka(B, C, D, E, slip)
    assert force < 0, "Force should be negative for negative slip"

def test_pacejka_peak_force():
    """Test if peak force is within expected range."""
    slip_values = np.linspace(-0.2, 0.2, 100)
    forces = pacejka(B, C, D, E, slip_values)
    max_force = np.max(np.abs(forces))
    assert max_force <= D, f"Peak force {max_force} should not exceed max parameter D={D}"

def test_pacejka_monotonicity():
    """Check if force increases then decreases (basic monotonicity test)."""
    slip_values = np.linspace(0, 0.2, 100)
    forces = pacejka(B, C, D, E, slip_values)

    # Find the index of peak force
    peak_index = np.argmax(forces)

    # Ensure force increases before the peak
    assert np.all(np.diff(forces[:peak_index]) >= 0), "Force should increase before the peak"

    # Ensure force decreases after the peak
    assert np.all(np.diff(forces[peak_index:]) <= 0), "Force should decrease after the peak"
