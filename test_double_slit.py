"""
Test Suite for Double-Slit Experiment Simulation Library
========================================================

This module contains comprehensive tests for the double_slit_simulation library.
Tests cover basic functionality, edge cases, and physics accuracy.

Run with: python -m pytest test_double_slit.py -v
"""

import pytest
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for testing
import matplotlib.pyplot as plt
from double_slit_simulation import (
    WaveFunction, DoubleslitSimulator, InterferenceAnalyzer,
    plot_interference_pattern, create_experimental_setup_guide
)

class TestWaveFunction:
    """Test the WaveFunction class."""
    
    def test_initialization(self):
        """Test WaveFunction initialization with valid parameters."""
        wavelength = 650e-9
        amplitude = 1.5
        wave = WaveFunction(wavelength, amplitude)
        
        assert abs(wave.wavelength - wavelength) < 1e-15
        assert abs(wave.amplitude - amplitude) < 1e-15
        assert abs(wave.frequency - 3e8/wavelength) < 1e6  # Within 1MHz
        assert abs(wave.k - 2*np.pi/wavelength) < 1e-6
    
    def test_default_amplitude(self):
        """Test default amplitude setting."""
        wave = WaveFunction(500e-9)
        assert abs(wave.amplitude - 1.0) < 1e-15
    
    def test_phase_calculation(self):
        """Test phase calculation at different distances."""
        wave = WaveFunction(500e-9)
        
        # At distance = 0, phase should be 0
        assert wave.phase_at_point(0) == 0
        
        # At distance = wavelength, phase should be 2π
        phase_at_wavelength = wave.phase_at_point(wave.wavelength)
        assert abs(phase_at_wavelength - 2*np.pi) < 1e-10
    
    def test_amplitude_at_point(self):
        """Test complex amplitude calculation."""
        wave = WaveFunction(500e-9, amplitude=2.0)
        
        # At distance = 0, complex amplitude should equal real amplitude
        amp_at_zero = wave.amplitude_at_point(0)
        assert abs(amp_at_zero - 2.0) < 1e-10
        assert abs(amp_at_zero.imag) < 1e-10
        
        # At distance = wavelength/4, should be purely imaginary
        amp_at_quarter = wave.amplitude_at_point(wave.wavelength/4)
        assert abs(amp_at_quarter.real) < 1e-10
        assert abs(abs(amp_at_quarter.imag) - 2.0) < 1e-10

