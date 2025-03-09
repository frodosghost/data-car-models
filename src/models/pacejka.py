import numpy as np

"""
B is the stiffness factor.
C is the shape factor.
D is the peak force.
E is the curvature factor.
"""
def pacejka(B, C, D, E, slip):
    """Pacejka 'Magic Formula' for tire force modeling"""
    return D * np.sin(C * np.arctan(B * slip - E * (B * slip - np.arctan(B * slip))))

# Curve Fitting inline function for Pacejka model
def pacejka_fit(slip, B, C, D, E):
    return pacejka(B, C, D, E, slip)