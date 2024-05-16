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

First, in line 36, change the value of runPart to the number 2,3 or 4 (Otherwise the program will ask you to insert a number at the beginning of the run), other values are not valid. This value will determine the part of the project that will run.

In addition, you must insert in line 37 in the main.py file the file path of the Sokoban board in XSB format. Leave the letter r as it appears in the example, and put your path inside the brackets. The file should have a txt extension. Example of a proper path:

r"C:\Users\Lenovo\Documents\aaa.txt"

After that, you must insert in line 38 in the main.py file the path to which you want the smv model of the above board to be created. Leave the letter r as it appears in the example, and put your path inside the brackets. An example of a proper path:

r"C:\Users\Lenovo\Documents\aaa.smv"

### option 2

There are no additional instructions for this part other than what is noted above.
If you want, you can change the engine in which the nuXmv model will run, by changing the parameter to the engine in which you want the model to run in line 43.

### option 3

Since we were asked to analyze in this section for which engine we will get a better runtime, we decided to compare the average runtime to get a better comparison. You can change the number of iterations if you want in line 51. The number of iterations we chose by default is 10.
Defaultly, there is no need to input the max number of steps for running with the SAT engine. For running with a maximum amount of steps, this should be changed in line 49 in the main.py file. Note that if the maximum number of steps is set to n, then a board that is solvable in more than n steps, turns to be unsolvable in this run.

### option 4



### option 4
In this section on line 61, enter the number of boxes you want to be solved in each iteration (we entered the value 1, but can be changed to any value). Be careful not to enter a value that is greater than the total number of boxes in the board (we did not perform such a correctness check, and it is not the purpose of the assignment either), as this is against the purpose of this part of solving in iterations.
If you enter a value that is not perfectly divisible by the total number of boxes, the last iteration of the solution will solve the board for the remaining boxes from the remainder of the division.


