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
There are 3 execution options:

Option 2 - For a given Sokoban board, the code will return if the board is solvable, and if so it will return the winning moves in a LURD format.

Option 3 - Comparison of runtime between BDD and SAT engines in a given board solution.

Option 4 - For a given Sokoban board, solve it in an iterative way. Every time try to solve the board for n boxes, until all the board is solve, or indicate if the board is not solvable.

### General running instructions

In this section there are general running instructions for the entire project:

The program must be run by running the file codes/main.py according to the instructions.

First, in line 36 in codes/main.py, change the value of runPart to the number 2,3 or 4 (Otherwise the program will ask you to insert a number at the beginning of the run), other values are not valid. This value will determine the part of the project that will run.

In addition, you must insert in line 37 in the codes/main.py file the file path of the Sokoban board in XSB format. Leave the letter r as it appears in the example, and put your path inside the brackets. The file must have a .txt extension. Example of a proper path:

r"C:\Users\Lenovo\Documents\aaa.txt"

After that, you must insert in line 38 in the codes/main.py file the path to which you want the smv model of the above board to be created. Leave the letter r as it appears in the example, and put your path inside the brackets. An example of a proper path:

r"C:\Users\Lenovo\Documents\aaa.smv"

### part 2

There are no additional instructions for this part other than what is noted above.
If you want, you can change the engine in which the nuXmv model will run, by changing the second parameter in the function run_nuxmv to the engine in which you want the model to run in line 43 in codes/main.py. valid options are 'bdd' or 'sat'.

### part 3

Since we were asked to analyze in this section for which engine we will get a better runtime, we decided to compare the average runtime to get a better comparison. 
You can change the number of iterations if you want in line 51 in codes/main.py. The number of iterations we chose by default is 10.

Defaultly, there is no need to input the max number of steps for running with the SAT engine. For running with a maximum amount of steps, this should be changed in line 49 in the codes/main.py file. Note that if the maximum number of steps is set to n, then a board that is solvable in more than n steps, turns to be unsolvable in this run.

### part 4

In this section on line 62 in codes/main.py, enter the number of boxes you want to be solved in each iteration (our default is 1). Be careful not to enter a number larger than the total number of boxes in the board (we did not perform such a correctness check, and it is not the purpose of the assignment either).
If you enter a value that is not perfectly divisible by the total number of boxes, the last iteration of the solution will solve the board for the remaining boxes from the remainder of the division.

The program will ask you for the engine in which you want to run the model during the program run, but this can also be changed manually in the code on line 61 in codes/main.py file.

In this part, the smv and out files will be named by concatenating : (given_file_name)_(# boxes_to_solve_per_iteration)_(# iteration). For example, if the given output filename was: r"C:\Users\Lenovo\Documents\board8.smv" & solving 2 boxes in every iteration, then the output files in the first iteration will be: 
"board8_2_boxes_IterationModel_iter1.out" & "board8_2_boxes_IterationModel_iter1.smv"

OPTION: You can choose to print in the code the initial state of the board in each iteration in XSB format. The default in the code is not to print this, but if you want to do so, you should un-comment lines 131, 132, 154, 155 in the file codes/SokobanIterativeSolver.py.

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
