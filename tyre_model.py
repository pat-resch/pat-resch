import numpy as np
import matplotlib.pyplot as plt

def magic_formula(k,D,C,E=0):
    """
    Computes the force using Magic Formula considering logitudinal slip (k).

    Parameters:
    - k: Longitudinal Slip (array or scalar)
    - D: Peak Factor
    - B: Stiffness Factor
    - C: Shape Factor
    - E: Curvature Factor (optional, default is 0)

    Returns:
    - Computed Force Values
    """
    
    #Formula Definition
    phi=(1-E)*k+(E/B)*np.arctan(B*k)
    return D*np.sin(C*np.arctan(B*phi))

#Parameter Definition
D=1.0
C=1.3
B=10.0

#Longitudinal Slip
k=np.linspace(0, 1, 100)

#Calculation
side_force = magic_formula(k,D,C,B)
brake_force = magic_formula(k,D,C,B*1.2)

#Plotting
plt.figure(figsize=(10, 6))
plt.plot(k * 100, side_force, label='Side Force')
plt.plot(k * 100, brake_force, label='Brake Force', linestyle='--')
plt.xlabel('Longitudinal Slip (%)')
plt.ylabel('Force')
plt.title('Side and Brake Forces over Longitudinal Slip')
plt.legend()
plt.grid(True)
plt.show()
