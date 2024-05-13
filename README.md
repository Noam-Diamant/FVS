# The sokoban solver
In this project we present a code designed to solve boards of the Sokoban game.
The code will be run according to one of the options that will be presented, and according to the instructions that will be presented below.

For the code you wrote there are 3 execution options:

Option 2 - running the code, receiving an answer as to whether the board is solvable, and if so, in what way.

Option 3 - Comparison of runtime between BDD and SAT engines in a given board solution.

Option 4 - comparison of running time between a normal solution and an iterative solution of a given board.

## Running instructions

In this section there are general running instructions for the entire project:
First, you must insert in line 37 in the main.py file the file path of the Sokoban board in XSB format. Leave the letter r as it appears in the example, and put your path inside the brackets. The file should have a txt extension. Example of a proper path:

r"C:\Users\Lenovo\Documents\aaa.txt"

After that, you must insert in line 38 in the main.py file the path to which you want the smv model of the above board to be created. Leave the letter r as it appears in the example, and put your path inside the brackets. An example of a proper path:

r"C:\Users\Lenovo\Documents\aaa.smv"

### option 2



