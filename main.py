import os  # Import the os module for file operations
import time
from SokobanBoardSolver import *
import subprocess
from SokobanBoardGenerator import *

def getPart():
    print("Please choose the part you want to run,")
    validOptions = [2, 3, 4]
    while True:
        try:
            userInput = int(input("valid answers are 2, 3 or 4: "))  # Try to convert input to int
            if userInput in validOptions:
                break  # Exit the loop if input is within valid options
            else:
                print("Invalid input. Please enter 2, 3, or 4.")
        except ValueError:
            print("Invalid input. Please enter an integer.")
    return userInput

def getEngine():
    while True:
            engineType = input("Please enter which type of engine to run,\nvalid answers are SAT or BDD: ")
            if (engineType == "SAT" or engineType == "sat" or engineType.upper() == "SAT"):
                steps = int(input("Enter the desired k value: "))
                break
            elif (engineType == "BDD" or engineType == "bdd" or engineType.upper() == "BDD"):
                steps = None
                break
            else:
                print("invalid answer, try again!")
    return engineType, steps

if __name__ == '__main__':
    print("Hello, and welcome to the Sokoban solver!")
    runPart = getPart()
    path = r"C:\Users\Lenovo\OneDrive - Bar-Ilan University - Students\GitHW\FVS\bbb.smv"
    # path = r"C:\Users\אורה\FVS\bbb.smv"
    if runPart == 2:
        run_nuxmv(r"./bbb.smv")
        #getLURD Moves - ORA!!
    if runPart == 3:
        engineType, steps = getEngine()
        runTime = MeasureRunTime(path, engineType, steps)
        printMsg = f"It took {runTime:.6f} seconds to run {path} on {engineType.upper()} engine"
        print(printMsg)
    
    if runPart == 4:
        exit





   # print("Hello, and welcome to the Sokoban folder!")
    #FileNameForRead = getInputFileName()
    #b = SokobanInitialBoard(3,5)
   # b.printInitialBoard()
    #rows, columns, content = readFile(FileNameForRead)
    #b = SokobanBoard(rows, columns, content)
    #b.printBoard()
    #i , o = createSmvBoardFile()
    #i = i.replace("\\\\", "\\")
    #print(MeasureRunTime(r'C:\Users\Lenovo\OneDrive - Bar-Ilan University - Students\GitHW\FVS\bbb.smv'))
