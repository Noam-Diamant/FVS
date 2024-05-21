# The sokoban solver
In this project we present a code designed to solve boards of the Sokoban game.
The code will run according to one of the options that will be presented, and according to the instructions that will be presented below.

There are 3 execution options:

Option 2 - For a given Sokoban board, the code will return if the board is solvable, and if so it will return the winning moves in a LURD format.

Option 3 - Comparison of runtime between BDD and SAT engines in a given board solution.

Option 4 - For a given Sokoban board, solve it in an iterative way. Every time try to solve the board for n boxes, until all the board is solve, or indicate if the board is not solvable.

## Running instructions

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

In this part, the smv and out files will be named by concatenating : (given_file_name)_(# boxes_to_solve_per_iteration)_(# iteration). For example, if the given output filename was: r"C:\Users\Lenovo\Documents\board8.smv" & solving 2 boxes in every iteration, then the output files in the firs iteration will be: 
"board8_2_boxes_IterationModel_iter1.out" & "board8_2_boxes_IterationModel_iter1.smv"

OPTION: You can choose to print in the code the initial state of the board in each iteration in XSB format. The default in the code is not to print this, but if you want to do so, you should un-comment lines 131, 132, 154, 155 in the file codes/SokobanIterativeSolver.py.

## An explanation of the files in this repo

### boards

Contains all the different boards we used in XSB format in txt files. Some of these boards are the boards that appeared in the assignment and some of them are boards that we wrote ourselves. In general, the level of difficulty in the boards increases as you progress.

### codes

Contains all the Python files we wrote to run the program. The program must be run by running the file main.py according to the above instructions.

### Report&Appendices

This folder contains the assignment and the summary report we wrote. In addition it includes the nuXmv software, and the functional demonstration of the transition relations of the model as explained in the first part of the report.

### outputFiles

Contains all the output files for the different parts of the project and as will be detailed.

#### part 2

In this section there are .smv, .out, .jpg files for all boards.
The .smv files are the models built for each board, the .out files are the output files received from running nuXmv on each of these models, and the .jpg files are images that contain the solution for each board in LURD format if it is solvable, otherwise a message that is not solvable.

#### part 3

In this section there are .time files that can be opened in any text reader.
These files contain the output for running the runtime analysis in both engines, for each of the boards.
As mentioned, we averaged the running time for each run over 10 iterations.

#### part 4

In this section there is an analysis of the running time for each board, for every number of goals to be solved in each iteration.
For every board, there are several folders according to the number of goals solved in each iteration. Each such folder contains the .smv files which are the models of each of the iterations, the .out files which are the solutions of each of the iterations, and the .iterative file (which can be opened in any reader text), which contain runtime analysis for each of the iterations and for the total runtime.

An example of the entire explanation written above:

For board 4, there is a folder named after it:

outputFiles/part4/board4


Since there are 4 goals in total in board 4, one or two or three goals can be solved in each iteration (in the case of three, the remainder, which is the remaining goal, will be solved in the second iteration). For each of these options there is a folder:

outputFiles/part4/board4/n_boxes_per_iter

where n is the number of goals solved in a single iteration.

This folder contains the model files of the various iterations (.smv files), the solutions of the models from each iteration (.out files), and an .iterative file containing the runtime analysis as above.
