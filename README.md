# FVS: Sokoban Solver & Model Checking Project

## Overview
This project provides a comprehensive framework for solving Sokoban puzzles using formal verification and model checking techniques. It includes tools for generating Sokoban boards, encoding them into formal models, and solving them using both BDD (Binary Decision Diagram) and SAT (Boolean Satisfiability) based engines. The project is structured for experimentation, benchmarking, and analysis of different solving strategies.

## Repository Structure
- **boards/**: Contains Sokoban board definitions in `.txt` format.
- **codes/**: Python source code for board generation, encoding, and solving:
  - `main.py`: Main entry point for running experiments and solving boards.
  - `SokobanBoardGenerator.py`: Generates Sokoban boards.
  - `SokobanBoardSolver.py`: Encodes and solves boards using model checking.
  - `SokobanIterativeSolver.py`: Implements iterative solving strategies.
- **outputFiles/**: Results and outputs from experiments, organized by part:
  - `part2/`: Model files (`.smv`), solver outputs (`.out`), and visualizations (`.jpg`).
  - `part3/`: Timing results for BDD and SAT solvers (`.time`).
  - `part4/`: Iterative solution results, with deep subfolders for each board and configuration.
- **Report&Appendices/**: Project reports, documentation, and example models:
  - `FVS_Final_Project.pdf`, `report.docx`, `report.pdf`: Detailed project documentation and results.
  - `nuXmv.exe`: Model checker executable.
  - `sokoban_example.smv`: Example model file.

## How to Use
1. **Board Preparation**: Place your Sokoban board files in the `boards/` directory. Boards should be in plain text format.
2. **Running Experiments**:
   - Use `main.py` to run experiments. You can specify which board, model, and solving strategy to use by editing the script or passing arguments (see code comments for details).
   - Generated models and outputs will be saved in the appropriate `outputFiles/` subdirectory.
3. **Model Checking**:
   - The project uses `nuXmv` for model checking. Ensure `nuXmv.exe` is available (see `Report&Appendices/`).
   - Models are encoded in `.smv` files and can be run with `nuXmv` for both BDD and SAT solving.
4. **Analysis**:
   - Output files include solver logs, timing results, and solution visualizations for benchmarking and comparison.
   - Reports and appendices provide detailed explanations of methodology, experiments, and findings.

## Features
- **Flexible Board Generation**: Easily add or modify Sokoban boards for new experiments.
- **Multiple Solving Strategies**: Compare BDD and SAT-based model checking, as well as iterative approaches.
- **Automated Experimentation**: Scripts for batch processing and benchmarking across multiple boards and configurations.
- **Comprehensive Reporting**: Includes detailed documentation, results, and analysis for reproducibility.

## Requirements
- Python 3.x
- `nuXmv` model checker (included as `nuXmv.exe`)
- Standard Python libraries (see code for any additional dependencies)

## References
- See `Report&Appendices/` for full project documentation, methodology, and results.
- For more information on model checking and Sokoban, refer to the included reports and example files.

---

*This project was developed as part of a formal verification and synthesis course, focusing on the application of model checking to combinatorial puzzles.*
