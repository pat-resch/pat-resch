"""
Tyre Force Simulation using the Magic Formula
Source: SAE Transactions , 1987, Vol. 96, Section 2 (1987), pp. 190-204
Author: Patrick Resch
Student ID: p2410710037
"""

import numpy as np
import matplotlib.pyplot as plt
import argparse

# Constant Values Tyre Parameters. Source: SAE Transactions, 1987, Vol. 96, Section 2, pp. 190-204

class TyreConstants:
    """Class containing hardcoded tabular values for different vertical loads."""
    
    PARAMETERS = {
        2000: {"Bx": 10, "Cx": 1.65, "Dx": 2000, "Ex": 0.97, "By": 9, "Cy": 1.3, "Dy": 2000, "Ey": 0.9, "Sh": 0.02, "Sv": 100},
        4000: {"Bx": 9, "Cx": 1.69, "Dx": 4000, "Ex": 0.95, "By": 8, "Cy": 1.3, "Dy": 4000, "Ey": 0.88, "Sh": 0.02, "Sv": 120},
        6000: {"Bx": 8, "Cx": 1.67, "Dx": 6000, "Ex": 0.93, "By": 7, "Cy": 1.3, "Dy": 6000, "Ey": 0.85, "Sh": 0.03, "Sv": 150},
        8000: {"Bx": 7, "Cx": 1.78, "Dx": 7500, "Ex": 0.90, "By": 6, "Cy": 1.3, "Dy": 7500, "Ey": 0.83, "Sh": 0.03, "Sv": 180}
    }

# Magic Formula Implementation

class MagicFormula:
    
    def __init__(self):
                self.parameters = TyreConstants.PARAMETERS

    def compute_longitudinal_force(self, slip_ratio, vertical_load):
        
        params = self.parameters.get(vertical_load, self.parameters[2000])
        Bx, Cx, Dx, Ex = params["Bx"], params["Cx"], params["Dx"], params["Ex"]
        force_x = Dx * np.sin(Cx * np.arctan(Bx * slip_ratio - Ex * (Bx * slip_ratio - np.arctan(Bx * slip_ratio))))
        return max(force_x, 0)

    def compute_lateral_force(self, slip_ratio, vertical_load):
        
        params = self.parameters.get(vertical_load, self.parameters[2000])
        By, Cy, Dy, Ey, Sh, Sv = params["By"], params["Cy"], params["Dy"], params["Ey"], params["Sh"], params["Sv"]
        phi = (1 - Ey) * (slip_ratio + Sh) + (Ey / By) * np.arctan(By * (slip_ratio + Sh))
        force_y = Dy * np.sin(Cy * np.arctan(By * phi)) + Sv
        force_y *= np.exp(-3 * slip_ratio)  # Fy tapers to 0 at 100% Slip
        return max(force_y, 0)

# Plot- incl. multiple load cases

def plot_tyre_forces(selected_fz):

    slip_range = np.linspace(0, 1, 100)  # Value range for Slip (0% bis 100%)
    model = MagicFormula()

    plt.figure(figsize=(10, 6))

    for Fz in selected_fz:
        forces_x = [model.compute_longitudinal_force(s, Fz) for s in slip_range]
        forces_y = [model.compute_lateral_force(s, Fz) for s in slip_range]

        plt.plot(slip_range * 100, forces_x, label=f"Fx at {Fz} N")  # Brake Force (Fx)
        plt.plot(slip_range * 100, forces_y, linestyle="--", label=f"Fy at {Fz} N")  # Side Force (Fy, dotted)

    # Axis Labeling

    plt.xlabel("Longitudinal Slip [%]")
    plt.ylabel("Brake Force Fx and Side Force Fy [N]")
    plt.legend()
    plt.grid()
    plt.title("Magic Formula - Longitudinal and Lateral Forces")
    plt.show()

# Main Execution with Argparse
# Source of code lines 75 - 87: code was generated with assistance from ChatGPT (GPT-4)

def main():
    """Main function for executing the tyre force calculations."""
    
    parser = argparse.ArgumentParser(description="Compute tyre forces using Magic Formula.")
    parser.add_argument("--fz", type=int, nargs="+", default=[2000, 4000, 6000, 8000],
                        help="List of vertical loads (e.g. --fz 2000 4000)")
    
    args = parser.parse_args()
    
    plot_tyre_forces(args.fz)

if __name__ == "__main__":
    main()