class TestDoubleslitSimulator:
    """Test the DoubleslitSimulator class."""
    
    def test_initialization(self):
        """Test simulator initialization with default and custom parameters."""
        # Default parameters
        sim_default = DoubleslitSimulator()
        assert sim_default.wave.wavelength == 650e-9
        assert sim_default.slit_width == 50e-6
        assert sim_default.slit_separation == 200e-6
        assert sim_default.screen_distance == 1.0
        
        # Custom parameters
        sim_custom = DoubleslitSimulator(
            wavelength=500e-9,
            slit_width=30e-6,
            slit_separation=150e-6,
            screen_distance=2.0
        )
        assert sim_custom.wave.wavelength == 500e-9
        assert sim_custom.slit_width == 30e-6
        assert sim_custom.slit_separation == 150e-6
        assert sim_custom.screen_distance == 2.0
    
    def test_single_slit_intensity(self):
        """Test single slit diffraction calculation."""
        sim = DoubleslitSimulator()
        y_positions = np.linspace(-0.005, 0.005, 100)  # ±5mm
        
        intensity = sim.single_slit_intensity(y_positions)
        
        # Check basic properties
        assert len(intensity) == len(y_positions)
        assert np.all(intensity >= 0)  # Intensity should be non-negative
        assert np.max(intensity) <= 1.0  # Should be normalized
        
        # Central maximum should be at center (y=0)
        center_idx = len(y_positions) // 2
        assert intensity[center_idx] == np.max(intensity)
        
        # Pattern should be symmetric
        left_half = intensity[:center_idx]
        right_half = intensity[center_idx+1:][::-1]  # Reverse right half
        if len(left_half) == len(right_half):
            assert np.allclose(left_half, right_half, rtol=1e-10)
    
    def test_double_slit_intensity(self):
        """Test double slit interference calculation."""
        sim = DoubleslitSimulator()
        y_positions = np.linspace(-0.005, 0.005, 100)
        
        intensity = sim.double_slit_intensity(y_positions)
        
        # Basic checks
        assert len(intensity) == len(y_positions)
        assert np.all(intensity >= 0)
        assert np.max(intensity) <= 1.0
        
        # Should have multiple peaks (interference fringes)
        peaks = []
        for i in range(1, len(intensity)-1):
            if (intensity[i] > intensity[i-1] and 
                intensity[i] > intensity[i+1] and 
                intensity[i] > 0.1):
                peaks.append(i)
        
        assert len(peaks) >= 3  # Should have at least central + 2 side peaks
        
        # Central peak should be brightest
        center_idx = len(y_positions) // 2
        assert intensity[center_idx] == np.max(intensity)
    
    def test_fraunhofer_diffraction(self):
        """Test Fraunhofer diffraction calculation."""
        sim = DoubleslitSimulator()
        y_positions = np.linspace(-0.01, 0.01, 200)
        
        # Test both single and double slit
        single_pattern = sim.fraunhofer_diffraction(y_positions, double_slit=False)
        double_pattern = sim.fraunhofer_diffraction(y_positions, double_slit=True)
        
        # Both should be normalized to max = 1
        assert abs(np.max(single_pattern) - 1.0) < 1e-10
        assert abs(np.max(double_pattern) - 1.0) < 1e-10
        
        # Double slit should have more structure (more peaks)
        single_peaks = np.sum(np.diff(np.sign(np.diff(single_pattern))) < 0)
        double_peaks = np.sum(np.diff(np.sign(np.diff(double_pattern))) < 0)
        assert double_peaks > single_peaks
    
    def test_simulate_experiment(self):
        """Test complete experiment simulation."""
        sim = DoubleslitSimulator()
        
        # Test with different parameters
        y_pos, intensity = sim.simulate_experiment(
            screen_width=0.02,  # 2cm
            resolution=500,
            double_slit=True
        )
        
        assert len(y_pos) == 500
        assert len(intensity) == 500
        assert np.min(y_pos) == -0.01  # -1cm
        assert np.max(y_pos) == 0.01   # +1cm
        assert np.all(intensity >= 0)
        assert abs(np.max(intensity) - 1.0) < 1e-10
    
    def test_fringe_spacing_accuracy(self):
        """Test that calculated fringe spacing matches theory."""
        wavelength = 650e-9
        slit_separation = 200e-6
        screen_distance = 1.0
        
        sim = DoubleslitSimulator(
            wavelength=wavelength,
            slit_separation=slit_separation,
            screen_distance=screen_distance
        )
        
        y_pos, intensity = sim.simulate_experiment(
            screen_width=0.02, resolution=2000
        )
        
        # Find peaks
        peaks = []
        for i in range(1, len(intensity)-1):
            if (intensity[i] > intensity[i-1] and 
                intensity[i] > intensity[i+1] and 
                intensity[i] > 0.3):  # Only bright peaks
                peaks.append(i)
        
        if len(peaks) >= 3:
            # Calculate experimental fringe spacing
            peak_positions = y_pos[peaks]
            fringe_spacings = np.diff(peak_positions)
            avg_fringe_spacing = np.mean(fringe_spacings)
            
            # Theoretical fringe spacing
            theoretical_spacing = wavelength * screen_distance / slit_separation
            
            # Should agree within 1%
            relative_error = abs(avg_fringe_spacing - theoretical_spacing) / theoretical_spacing
            assert relative_error < 0.01

