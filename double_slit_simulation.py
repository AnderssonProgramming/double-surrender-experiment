"""
Double Slit Experiment Simulation Library
=========================================

A Python library for simulating and analyzing the double-slit experiment,
one of the most fundamental demonstrations of quantum mechanics and wave-particle duality.

This library provides tools for:
- Simulating wave interference patterns
- Calculating diffraction patterns for single and double slits
- Analyzing experimental data from physical double-slit setups
- Visualizing interference patterns with customizable parameters

Classes:
    DoubleslitSimulator: Main simulation class
    WaveFunction: Represents electromagnetic waves
    InterferenceAnalyzer: Analyzes experimental data
    
Functions:
    calculate_intensity_pattern: Calculates the intensity distribution
    generate_slit_pattern: Creates slit geometries
    plot_interference: Visualization utilities
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from typing import Tuple, Optional, List
import cv2

class WaveFunction:
    """
    Represents an electromagnetic wave for the double-slit experiment.
    
    Attributes:
        wavelength (float): Wavelength of the light in meters
        amplitude (float): Wave amplitude
        frequency (float): Wave frequency in Hz
    """
    
    def __init__(self, wavelength: float, amplitude: float = 1.0):
        """
        Initialize a wave function.
        
        Args:
            wavelength: Wavelength in meters (e.g., 650e-9 for red laser)
            amplitude: Wave amplitude (default: 1.0)
        """
        self.wavelength = wavelength
        self.amplitude = amplitude
        self.frequency = 3e8 / wavelength  # c / lambda
        self.k = 2 * np.pi / wavelength    # wave number
    
    def phase_at_point(self, distance: float) -> float:
        """Calculate phase at a given distance from source."""
        return self.k * distance
    
    def amplitude_at_point(self, distance: float) -> complex:
        """Calculate complex amplitude at a point."""
        phase = self.phase_at_point(distance)
        return self.amplitude * np.exp(1j * phase)

class DoubleslitSimulator:
    """
    Main simulator for the double-slit experiment.
    
    This class handles the setup and calculation of interference patterns
    for both single and double-slit configurations.
    """
    
    def __init__(self, 
                 wavelength: float = 650e-9,  # Red laser wavelength
                 slit_width: float = 50e-6,   # 50 micrometers
                 slit_separation: float = 200e-6,  # 200 micrometers
                 screen_distance: float = 1.0):  # 1 meter
        """
        Initialize the double-slit simulator.
        
        Args:
            wavelength: Light wavelength in meters
            slit_width: Width of each slit in meters
            slit_separation: Distance between slit centers in meters
            screen_distance: Distance from slits to screen in meters
        """
        self.wave = WaveFunction(wavelength)
        self.slit_width = slit_width
        self.slit_separation = slit_separation
        self.screen_distance = screen_distance
        
    def single_slit_intensity(self, y_positions: np.ndarray) -> np.ndarray:
        """
        Calculate intensity pattern for a single slit.
        
        Args:
            y_positions: Array of y-coordinates on the screen
            
        Returns:
            Array of intensity values
        """
        # Angle from center to each position
        theta = np.arctan(y_positions / self.screen_distance)
        
        # Single slit diffraction formula
        beta = (np.pi * self.slit_width * np.sin(theta)) / self.wave.wavelength
        
        # Avoid division by zero
        beta_safe = np.where(np.abs(beta) < 1e-10, 1e-10, beta)
        
        # Intensity pattern: I = I0 * (sin(beta)/beta)^2
        intensity = (np.sin(beta_safe) / beta_safe) ** 2
        
        return intensity
    
    def double_slit_intensity(self, y_positions: np.ndarray) -> np.ndarray:
        """
        Calculate intensity pattern for double slits.
        
        Args:
            y_positions: Array of y-coordinates on the screen
            
        Returns:
            Array of intensity values
        """
        # Angle from center to each position
        theta = np.arctan(y_positions / self.screen_distance)
        
        # Single slit diffraction term
        beta = (np.pi * self.slit_width * np.sin(theta)) / self.wave.wavelength
        beta_safe = np.where(np.abs(beta) < 1e-10, 1e-10, beta)
        single_slit_term = (np.sin(beta_safe) / beta_safe) ** 2
        
        # Double slit interference term
        delta = (np.pi * self.slit_separation * np.sin(theta)) / self.wave.wavelength
        interference_term = (np.cos(delta)) ** 2
        
        # Combined intensity
        intensity = single_slit_term * interference_term
        
        return intensity
    
    def fraunhofer_diffraction(self, y_positions: np.ndarray, 
                             double_slit: bool = True) -> np.ndarray:
        """
        Calculate the Fraunhofer diffraction pattern.
        
        Args:
            y_positions: Array of y-coordinates on screen
            double_slit: If True, calculate double-slit pattern; if False, single-slit
            
        Returns:
            Normalized intensity array
        """
        if double_slit:
            intensity = self.double_slit_intensity(y_positions)
        else:
            intensity = self.single_slit_intensity(y_positions)
            
        # Normalize to maximum intensity of 1
        return intensity / np.max(intensity)
    
    def simulate_experiment(self, screen_width: float = 0.01, 
                          resolution: int = 1000,
                          double_slit: bool = True) -> Tuple[np.ndarray, np.ndarray]:
        """
        Run a complete simulation of the experiment.
        
        Args:
            screen_width: Width of the screen in meters (default: 1cm)
            resolution: Number of points to calculate
            double_slit: Whether to simulate double or single slit
            
        Returns:
            Tuple of (y_positions, intensity_pattern)
        """
        # Create array of y-positions on the screen
        y_positions = np.linspace(-screen_width/2, screen_width/2, resolution)
        
        # Calculate intensity pattern
        intensity = self.fraunhofer_diffraction(y_positions, double_slit)
        
        return y_positions, intensity

class InterferenceAnalyzer:
    """
    Analyzes experimental data from physical double-slit experiments.
    """
    
    def __init__(self):
        self.experimental_data = None
        self.theoretical_data = None
    
    def load_image(self, image_path: str) -> np.ndarray:
        """
        Load and process an experimental interference pattern image.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Processed grayscale intensity array
        """
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Could not load image: {image_path}")
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Extract central horizontal line (where interference pattern is clearest)
        height, width = gray.shape
        center_line = gray[height//2, :]
        
        # Normalize intensity
        intensity = center_line.astype(float) / 255.0
        
        self.experimental_data = intensity
        return intensity
    
    def extract_line_profile(self, image: np.ndarray, 
                           start_point: Tuple[int, int],
                           end_point: Tuple[int, int]) -> np.ndarray:
        """
        Extract intensity profile along a line in the image.
        
        Args:
            image: Input image array
            start_point: (x, y) coordinates of line start
            end_point: (x, y) coordinates of line end
            
        Returns:
            Intensity profile along the line
        """
        # Create line coordinates
        x0, y0 = start_point
        x1, y1 = end_point
        
        num_points = int(np.sqrt((x1-x0)**2 + (y1-y0)**2))
        x_coords = np.linspace(x0, x1, num_points).astype(int)
        y_coords = np.linspace(y0, y1, num_points).astype(int)
        
        # Extract intensity values
        intensity_profile = image[y_coords, x_coords]
        
        return intensity_profile.astype(float) / 255.0
    
    def find_peaks_and_minima(self, intensity: np.ndarray) -> Tuple[List[int], List[int]]:
        """
        Find peaks (maxima) and minima in the intensity pattern.
        
        Args:
            intensity: Intensity array
            
        Returns:
            Tuple of (peak_indices, minima_indices)
        """
        # Find peaks
        peaks, _ = signal.find_peaks(intensity, height=0.1, distance=10)
        
        # Find minima by inverting the signal
        minima, _ = signal.find_peaks(-intensity, height=-0.9, distance=10)
        
        return peaks.tolist(), minima.tolist()
    
    def compare_with_theory(self, simulator: DoubleslitSimulator,
                          screen_width: float = 0.01) -> dict:
        """
        Compare experimental data with theoretical prediction.
        
        Args:
            simulator: DoubleslitSimulator instance with matching parameters
            screen_width: Width of experimental screen in meters
            
        Returns:
            Dictionary with comparison results
        """
        if self.experimental_data is None:
            raise ValueError("No experimental data loaded")
        
        # Generate theoretical pattern
        resolution = len(self.experimental_data)
        y_pos, theoretical = simulator.simulate_experiment(screen_width, resolution)
        
        self.theoretical_data = theoretical
        
        # Calculate correlation coefficient
        correlation = np.corrcoef(self.experimental_data, theoretical)[0, 1]
        
        # Calculate RMS error
        rms_error = np.sqrt(np.mean((self.experimental_data - theoretical)**2))
        
        # Find peaks in both patterns
        exp_peaks, exp_minima = self.find_peaks_and_minima(self.experimental_data)
        theo_peaks, theo_minima = self.find_peaks_and_minima(theoretical)
        
        return {
            'correlation': correlation,
            'rms_error': rms_error,
            'experimental_peaks': exp_peaks,
            'theoretical_peaks': theo_peaks,
            'experimental_minima': exp_minima,
            'theoretical_minima': theo_minima
        }

def plot_interference_pattern(y_positions: np.ndarray, 
                            intensity: np.ndarray,
                            title: str = "Double-Slit Interference Pattern",
                            save_path: Optional[str] = None) -> None:
    """
    Plot the interference pattern.
    
    Args:
        y_positions: Array of y-coordinates in meters
        intensity: Intensity values
        title: Plot title
        save_path: Optional path to save the figure
    """
    plt.figure(figsize=(12, 8))
    
    # Convert positions to millimeters for better readability
    y_mm = y_positions * 1000
    
    plt.subplot(2, 1, 1)
    plt.plot(y_mm, intensity, 'b-', linewidth=2)
    plt.xlabel('Position on Screen (mm)')
    plt.ylabel('Normalized Intensity')
    plt.title(f'{title} - Intensity Profile')
    plt.grid(True, alpha=0.3)
    
    # 2D visualization
    plt.subplot(2, 1, 2)
    # Create 2D pattern by repeating the 1D pattern
    pattern_2d = np.tile(intensity, (50, 1))
    extent = [y_mm[0], y_mm[-1], -1, 1]
    plt.imshow(pattern_2d, extent=extent, aspect='auto', cmap='hot')
    plt.xlabel('Position on Screen (mm)')
    plt.ylabel('Height (arbitrary)')
    plt.title(f'{title} - 2D Visualization')
    plt.colorbar(label='Intensity')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()

def create_experimental_setup_guide() -> str:
    """
    Generate a comprehensive guide for building the physical experiment.
    
    Returns:
        Formatted string with setup instructions
    """
    guide = """
