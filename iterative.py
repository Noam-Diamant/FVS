import os  # Import the os module for file operations
import time
from SokobanBoardSolver import *
import subprocess
from SokobanBoardGenerator import *
import random
import re


# needs to get the number off goals 
# needs to get the file 
# saves in the same dir in sub board 
# also print how many sub boards 


# run sub boards 

# print time for each iteration and total time

def print_board(InitialBoard):
    printable_board = ''
    for line in InitialBoard:
        for cell in line:
            printable_board += f'{name_dict[cell]}\t'
        printable_board += '\n'
    print(printable_board)


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
            if sokobanBoard.InitialBoard[rowIdx][columnIdx] in goal_states.values():
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


def update(smvSolution, board):
    with open(smvSolution, 'r') as f:
        output = f.read()

    if 'true' in output:
        # The board is not solvable, return false
        return False, board

    elif 'false' in output:
        iter_goal_coordinates = find_goal_tiles(output)
        boxes_on_goal_coordinates = []
        output_states = output.split("-> State:")
        movement_pattern = \
            rf"SokobanBoard\[(\d+)\]\[(\d+)\] = ({goal_states['floor']}|{goal_states['keeper']}|{goal_states['box']}|" \
            rf"{floor_states['floor']}|{floor_states['keeper']}|{floor_states['box']})"

        # First state is the initial state, there is no need to update that
        for i in range(1, len(output_states)):
            coordinates_and_next_state = re.findall(movement_pattern, output_states[i])

            # In first iteration, find boxes on goals, but no need to update the board
            for coord1, coord2, tile_state in coordinates_and_next_state:
                if i != 1:
                    board.InitialBoard[int(coord1)][int(coord2)] = tile_state

                # Check when to stop running
                if tile_state == goal_states['box']:
                    boxes_on_goal_coordinates.append((int(coord1), int(coord2)))
                elif tile_state in goal_states.values() and (int(coord1), int(coord2)) in boxes_on_goal_coordinates:
                    boxes_on_goal_coordinates.remove((int(coord1), int(coord2)))

            # If in this state, all boxes are on goals - this was the winning move
            if boxes_on_goal_coordinates == iter_goal_coordinates:
                break

    return True, board.InitialBoard


def createSmvBoardFileIteration(Ipath, Opath, iterationGoals, board = None,  iteration = 1, smvSolution = None):
    inputFilePath = Ipath
    board.winConditions = setIterWinConditions(iterationGoals)
    if iteration == 1:
        None
    else:
        # update the initial board at the next iteration to be final state at the previous iteration
        is_solvable, board.InitialBoard = update(smvSolution, board)
        if not is_solvable:
            raise RuntimeError(f"The board is not solvable in iteration {iteration}")
        board.setInitialBoardString()
    # Obtain output file path
    IterModelFilePath = Opath+f"_IterationModel_iter{iteration}.smv"#getOutputPath()
    
    # Generate SMV model content and write to output file
    model = board.createSmvFileContent(inputFilePath, IterModelFilePath)
    writeStringToFile(model, IterModelFilePath)
    print(f"model from iteration {iteration} saved to {IterModelFilePath}")
    
    # Return tuple containing input and output file paths with double backslashes replaced
    if iteration == 1:
        return iteration+1, board, inputFilePath.replace("\\\\", "\\"), IterModelFilePath
    else:
        return iteration+1, board, inputFilePath, IterModelFilePath


def sampleNCreateBoards(Ipath, Opath, boardGoals, nunBoxesInItter, board):
    iterationGoals = []
    iteration = 1
    totalRunTime = 0
    while len(boardGoals) >= nunBoxesInItter:
        print(f"*********** Starting iteration {iteration} ***********")
        randomGoals = random.sample(boardGoals, nunBoxesInItter)
        iterationGoals.extend(randomGoals)
        for goal in randomGoals:
            boardGoals.remove(goal)
        try:
            iteration, board, Ipath, IterModelFilePath = createSmvBoardFileIteration(Ipath, Opath, iterationGoals, board, iteration, smvSolution=None if iteration == 1 else PrevIterOutFilePath)
        except RuntimeError as e:
            raise e

        print("Initial board in current iteration:")
        print_board(board.InitialBoard)
        curRunTime, PrevIterOutFilePath = MeasureRunTime(IterModelFilePath, 'sat')
        totalRunTime += curRunTime
        if not get_board_result(PrevIterOutFilePath, to_print=False):
            raise RuntimeError(f"The board is not solvable in iteration {iteration - 1}")
        print(f"*** Iteration {iteration - 1} solved {nunBoxesInItter} boxes in: {curRunTime} seconds ***")

    # If there are fewer than n values remaining, take all of them
    if boardGoals:
        print(f"*********** Starting iteration {iteration} ***********")
        iterationGoals.extend(boardGoals)
        boardGoals.clear()
        try:
            iteration, board, Ipath, Modelpath = createSmvBoardFileIteration(Ipath,Opath, iterationGoals, board, iteration, smvSolution=None if iteration == 1 else PrevIterOutFilePath)
        except RuntimeError as e:
            raise e

        print("Initial board in current iteration:")
        print_board(board.InitialBoard)
        curRunTime, PrevIterOutFilePath = MeasureRunTime(IterModelFilePath, 'sat')
        totalRunTime += curRunTime
        if not get_board_result(PrevIterOutFilePath, to_print=False):
            raise RuntimeError(f"The board is not solvable in iteration {iteration - 1}")
        print(f"*** Iteration {iteration - 1} solved {nunBoxesInItter} boxes in: {curRunTime} seconds ***")

    print(f"\n*** Total running time: {totalRunTime} ***")
    return iterationGoals

def runIterative(Ipath, Opath, numBoxes):
    board = createBoard(Ipath)
    boardGoals = getGoalsLocs(board)
    try:
        sampleNCreateBoards(Ipath, Opath, boardGoals, numBoxes, board)
    except RuntimeError as e:
        raise e