class TestInterferenceAnalyzer:
    """Test the InterferenceAnalyzer class."""
    
    def test_initialization(self):
        """Test analyzer initialization."""
        analyzer = InterferenceAnalyzer()
        assert analyzer.experimental_data is None
        assert analyzer.theoretical_data is None
    
    def test_find_peaks_and_minima(self):
        """Test peak and minima detection."""
        analyzer = InterferenceAnalyzer()
        
        # Create test data with known peaks
        x = np.linspace(0, 4*np.pi, 100)
        test_intensity = 0.5 + 0.4 * np.cos(x)  # Cosine with offset
        
        peaks, minima = analyzer.find_peaks_and_minima(test_intensity)
        
        # Should find approximately 4 peaks and 4 minima
        assert len(peaks) >= 3
        assert len(minima) >= 3
        
        # Peaks should have higher intensity than minima
        if len(peaks) > 0 and len(minima) > 0:
            avg_peak_intensity = np.mean(test_intensity[peaks])
            avg_minima_intensity = np.mean(test_intensity[minima])
            assert avg_peak_intensity > avg_minima_intensity
    
    def test_compare_with_theory(self):
        """Test comparison between experimental and theoretical data."""
        # Create synthetic experimental data
        sim = DoubleslitSimulator()
        y_pos, theoretical = sim.simulate_experiment(resolution=200)
        
        # Add some realistic noise
        rng = np.random.default_rng(42)
        noise = rng.normal(0, 0.05, len(theoretical))
        experimental = theoretical + noise
        experimental = np.clip(experimental, 0, 1)
        
        # Analyze
        analyzer = InterferenceAnalyzer()
        analyzer.experimental_data = experimental
        
        comparison = analyzer.compare_with_theory(sim)
        
        # Check results structure
        assert 'correlation' in comparison
        assert 'rms_error' in comparison
        assert 'experimental_peaks' in comparison
        assert 'theoretical_peaks' in comparison
        
        # With small noise, correlation should be high
        assert comparison['correlation'] > 0.95
        assert comparison['rms_error'] < 0.1
    
    def test_extract_line_profile(self):
        """Test line profile extraction from images."""
        analyzer = InterferenceAnalyzer()
        
        # Create test image
        test_image = np.zeros((100, 200), dtype=np.uint8)
        # Add a diagonal line with varying intensity
        for i in range(100):
            for j in range(200):
                if abs(j - i*2) < 5:  # Diagonal line
                    test_image[i, j] = int(255 * (0.5 + 0.5 * np.cos(j * 0.1)))
        
        # Extract line profile
        profile = analyzer.extract_line_profile(
            test_image, (0, 0), (199, 99)
        )
        
        assert len(profile) > 0
        assert np.all(profile >= 0)
        assert np.all(profile <= 1)

class TestUtilityFunctions:
    """Test utility functions."""
    
    def test_plot_interference_pattern(self):
        """Test plotting function doesn't crash."""
        # Generate test data
        sim = DoubleslitSimulator()
        y_pos, intensity = sim.simulate_experiment()
        
        # Test plotting (should not raise exception)
        try:
            plot_interference_pattern(y_pos, intensity)
            plt.close('all')  # Clean up
        except Exception as e:
            pytest.fail(f"plot_interference_pattern raised {e}")
    
    def test_create_experimental_setup_guide(self):
        """Test setup guide generation."""
        guide = create_experimental_setup_guide()
        
        assert isinstance(guide, str)
        assert len(guide) > 1000  # Should be substantial
        assert "Materials Needed" in guide
        assert "Step-by-Step" in guide
        assert "Safety" in guide

