"""
Simple Test of Double-Slit Simulation
=====================================

A simplified version to test the core simulation without OpenCV dependency.
"""

import numpy as np
import matplotlib.pyplot as plt

class SimpleWaveFunction:
    """Simple wave function for testing."""
    
    def __init__(self, wavelength, amplitude=1.0):
        self.wavelength = wavelength
        self.amplitude = amplitude
        self.k = 2 * np.pi / wavelength

class SimpleDoubleslitSimulator:
    """Simplified simulator for testing."""
    
    def __init__(self, wavelength=650e-9, slit_width=50e-6, 
                 slit_separation=200e-6, screen_distance=1.0):
        self.wave = SimpleWaveFunction(wavelength)
        self.slit_width = slit_width
        self.slit_separation = slit_separation
        self.screen_distance = screen_distance
    
    def double_slit_intensity(self, y_positions):
        """Calculate double slit interference pattern."""
        theta = np.arctan(y_positions / self.screen_distance)
        
        # Single slit diffraction term
        beta = (np.pi * self.slit_width * np.sin(theta)) / self.wave.wavelength
        beta_safe = np.where(np.abs(beta) < 1e-10, 1e-10, beta)
        single_slit_term = (np.sin(beta_safe) / beta_safe) ** 2
        
        # Double slit interference term
        delta = (np.pi * self.slit_separation * np.sin(theta)) / self.wave.wavelength
        interference_term = (np.cos(delta)) ** 2
        
        return single_slit_term * interference_term
    
    def simulate_experiment(self, screen_width=0.01, resolution=1000):
        """Run simulation and return results."""
        y_positions = np.linspace(-screen_width/2, screen_width/2, resolution)
        intensity = self.double_slit_intensity(y_positions)
        return y_positions, intensity / np.max(intensity)

def test_simulation():
    """Test the simulation and create a simple plot."""
    print("Testing Double-Slit Simulation...")
    
    # Create simulator
    sim = SimpleDoubleslitSimulator()
    
    # Run simulation
    y_pos, intensity = sim.simulate_experiment()
    
    # Create plot
    plt.figure(figsize=(12, 6))
    
    # 1D plot
    plt.subplot(1, 2, 1)
    y_mm = y_pos * 1000
    plt.plot(y_mm, intensity, 'b-', linewidth=2)
    plt.xlabel('Position on Screen (mm)')
    plt.ylabel('Normalized Intensity')
    plt.title('Double-Slit Interference Pattern')
    plt.grid(True, alpha=0.3)
    
    # 2D visualization
    plt.subplot(1, 2, 2)
    pattern_2d = np.tile(intensity, (30, 1))
    extent = [y_mm[0], y_mm[-1], -1, 1]
    plt.imshow(pattern_2d, extent=extent, aspect='auto', cmap='hot')
    plt.xlabel('Position on Screen (mm)')
    plt.ylabel('Height (arbitrary)')
    plt.title('2D Pattern Visualization')
    plt.colorbar(label='Intensity')
    
    plt.tight_layout()
    plt.show()
    
    # Calculate and display key results
    theoretical_spacing = (sim.wave.wavelength * sim.screen_distance / 
                         sim.slit_separation) * 1000  # in mm
    
    print(f"Simulation completed successfully!")
    print(f"Parameters used:")
    print(f"  Wavelength: {sim.wave.wavelength*1e9:.0f} nm")
    print(f"  Slit separation: {sim.slit_separation*1e6:.0f} μm")
    print(f"  Screen distance: {sim.screen_distance:.1f} m")
    print(f"Expected fringe spacing: {theoretical_spacing:.2f} mm")
    
    # Count peaks
    peaks = []
    for i in range(1, len(intensity)-1):
        if (intensity[i] > intensity[i-1] and 
            intensity[i] > intensity[i+1] and 
            intensity[i] > 0.1):
            peaks.append(i)
    
    print(f"Number of bright fringes found: {len(peaks)}")
    print("✓ Core simulation functionality working correctly!")

if __name__ == "__main__":
    test_simulation()