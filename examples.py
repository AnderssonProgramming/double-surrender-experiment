"""
Interactive Examples for Double-Slit Experiment
================================================

This script provides interactive examples and demonstrations of the double-slit
experiment simulation. Run this script to see various aspects of the phenomenon.
"""

import numpy as np
import matplotlib.pyplot as plt
from double_slit_simulation import (
    DoubleslitSimulator, InterferenceAnalyzer, 
    plot_interference_pattern, create_experimental_setup_guide,
    demo_single_vs_double_slit, demo_wavelength_effects
)

def example_basic_simulation():
    """Basic example of running a double-slit simulation."""
    print("=" * 60)
    print("BASIC DOUBLE-SLIT SIMULATION")
    print("=" * 60)
    
    # Create simulator with typical laser parameters
    simulator = DoubleslitSimulator(
        wavelength=650e-9,      # Red laser (650 nm)
        slit_width=50e-6,       # 50 micrometers
        slit_separation=200e-6,  # 200 micrometers
        screen_distance=1.0     # 1 meter
    )
    
    # Run simulation
    y_positions, intensity = simulator.simulate_experiment(
        screen_width=0.01,  # 1 cm screen width
        resolution=1000     # 1000 points
    )
    
    # Plot results
    plot_interference_pattern(y_positions, intensity, 
                            "Basic Double-Slit Pattern")
    
    # Calculate some interesting properties
    y_mm = y_positions * 1000
    peaks_indices = []
    for i in range(1, len(intensity)-1):
        if intensity[i] > intensity[i-1] and intensity[i] > intensity[i+1] and intensity[i] > 0.1:
            peaks_indices.append(i)
    
    if len(peaks_indices) >= 3:
        # Calculate fringe spacing
        peak_positions = y_mm[peaks_indices]
        fringe_spacing = np.mean(np.diff(peak_positions))
        print(f"Average fringe spacing: {fringe_spacing:.2f} mm")
        
        # Theoretical fringe spacing: λD/d
        theoretical_spacing = (simulator.wave.wavelength * simulator.screen_distance / 
                             simulator.slit_separation) * 1000
        print(f"Theoretical fringe spacing: {theoretical_spacing:.2f} mm")
        print(f"Relative error: {abs(fringe_spacing - theoretical_spacing)/theoretical_spacing*100:.1f}%")