class TestPhysicsAccuracy:
    """Test that simulations produce physically correct results."""
    
    def test_energy_conservation(self):
        """Test that total intensity is conserved in interference."""
        sim = DoubleslitSimulator()
        
        # Single slit
        y_pos, single_intensity = sim.simulate_experiment(
            double_slit=False, resolution=1000, screen_width=0.02
        )
        
        # Double slit  
        y_pos, double_intensity = sim.simulate_experiment(
            double_slit=True, resolution=1000, screen_width=0.02
        )
        
        # Integrate intensity (approximate total power)
        dy = y_pos[1] - y_pos[0]
        single_power = np.sum(single_intensity) * dy
        double_power = np.sum(double_intensity) * dy
        
        # For two identical slits, total power should be ~4x single slit
        # (factor of 2 for two slits, factor of 2 for coherent addition)
        # In practice, finite slit width modifies this slightly
        assert 3.0 < double_power / single_power < 5.0
    
    def test_scaling_laws(self):
        """Test that patterns scale correctly with parameters."""
        base_sim = DoubleslitSimulator(
            wavelength=650e-9,
            slit_separation=200e-6,
            screen_distance=1.0
        )
        
        # Double the wavelength
        wavelength_sim = DoubleslitSimulator(
            wavelength=1300e-9,  # 2x wavelength
            slit_separation=200e-6,
            screen_distance=1.0
        )
        
        # Get fringe positions for both
        y_pos, base_intensity = base_sim.simulate_experiment(resolution=1000)
        y_pos, wave_intensity = wavelength_sim.simulate_experiment(resolution=1000)
        
        # Find first peak positions (excluding central peak)
        def find_first_peak(intensity, y_positions):
            center_idx = len(intensity) // 2
            for i in range(center_idx + 10, len(intensity) - 1):
                if (intensity[i] > intensity[i-1] and 
                    intensity[i] > intensity[i+1] and 
                    intensity[i] > 0.3):
                    return y_positions[i]
            return None
        
        base_peak = find_first_peak(base_intensity, y_pos)
        wave_peak = find_first_peak(wave_intensity, y_pos)
        
        if base_peak is not None and wave_peak is not None:
            # Peak position should scale linearly with wavelength
            scaling_factor = wave_peak / base_peak
            assert 1.8 < scaling_factor < 2.2  # Should be close to 2.0
    
    def test_small_angle_approximation(self):
        """Test that small angle approximation is valid in simulation."""
        sim = DoubleslitSimulator()
        y_pos, intensity = sim.simulate_experiment(screen_width=0.01)  # ±5mm
        
        # Calculate maximum angle
        max_y = np.max(np.abs(y_pos))
        max_angle = np.arctan(max_y / sim.screen_distance)
        
        # For small angle approximation to be valid, angle should be < 0.1 rad
        assert max_angle < 0.1
        
        # sin(θ) ≈ tan(θ) ≈ θ for small angles
        sin_theta = max_y / np.sqrt(max_y**2 + sim.screen_distance**2)
        tan_theta = max_y / sim.screen_distance
        
        relative_error = abs(sin_theta - tan_theta) / sin_theta
        assert relative_error < 0.01  # Less than 1% error

def test_parameter_ranges():
    """Test simulation with various realistic parameter ranges."""
    # Test different wavelengths (visible light)
    wavelengths = [400e-9, 550e-9, 700e-9]  # Blue to red
    
    # Test different slit separations
    separations = [100e-6, 200e-6, 500e-6]  # 100-500 μm
    
    # Test different screen distances
    distances = [0.5, 1.0, 2.0]  # 0.5-2 meters
    
    for wavelength in wavelengths:
        for separation in separations:
            for distance in distances:
                sim = DoubleslitSimulator(
                    wavelength=wavelength,
                    slit_separation=separation,
                    screen_distance=distance
                )
                
                # Should not crash and produce reasonable results
                y_pos, intensity = sim.simulate_experiment()
                
                assert len(y_pos) > 0
                assert len(intensity) > 0
                assert np.all(intensity >= 0)
                assert np.max(intensity) <= 1.0

if __name__ == "__main__":
    # Run tests if script is executed directly
    pytest.main([__file__, "-v"])