# Physical Double-Slit Experiment Setup Guide

## Materials Needed:
1. **Laser pointer** (red, 650nm wavelength preferred)
2. **Cardboard or foam board** (for the slit holder)
3. **Aluminum foil** (to create the slits)
4. **Razor blade or X-acto knife** (to cut precise slits)
5. **White screen or wall** (to observe the pattern)
6. **Ruler and caliper** (for measurements)
7. **Camera** (to record the pattern)
8. **Dark room or low light environment**

## Step-by-Step Instructions:

### 1. Prepare the Slit Apparatus
- Cut a rectangular piece of cardboard (10cm x 15cm)
- Cover one side completely with aluminum foil
- Using a razor blade, carefully cut two parallel slits in the foil
- **Slit specifications:**
  - Width: ~0.05mm (as thin as possible)
  - Separation: ~0.2mm (distance between centers)
  - Length: ~10mm (vertical)

### 2. Setup the Experiment
- Place the laser 2-3 meters from the slit apparatus
- Position the slit apparatus perpendicular to the laser beam
- Place a white screen 1-2 meters beyond the slits
- Ensure the room is as dark as possible

### 3. Alignment
- Turn on the laser and aim it at the center of the slits
- Adjust the position until you see the interference pattern on the screen
- Fine-tune the alignment for the clearest pattern

