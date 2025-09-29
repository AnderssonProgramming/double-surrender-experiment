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
python -c "from double_slit_simulation import DoubleslitSimulator; print('✅ Installation successful!')"
```

This will verify that the core simulation library is working correctly.

**Step 4: Start Interactive Exploration**

Launch the Jupyter notebook for interactive exploration:

```bash
jupyter notebook interactive_notebook.ipynb
```

The notebook contains all examples, demonstrations, and educational content in one place.

## Project Structure

The project has been streamlined for optimal usability:

```
double-surrender-experiment/
├── double_slit_simulation.py     # Core physics simulation library
├── interactive_notebook.ipynb    # Educational interface & examples
├── requirements.txt              # Python dependencies
├── README.md                     # This documentation
└── LICENSE                       # GPL-3.0 license
```

### Validation and Testing

The simulation accuracy can be verified through the interactive notebook, which includes:
- Physics accuracy demonstrations
- Comparison with theoretical predictions
- Interactive parameter exploration
- Visual validation of results

### Physical Experiment Integration

After building your physical setup:

1. **Take clear photos** of your interference pattern
2. **Measure key parameters** (distances, slit dimensions)
3. **Use the simulation tools** to compare with theory:

```python
from double_slit_simulation import DoubleslitSimulator, InterferenceAnalyzer

# Set up simulation with your measured parameters
sim = DoubleslitSimulator(
    wavelength=650e-9,        # Your laser wavelength (nm)
    slit_separation=200e-6,   # Measured slit separation (μm)
    screen_distance=1.0       # Measured distance (m)
)

# Generate theoretical pattern
y_pos, intensity = sim.simulate_experiment(screen_width=0.01, resolution=1000)

# Analyze and compare (visual comparison through notebook)
analyzer = InterferenceAnalyzer()
analysis = analyzer.analyze_fringe_spacing(y_pos, intensity)
print(f"Predicted fringe spacing: {analysis['fringe_spacing']*1000:.2f} mm")
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

All documentation is integrated into the interactive notebook:
- Comprehensive physics background
- Step-by-step simulation procedures  
- Interactive analysis tools
- Educational explanations and examples

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
- [Jupyter](https://jupyter.org/) - Interactive notebook environment
- [ipywidgets](https://ipywidgets.readthedocs.io/) - Interactive widgets for education

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
4. Test functionality using the notebook examples
5. Verify core simulation works (`python -c "from double_slit_simulation import DoubleslitSimulator; DoubleslitSimulator()"`)
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

- **Andersson David Sánchez Méndez** - *Initial development* - [AnderssonProgramming](https://github.com/AnderssonProgramming)  

- **Cristian Santiago Pedraza Rodríguez** - *Initial development* - [Cris-ECI](https://github.com/cris-eci)

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE.md](LICENSE) file for details.

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
