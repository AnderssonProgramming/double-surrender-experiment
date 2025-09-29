# Double-Slit Experiment: Quantum Mechanics Demonstration

A comprehensive project for simulating, building, and analyzing the famous double-slit experiment - one of the most important demonstrations of wave-particle duality in quantum mechanics. This project combines theoretical physics, computational simulation, and hands-on experimental work.

## Getting Started

This project provides everything you need to understand, simulate, and physically build the double-slit experiment. Whether you're a student learning about quantum mechanics or an educator demonstrating wave interference, this comprehensive toolkit will guide you through the entire process.

### Prerequisites

**For Simulation (Required):**
- Python 3.8 or higher
- Basic understanding of physics (waves, interference)
- Computer with graphics capability

**For Physical Experiment (Required):**
- Laser pointer (red, 650nm recommended)
- Cardboard and aluminum foil
- Razor blade for cutting precise slits
- Dark room or space
- White screen or wall
- Ruler and measuring tools
- Camera for documentation

**Programming Knowledge:**
- Basic Python (for using simulations)
- Matplotlib for visualization
- Jupyter notebooks (optional, for interactive exploration)

### Installing

**Step 1: Clone the Repository**

```bash
git clone https://github.com/AnderssonProgramming/double-surrender-experiment.git
cd double-surrender-experiment
```

**Step 2: Install Python Dependencies**

```bash
pip install -r requirements.txt
```

**Step 3: Test the Installation**

```bash
python double_slit_simulation.py
```

This will run the simulation demonstrations and show you sample interference patterns.

**Step 4: Explore Interactive Examples**

```bash
python examples.py
```

Or for interactive exploration, launch the Jupyter notebook:

```bash
jupyter notebook interactive_notebook.ipynb
```

**Step 5: Run Tests (Optional)**

```bash
pip install -r requirements-test.txt
python -m pytest test_double_slit.py -v
```

All tests should pass, confirming that the physics simulations are working correctly.

## Running the tests

The project includes comprehensive tests to verify the physics accuracy and functionality of the simulation library.

### Automated Tests

Run the full test suite to verify everything is working correctly:

```bash
python -m pytest test_double_slit.py -v
```

### Test Categories

**Physics Accuracy Tests:**
- Wave function calculations
- Interference pattern generation
- Fringe spacing accuracy
- Energy conservation
- Parameter scaling laws

**Simulation Functionality Tests:**
- Single vs double slit patterns
- Parameter range validation
- Edge case handling
- Data analysis tools

**Integration Tests:**
- Complete experiment simulation
- Image processing for experimental data
- Comparison between theory and experiment

### Physical Experiment Validation

After building your physical setup:

1. **Take clear photos** of your interference pattern
2. **Measure key parameters** (distances, slit dimensions)
3. **Use the analysis tools** to compare with simulation:

```python
from double_slit_simulation import InterferenceAnalyzer, DoubleslitSimulator

# Load your experimental image
analyzer = InterferenceAnalyzer()
intensity = analyzer.load_image('your_experiment_photo.jpg')

# Set up simulation with your parameters
sim = DoubleslitSimulator(
    wavelength=650e-9,        # Your laser wavelength
    slit_separation=200e-6,   # Measured slit separation
    screen_distance=1.0       # Measured distance
)

# Compare results
comparison = analyzer.compare_with_theory(sim)
print(f"Correlation with theory: {comparison['correlation']:.3f}")
```

## Deployment

### Physical Experiment Setup

This project is designed to be deployed as a complete learning experience combining simulation and hands-on experimentation.

**Classroom Deployment:**
- Each team (max 3 students) builds their own double-slit apparatus
- Use simulation library to predict expected results
- Compare experimental measurements with theoretical predictions
- Document the complete process with photos and videos

**Educational Integration:**
- Suitable for physics courses covering wave optics
- Excellent introduction to quantum mechanics concepts
- Combines theory, computation, and experimental skills
- Scalable from high school to university level

### Documentation and Reporting

Complete documentation is available in the `docs/` folder:
- Comprehensive physics background
- Detailed experimental procedures
- Analysis methodologies
- Troubleshooting guides

### Assessment Criteria

The project is evaluated on:
- **Quality of experimental setup** (construction and alignment)
- **Clear interference pattern** (visibility and symmetry)
- **Accurate measurements** (distances, fringe spacing)
- **Analysis and comparison** (simulation vs experiment)
- **Documentation** (photos, videos, lab report)

## Built With

- [Python](https://www.python.org/) - Programming language for simulations
- [NumPy](https://numpy.org/) - Scientific computing and array operations
- [Matplotlib](https://matplotlib.org/) - Plotting and visualization
- [SciPy](https://scipy.org/) - Scientific algorithms and signal processing
- [OpenCV](https://opencv.org/) - Computer vision for image analysis
- [Jupyter](https://jupyter.org/) - Interactive notebook environment

## Contributing

This project welcomes contributions from students, educators, and physics enthusiasts. Here's how you can contribute:

### Ways to Contribute

- **Improve the simulation library** with additional features
- **Add new educational examples** and demonstrations
- **Enhance the documentation** with better explanations
- **Submit experimental results** and analysis from your own setups
- **Report bugs** or suggest improvements
- **Translate documentation** to other languages

### Contribution Guidelines

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-simulation`)
3. Make your changes with clear, documented code
4. Add tests for new functionality
5. Ensure all tests pass (`python -m pytest`)
6. Submit a pull request with detailed description

### Educational Use

This project is specifically designed for educational purposes. Contributions should:
- Maintain scientific accuracy
- Include clear explanations
- Provide practical learning value
- Be accessible to students at various levels

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/AnderssonProgramming/double-surrender-experiment/tags).

## Authors

- **Physics Education Team** - *Initial development* - [AnderssonProgramming](https://github.com/AnderssonProgramming)

See also the list of [contributors](https://github.com/AnderssonProgramming/double-surrender-experiment/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details.

## Acknowledgments

- **Thomas Young** - Original double-slit experiment (1801)
- **Richard Feynman** - Popularizing the experiment's quantum mechanical implications
- **Physics educators worldwide** - For inspiring clear explanations of complex concepts
- **Open source community** - For the excellent Python scientific libraries
- **Students and educators** - Who will use this project to explore quantum mechanics

## Educational Impact

This project demonstrates that profound physics concepts can be made accessible through:
- Hands-on experimentation with simple materials
- Computational simulation and analysis
- Clear documentation and educational resources
- Interactive exploration tools

The double-slit experiment remains one of the most elegant demonstrations of quantum mechanics, showing that light exhibits both wave and particle properties. This project helps students experience this fundamental discovery firsthand.

---

**"The double-slit experiment is absolutely impossible, absolutely impossible to explain in any classical way, and [it] has in it the heart of quantum mechanics."** - Richard Feynman
