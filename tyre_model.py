import numpy as np
import matplotlib.pyplot as plt
import argparse
from scipy.constants import g

# Prüfen, ob der Code als Skript ausgeführt wird
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Berechnet und plottet Brems- und Seitenkräfte basierend auf Schlupf.")
    parser.add_argument("slip", type=float, help="Schräglaufwinkel in Grad")
    parser.add_argument("mass", type=float, help="Fahrzeugmasse in kg")
    parser.add_argument("mu", type=float, help="Reibwert µ (0-1)")
    
    # Argumente parsen, aber nur, wenn das Skript über die Kommandozeile aufgerufen wird
    try:
        args = parser.parse_args()
        slip_angle = args.slip
        vehicle_mass = args.mass
        mu = args.mu
    except SystemExit:
        # Standardwerte für Debugging in Jupyter/IDE
        slip_angle = 2
        vehicle_mass = 1500
        mu = 0.8
        print("⚠️ Keine Kommandozeilenargumente! Verwende Standardwerte (slip=2, mass=1500, mu=0.8)")

# Radlast (angenommen 4 Räder, gleichmäßig verteilt)
wheel_loads = [2000, 4000, 6000, 8000]
k = np.linspace(0, 1, 100)

def magic_formula(k, D, C, B, E=0):
    phi = (1 - E) * k + (E / B) * np.arctan(B * k)
    return D * np.sin(C * np.arctan(B * phi))

# Pacejka-Parameter
C = 1.3
D_base = 1.0
E = 0

# Zwei Subplots für verschiedene Winkel
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

for idx, alpha in enumerate([slip_angle, slip_angle + 3]):  # Default: 2° & 5° simulieren
    ax = axes[idx]
    for Fz in wheel_loads:
        B = mu * 0.02 * Fz
        D = D_base * Fz
        Fy = magic_formula(k, D * np.sin(np.radians(alpha)), C, B, E)
        Fx = magic_formula(k, D, C, B, E)
        ax.plot(k * 100, Fy, label=f'Fy - {Fz}N')
        ax.plot(k * 100, Fx, '--', label=f'Fx - {Fz}N')

    ax.set_xlabel('Longitudinal Slip (%)')
    ax.set_ylabel('Force (N)')
    ax.set_title(f'Side & Brake Forces (α={alpha}°)')
    ax.legend()
    ax.grid(True)

plt.tight_layout()
plt.show()



