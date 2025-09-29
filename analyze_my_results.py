"""
Results Analysis Template for Double-Slit Experiment
===================================================

This script provides a template for analyzing your experimental results
and comparing them with the theoretical simulation.

Fill in your measured values and run this script to get a complete analysis.
"""

import numpy as np
import matplotlib.pyplot as plt
from double_slit_simulation import DoubleslitSimulator, InterferenceAnalyzer, plot_interference_pattern

# ================================================================
# EXPERIMENTAL PARAMETERS - FILL IN YOUR MEASURED VALUES
# ================================================================

# Your measured distances (in meters)
LASER_TO_SLITS_DISTANCE = 2.0      # Distance from laser to slits
SLITS_TO_SCREEN_DISTANCE = 1.5     # Distance from slits to screen
SCREEN_WIDTH_OBSERVED = 0.02       # Width of screen you observed (2cm)

# Your laser specifications
LASER_WAVELENGTH = 650e-9           # Wavelength in meters (650nm for red laser)

# Your slit dimensions (estimates are OK if precise measurement unavailable)
SLIT_WIDTH = 50e-6                  # Width of each slit in meters (50 micrometers)
SLIT_SEPARATION = 200e-6            # Distance between slit centers (200 micrometers)

# Your experimental observations
MEASURED_FRINGE_SPACING = 4.9       # Fringe spacing you measured in mm
OBSERVED_FRINGE_COUNT = 7           # Number of bright fringes you counted (one side)
PATTERN_QUALITY = "good"            # "excellent", "good", "fair", or "poor"

# Uncertainties (estimate if unsure)
DISTANCE_UNCERTAINTY = 0.01         # ±1cm for distance measurements
FRINGE_SPACING_UNCERTAINTY = 0.2    # ±0.2mm for fringe spacing
SLIT_SEPARATION_UNCERTAINTY = 50e-6 # ±50μm for slit separation

# ================================================================
# ANALYSIS FUNCTIONS
# ================================================================

def calculate_theoretical_predictions():
    """Calculate what the theory predicts for your setup."""
    
    print("THEORETICAL PREDICTIONS")
    print("=" * 50)
    
    # Basic fringe spacing formula: λD/d
    theoretical_fringe_spacing = (LASER_WAVELENGTH * SLITS_TO_SCREEN_DISTANCE / 
                                SLIT_SEPARATION)
    
    # Angular fringe spacing
    angular_spacing = LASER_WAVELENGTH / SLIT_SEPARATION
    angular_spacing_degrees = angular_spacing * 180 / np.pi
    
    # Number of fringes in observed width
    theoretical_fringe_count = int(SCREEN_WIDTH_OBSERVED / (2 * theoretical_fringe_spacing))
    
    print(f"Expected fringe spacing: {theoretical_fringe_spacing*1000:.2f} mm")
    print(f"Angular fringe spacing: {angular_spacing_degrees:.3f} degrees")
    print(f"Expected fringe count (one side): ~{theoretical_fringe_count}")
    print(f"Central fringe width: {2*theoretical_fringe_spacing*1000:.2f} mm")
    
    return theoretical_fringe_spacing, theoretical_fringe_count

def compare_with_experiment(theoretical_fringe_spacing):
    """Compare theoretical predictions with your measurements."""
    
    print("\nCOMPARISON WITH EXPERIMENT")
    print("=" * 50)
    
    # Convert measured spacing to meters
    measured_spacing_m = MEASURED_FRINGE_SPACING / 1000
    
    # Calculate relative error
    relative_error = abs(measured_spacing_m - theoretical_fringe_spacing) / theoretical_fringe_spacing
    absolute_error = abs(measured_spacing_m - theoretical_fringe_spacing) * 1000  # in mm
    
    print(f"Measured fringe spacing: {MEASURED_FRINGE_SPACING:.2f} ± {FRINGE_SPACING_UNCERTAINTY:.1f} mm")
    print(f"Theoretical fringe spacing: {theoretical_fringe_spacing*1000:.2f} mm")
    print(f"Absolute error: {absolute_error:.2f} mm")
    print(f"Relative error: {relative_error*100:.1f}%")
    
    # Assessment
    if relative_error < 0.05:
        print("✓ EXCELLENT agreement with theory!")
    elif relative_error < 0.15:
        print("✓ GOOD agreement with theory")
    elif relative_error < 0.30:
        print("⚠ FAIR agreement - some systematic error likely")
    else:
        print("⚠ POOR agreement - check measurements and setup")
    
    return relative_error

def estimate_slit_separation_from_data():
    """Estimate your actual slit separation from measured fringe spacing."""
    
    print("\nSLIT SEPARATION ESTIMATION")
    print("=" * 50)
    
    # Use measured fringe spacing to estimate actual slit separation
    measured_spacing_m = MEASURED_FRINGE_SPACING / 1000
    estimated_slit_separation = (LASER_WAVELENGTH * SLITS_TO_SCREEN_DISTANCE / 
                                measured_spacing_m)
    
    print(f"Estimated from your measurements:")
    print(f"Slit separation: {estimated_slit_separation*1e6:.1f} μm")
    print(f"Original estimate: {SLIT_SEPARATION*1e6:.1f} μm")
    
    difference = abs(estimated_slit_separation - SLIT_SEPARATION) * 1e6
    print(f"Difference: {difference:.1f} μm")
    
    return estimated_slit_separation

