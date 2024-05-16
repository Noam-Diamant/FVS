import os  # Import the os module for file operations
import time
from SokobanBoardSolver import *
import subprocess
from SokobanBoardGenerator import *
from SokobanIterativeSolver import *

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
                break
            elif (engineType == "BDD" or engineType == "bdd" or engineType.upper() == "BDD"):
                steps = None
                break
            else:
                print("invalid answer, try again!")
    return engineType

if __name__ == '__main__':
    print("Hello, and welcome to the Sokoban solver!")
    runPart = getPart()
    inputFilePath = r"C:\Users\Lenovo\Documents\FVS\boards\board4.txt"#**************YOUR FILE HERE***************
    modelFilePath = r"C:\Users\Lenovo\Documents\FVS\outputFiles\part4\board4.smv"#**************YOUR PATH TO THE SMV MOODEL HERE***************
    modelFileName = rf"{modelFilePath.split('.')[0]}"

    if runPart == 2:
        createSmvBoardFile(inputFilePath, modelFilePath)
        outputFilePath = run_nuxmv(modelFilePath, 'sat')
        get_board_result(outputFilePath)#r"./da.out")

    if runPart == 3:
        createSmvBoardFile(inputFilePath, modelFilePath)
        engineType = getEngine()
        steps=None ###############Optional: Enter a selected number of steps here (defualt is None)##########
        avergeTime = 0
        iters = 10 ######################optional: insert HERE number######################
        for iter in range(iters):
            runTime, _ = MeasureRunTime(modelFilePath, engineType, steps)
            printMsg = f"It took {runTime:.6f} seconds to run {modelFilePath} on {engineType.upper()} engine on iteration {iter+1}."
            print(printMsg)
            avergeTime += runTime
        printMsg = f"It took {(avergeTime / iters):.6f} seconds on average to run {modelFilePath} on {engineType.upper()} engine."
        print(printMsg)
    
    if runPart == 4:
        engineType = getEngine()
        numBoxes = 2 ######################insert HERE number for the amount of boxes per iteration######################
        try:
            runIterative(inputFilePath, modelFileName, numBoxes, engineType)
        except RuntimeError as e:
            print(e)