### 4. Observation and Recording
- Observe the alternating bright and dark fringes
- Take photos of the pattern from different distances
- Record videos showing the setup and resulting pattern
- Measure the fringe spacing with a ruler

### 5. Data Collection
- Measure distances: laser to slits, slits to screen
- Measure slit width and separation (use calipers if available)
- Count the number of visible fringes
- Measure the spacing between bright fringes

## Safety Notes:
- Never look directly into the laser beam
- Handle the razor blade carefully when cutting slits
- Ensure the laser is pointed away from people

## Expected Results:
You should observe:
- Central bright maximum
- Alternating bright and dark fringes on both sides
- Fringes becoming dimmer with distance from center
- Pattern that matches the simulation from this library

## Troubleshooting:
- **No pattern visible:** Check slit alignment, room darkness
- **Pattern too blurry:** Slits may be too wide or alignment off
- **Weak pattern:** Increase screen distance or use better laser
"""
    return guide

# Example usage and demonstration functions
def demo_single_vs_double_slit():
    """Demonstrate the difference between single and double-slit patterns."""
    simulator = DoubleslitSimulator()
    
    # Single slit
    y_pos, single_intensity = simulator.simulate_experiment(double_slit=False)
    
    # Double slit
    y_pos, double_intensity = simulator.simulate_experiment(double_slit=True)
    
    # Plot comparison
    plt.figure(figsize=(15, 6))
    
    plt.subplot(1, 2, 1)
    plt.plot(y_pos * 1000, single_intensity, 'r-', linewidth=2)
    plt.xlabel('Position (mm)')
    plt.ylabel('Intensity')
    plt.title('Single Slit Diffraction')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(1, 2, 2)
    plt.plot(y_pos * 1000, double_intensity, 'b-', linewidth=2)
    plt.xlabel('Position (mm)')
    plt.ylabel('Intensity')
    plt.title('Double Slit Interference')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def demo_wavelength_effects():
    """Demonstrate how different wavelengths affect the pattern."""
    wavelengths = [450e-9, 550e-9, 650e-9]  # Blue, Green, Red
    colors = ['blue', 'green', 'red']
    labels = ['Blue (450nm)', 'Green (550nm)', 'Red (650nm)']
    
    plt.figure(figsize=(12, 8))
    
    for i, (wavelength, color, label) in enumerate(zip(wavelengths, colors, labels)):
        simulator = DoubleslitSimulator(wavelength=wavelength)
        y_pos, intensity = simulator.simulate_experiment()
        
        plt.plot(y_pos * 1000, intensity, color=color, linewidth=2, label=label)
    
    plt.xlabel('Position on Screen (mm)')
    plt.ylabel('Normalized Intensity')
    plt.title('Double-Slit Patterns for Different Wavelengths')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

if __name__ == "__main__":
    # Run demonstrations
    print("Double-Slit Experiment Simulation Library")
    print("=========================================")
    print()
    print("Running demonstrations...")
    
    demo_single_vs_double_slit()
    demo_wavelength_effects()
    
    # Print setup guide
    print(create_experimental_setup_guide())