def run_simulation():
    """Run the simulation with your parameters."""
    
    print("\nRUNNING SIMULATION")
    print("=" * 50)
    
    # Create simulator with your parameters
    simulator = DoubleslitSimulator(
        wavelength=LASER_WAVELENGTH,
        slit_width=SLIT_WIDTH,
        slit_separation=SLIT_SEPARATION,
        screen_distance=SLITS_TO_SCREEN_DISTANCE
    )
    
    # Generate pattern
    y_positions, intensity = simulator.simulate_experiment(
        screen_width=SCREEN_WIDTH_OBSERVED,
        resolution=1000
    )
    
    # Plot the results
    plot_interference_pattern(
        y_positions, intensity,
        title=f"Simulated Pattern for Your Setup\n" +
              f"λ={LASER_WAVELENGTH*1e9:.0f}nm, d={SLIT_SEPARATION*1e6:.0f}μm, D={SLITS_TO_SCREEN_DISTANCE:.1f}m"
    )
    
    return y_positions, intensity

def error_analysis():
    """Perform error analysis on your measurements."""
    
    print("\nERROR ANALYSIS")
    print("=" * 50)
    
    # Propagate uncertainties in fringe spacing calculation
    # Δy = λD/d, so δ(Δy)/Δy = sqrt((δD/D)² + (δd/d)²)
    # (wavelength uncertainty is negligible)
    
    relative_distance_error = DISTANCE_UNCERTAINTY / SLITS_TO_SCREEN_DISTANCE
    relative_slit_error = SLIT_SEPARATION_UNCERTAINTY / SLIT_SEPARATION
    
    relative_fringe_error = np.sqrt(relative_distance_error**2 + relative_slit_error**2)
    absolute_fringe_error = relative_fringe_error * (LASER_WAVELENGTH * SLITS_TO_SCREEN_DISTANCE / 
                                                   SLIT_SEPARATION) * 1000  # in mm
    
    print(f"Sources of uncertainty:")
    print(f"  Distance measurement: ±{DISTANCE_UNCERTAINTY*100:.0f} cm ({relative_distance_error*100:.1f}%)")
    print(f"  Slit separation: ±{SLIT_SEPARATION_UNCERTAINTY*1e6:.0f} μm ({relative_slit_error*100:.1f}%)")
    print(f"  Combined fringe spacing uncertainty: ±{absolute_fringe_error:.2f} mm")
    print(f"  Your measurement uncertainty: ±{FRINGE_SPACING_UNCERTAINTY:.1f} mm")
    
    if FRINGE_SPACING_UNCERTAINTY > absolute_fringe_error:
        print("⚠ Your measurement uncertainty is larger than expected from setup")
        print("  Consider improving measurement technique")
    else:
        print("✓ Your measurement uncertainty is reasonable")

def generate_report_summary():
    """Generate a summary for your lab report."""
    
    print("\nLAB REPORT SUMMARY")
    print("=" * 50)
    
    theoretical_spacing, theoretical_count = calculate_theoretical_predictions()
    relative_error = compare_with_experiment(theoretical_spacing)
    estimated_separation = estimate_slit_separation_from_data()
    
    print(f"\nSUMMARY FOR REPORT:")
    print(f"- Setup: λ={LASER_WAVELENGTH*1e9:.0f}nm laser, screen distance {SLITS_TO_SCREEN_DISTANCE:.1f}m")
    print(f"- Theoretical fringe spacing: {theoretical_spacing*1000:.2f}mm")
    print(f"- Measured fringe spacing: {MEASURED_FRINGE_SPACING:.2f}±{FRINGE_SPACING_UNCERTAINTY:.1f}mm")
    print(f"- Relative error: {relative_error*100:.1f}%")
    print(f"- Pattern quality: {PATTERN_QUALITY}")
    print(f"- Estimated actual slit separation: {estimated_separation*1e6:.1f}μm")
    
    # Suggestions for discussion
    print(f"\nPOSSIBLE DISCUSSION POINTS:")
    if relative_error > 0.15:
        print("- Large error suggests systematic issues (measurement, alignment, slit quality)")
    if PATTERN_QUALITY in ["fair", "poor"]:
        print("- Poor pattern quality could be due to wide slits, misalignment, or ambient light")
    print("- Compare single vs double slit behavior")
    print("- Discuss quantum mechanical interpretation")
    print("- Consider improvements for future experiments")

def main():
    """Run the complete analysis."""
    
    print("DOUBLE-SLIT EXPERIMENT ANALYSIS")
    print("=" * 50)
    print("Analyzing your experimental results...")
    print()
    
    # Run all analysis functions
    theoretical_spacing, theoretical_count = calculate_theoretical_predictions()
    relative_error = compare_with_experiment(theoretical_spacing)
    estimated_separation = estimate_slit_separation_from_data()
    error_analysis()
    
    # Run simulation
    y_positions, intensity = run_simulation()
    
    # Generate report summary
    generate_report_summary()
    
    print("\nAnalysis complete! Use these results in your lab report.")
    print("Don't forget to include:")
    print("- Photos of your setup and interference pattern")
    print("- Discussion of any discrepancies")
    print("- Suggestions for experimental improvements")

if __name__ == "__main__":
    main()