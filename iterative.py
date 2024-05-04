import os  # Import the os module for file operations
import time
from SokobanBoardSolver import *
import subprocess
from SokobanBoardGenerator import *
import random


# needs to get the number off goals 
# needs to get the file 
# saves in the same dir in sub board 
# also print how many sub boards 


# run sub boards 

# print time for each iteration and total time 

def setIterWinConditions(iterationGoals):
    winConditionsString = f"LTLSPEC !(F("
    for goal in iterationGoals:
        winConditionsString += f"(SokobanBoard[{goal[0]}][{goal[1]}] = asterisk) & "
    # Check if the string ends with " & " before removing it
    if winConditionsString.endswith(" & "):
        # Remove the last " & " by slicing the string
        winConditionsString = winConditionsString[:-3]  # Remove the last 3 characters
    winConditionsString += "));"
    return winConditionsString

def getGoalsLocs(sokobanBoard):
    boardGoals = []
    for rowIdx in range(sokobanBoard.rows):
        for columnIdx in range(sokobanBoard.columns):
            if (sokobanBoard.InitialBoard[rowIdx][columnIdx] == 'dot' or
                sokobanBoard.InitialBoard[rowIdx][columnIdx] == 'asterisk' or
                sokobanBoard.InitialBoard[rowIdx][columnIdx] == 'plus'):
                boardGoals.append([rowIdx, columnIdx])
    return boardGoals

def createBoard(Ipath, iteration = 1):
    if iteration == 1:
        # Obtain input file path
        inputFilePath = Ipath #getInputFileName()
    
        # Read rows, columns, and content from input file
        rows, columns, content = readFile(inputFilePath)
    
        # Initialize SokobanBoard object with obtained data
        board = SokobanBoard(rows, columns, content)

    return board

def createSmvBoardFileIteration(Ipath, Opath, iterationGoals, board = None,  iteration = 1, smvSolution = None):
    inputFilePath = Ipath
    board.winConditions = setIterWinConditions(iterationGoals)
    if iteration == 1:
        None
    else:
        #update the intial board at the next iteration to to final state at the previous iteration
        #board.InitialBoard = update(smvSolution, board) 
        board.setInitialBoardString()
    # Obtain output file path
    outputFilePath = Opath+f"_IterationModel_iter{iteration}.smv"#getOutputPath()
    
    # Generate SMV model content and write to output file
    model = board.createSmvFileContent(inputFilePath, outputFilePath)
    writeStringToFile(model, outputFilePath)
    print(f"model from iteration {iteration} saved to {outputFilePath}")
    
    # Return tuple containing input and output file paths with double backslashes replaced
    if iteration == 1:
        return iteration+1, board, inputFilePath.replace("\\\\", "\\"), outputFilePath
    else:
        return iteration+1, board, inputFilePath, outputFilePath

def sampleNCreateBoards(Ipath, Opath, boardGoals, n, board):
    iterationGoals = []
    iteration = 1
    while len(boardGoals) >= n:
        randomGoals = random.sample(boardGoals, n)
        iterationGoals.extend(randomGoals)
        for goal in randomGoals:
            boardGoals.remove(goal)
        if iteration == 1:
            iteration, board, Ipath, _ = createSmvBoardFileIteration(Ipath, Opath, iterationGoals, board, iteration=1, smvSolution = None)
            #yield Opath
        else:
            iteration, board, Ipath, _ = createSmvBoardFileIteration(Ipath,Opath, iterationGoals, board, iteration, smvSolution = "./bbb_IterationModel_iter"+f"{iteration-1}"+".out")
            #yield Opat

    # If there are fewer than n values remaining, take all of them
    if boardGoals:
        iterationGoals.extend(boardGoals)
        boardGoals.clear()
        iteration, board, Ipath, Opath = createSmvBoardFileIteration(Ipath,Opath, iterationGoals, board, iteration, smvSolution = "./bbb_IterationModel_iter"+f"{iteration-1}"+".out")
        #yield Opath

    return iterationGoals


if __name__ == '__main__':
    Ipath = "./aaa.txt"
    Opath = "./bbb"
    board = createBoard(Ipath)
    print(board.InitialBoard)
    boardGoals = getGoalsLocs(board)
    print(boardGoals)
    sampleNCreateBoards(Ipath, Opath, boardGoals, 1, board)
    print(MeasureRunTime("./bbb_IterationModel_iter1.smv", 'BDD', 50))
    print(MeasureRunTime("./bbb_IterationModel_iter2.smv", 'BDD', 50))
    




    