def example_parameter_effects():
    """Demonstrate how changing parameters affects the pattern."""
    print("\n" + "=" * 60)
    print("PARAMETER EFFECTS DEMONSTRATION")
    print("=" * 60)
    
    _, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # 1. Effect of slit separation
    ax = axes[0, 0]
    separations = [100e-6, 200e-6, 400e-6]  # micrometers
    for sep in separations:
        sim = DoubleslitSimulator(slit_separation=sep)
        y_pos, intensity = sim.simulate_experiment()
        ax.plot(y_pos * 1000, intensity, label=f'{sep*1e6:.0f} μm')
    ax.set_xlabel('Position (mm)')
    ax.set_ylabel('Intensity')
    ax.set_title('Effect of Slit Separation')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 2. Effect of slit width
    ax = axes[0, 1]
    widths = [30e-6, 50e-6, 100e-6]  # micrometers
    for width in widths:
        sim = DoubleslitSimulator(slit_width=width)
        y_pos, intensity = sim.simulate_experiment()
        ax.plot(y_pos * 1000, intensity, label=f'{width*1e6:.0f} μm')
    ax.set_xlabel('Position (mm)')
    ax.set_ylabel('Intensity')
    ax.set_title('Effect of Slit Width')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 3. Effect of screen distance
    ax = axes[1, 0]
    distances = [0.5, 1.0, 2.0]  # meters
    for dist in distances:
        sim = DoubleslitSimulator(screen_distance=dist)
        y_pos, intensity = sim.simulate_experiment()
        ax.plot(y_pos * 1000, intensity, label=f'{dist:.1f} m')
    ax.set_xlabel('Position (mm)')
    ax.set_ylabel('Intensity')
    ax.set_title('Effect of Screen Distance')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 4. Effect of wavelength
    ax = axes[1, 1]
    wavelengths = [450e-9, 550e-9, 650e-9]  # Blue, Green, Red
    colors = ['blue', 'green', 'red']
    for wavelength, color in zip(wavelengths, colors):
        sim = DoubleslitSimulator(wavelength=wavelength)
        y_pos, intensity = sim.simulate_experiment()
        ax.plot(y_pos * 1000, intensity, color=color, 
               label=f'{wavelength*1e9:.0f} nm')
    ax.set_xlabel('Position (mm)')
    ax.set_ylabel('Intensity')
    ax.set_title('Effect of Wavelength')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def example_experimental_analysis():
    """Example of how to analyze experimental data."""
    print("\n" + "=" * 60)
    print("EXPERIMENTAL DATA ANALYSIS EXAMPLE")
    print("=" * 60)
    
    # Create synthetic "experimental" data with some noise
    simulator = DoubleslitSimulator()
    y_pos, theoretical = simulator.simulate_experiment(resolution=500)
    
    # Add some realistic noise and measurement errors
    rng = np.random.default_rng(42)  # For reproducible results
    noise = rng.normal(0, 0.05, len(theoretical))
    experimental = theoretical + noise
    experimental = np.clip(experimental, 0, 1)  # Keep in valid range
    
    # Simulate slight parameter differences
    sim_experimental = DoubleslitSimulator(
        slit_separation=195e-6,  # Slightly different from theoretical 200μm
        slit_width=55e-6        # Slightly different from theoretical 50μm
    )
    
    # Analyze with the InterferenceAnalyzer
    analyzer = InterferenceAnalyzer()
    analyzer.experimental_data = experimental
    
    # Compare with theory
    comparison = analyzer.compare_with_theory(sim_experimental)
    
    print(f"Correlation coefficient: {comparison['correlation']:.3f}")
    print(f"RMS error: {comparison['rms_error']:.3f}")
    print(f"Number of experimental peaks: {len(comparison['experimental_peaks'])}")
    print(f"Number of theoretical peaks: {len(comparison['theoretical_peaks'])}")
    
    # Plot comparison
    plt.figure(figsize=(12, 8))
    
    plt.subplot(2, 1, 1)
    plt.plot(y_pos * 1000, experimental, 'ro-', alpha=0.7, label='Experimental Data')
    plt.plot(y_pos * 1000, analyzer.theoretical_data, 'b-', linewidth=2, label='Theoretical Fit')
    plt.xlabel('Position (mm)')
    plt.ylabel('Normalized Intensity')
    plt.title('Experimental vs Theoretical Comparison')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Mark peaks
    if comparison['experimental_peaks']:
        exp_peak_positions = y_pos[comparison['experimental_peaks']] * 1000
        exp_peak_intensities = experimental[comparison['experimental_peaks']]
        plt.plot(exp_peak_positions, exp_peak_intensities, 'rs', markersize=8, label='Exp. Peaks')
    
    if comparison['theoretical_peaks']:
        theo_peak_positions = y_pos[comparison['theoretical_peaks']] * 1000
        theo_peak_intensities = analyzer.theoretical_data[comparison['theoretical_peaks']]
        plt.plot(theo_peak_positions, theo_peak_intensities, 'b^', markersize=8, label='Theo. Peaks')
    
    plt.legend()
    
    # Residuals plot
    plt.subplot(2, 1, 2)
    residuals = experimental - analyzer.theoretical_data
    plt.plot(y_pos * 1000, residuals, 'g-', alpha=0.7)
    plt.axhline(y=0, color='k', linestyle='--', alpha=0.5)
    plt.xlabel('Position (mm)')
    plt.ylabel('Residuals')
    plt.title('Residuals (Experimental - Theoretical)')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def example_measurement_guide():
    """Provide guidance for making measurements in the physical experiment."""
    print("\n" + "=" * 60)
    print("MEASUREMENT GUIDE FOR PHYSICAL EXPERIMENT")
    print("=" * 60)
    
    guide_text = """
CRITICAL MEASUREMENTS FOR YOUR EXPERIMENT:

1. LASER WAVELENGTH:
   - Red laser pointer: ~650 nm (most common)
   - Green laser pointer: ~532 nm
   - Check specifications or assume 650 nm for red

2. SLIT DIMENSIONS:
   - Slit width: Measure with calipers if possible
   - Typical range: 20-100 micrometers
   - If unmeasurable, estimate ~50 micrometers

3. SLIT SEPARATION:
   - Distance between slit centers
   - Typical range: 100-500 micrometers
   - Critical for pattern spacing!

4. DISTANCES:
   - Laser to slits: 1-3 meters (not critical)
   - Slits to screen: 0.5-3 meters (affects pattern size)
   - Use a measuring tape for accuracy

5. PATTERN MEASUREMENTS:
   - Fringe spacing: Distance between adjacent bright fringes
   - Central maximum width: Width of the brightest central fringe
   - Number of visible fringes: Count on one side

TIPS FOR BETTER MEASUREMENTS:
- Take photos with a ruler in the image for scale
- Measure multiple fringe spacings and average them
- Record all distances carefully
- Note any asymmetries in the pattern

USING THESE MEASUREMENTS WITH THE SIMULATION:
- Input your measured values into the DoubleslitSimulator
- Compare your experimental pattern with the simulation
- Adjust parameters to get the best fit
- This helps verify your measurement accuracy!
"""
    
    print(guide_text)
    
    # Example calculation
    print("\nEXAMPLE CALCULATION:")
    print("-" * 30)
    
    # Typical experimental values
    wavelength = 650e-9  # meters
    slit_separation = 200e-6  # meters
    screen_distance = 1.5  # meters
    
    # Calculate expected fringe spacing
    fringe_spacing = wavelength * screen_distance / slit_separation
    
    print("Given:")
    print(f"  Wavelength: {wavelength*1e9:.0f} nm")
    print(f"  Slit separation: {slit_separation*1e6:.0f} μm")
    print(f"  Screen distance: {screen_distance:.1f} m")
    print(f"Expected fringe spacing: {fringe_spacing*1000:.2f} mm")
    
    print(f"\nIf you measure a fringe spacing of {fringe_spacing*1000:.2f} mm,")
    print("your setup matches the theoretical prediction!")

def run_all_examples():
    """Run all example demonstrations."""
    print("DOUBLE-SLIT EXPERIMENT SIMULATION EXAMPLES")
    print("==========================================")
    print("This script will demonstrate various aspects of the double-slit experiment.")
    print("Press Enter to continue through each example...\n")
    
    # Basic simulation
    input("Press Enter to run basic simulation...")
    example_basic_simulation()
    
    # Parameter effects
    input("\nPress Enter to see parameter effects...")
    example_parameter_effects()
    
    # Experimental analysis
    input("\nPress Enter to see experimental analysis example...")
    example_experimental_analysis()
    
    # Single vs double slit comparison
    input("\nPress Enter to see single vs double slit comparison...")
    demo_single_vs_double_slit()
    
    # Wavelength effects
    input("\nPress Enter to see wavelength effects...")
    demo_wavelength_effects()
    
    # Measurement guide
    input("\nPress Enter to see measurement guide...")
    example_measurement_guide()
    
    # Setup guide
    input("\nPress Enter to see experimental setup guide...")
    print(create_experimental_setup_guide())
    
    print("\n" + "=" * 60)
    print("ALL EXAMPLES COMPLETED!")
    print("=" * 60)
    print("Now you're ready to:")
    print("1. Build your physical double-slit setup")
    print("2. Take measurements and photos")
    print("3. Use this library to analyze your results")
    print("4. Compare theory with your experimental data")

if __name__ == "__main__":
    run_all_examples()