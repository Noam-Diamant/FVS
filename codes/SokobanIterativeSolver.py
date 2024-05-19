import os  # Import the os module for file operations
import time
from SokobanBoardSolver import *
import subprocess
from SokobanBoardGenerator import *
import random
import re

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


def createSmvBoardFileIteration(Ipath, Opath, iterationGoals, numBoxes, board = None,  iteration = 1, smvSolution = None):
    inputFilePath = Ipath
    board.winConditions = setIterWinConditions(iterationGoals)
    if iteration == 1:
        None
    else:
        # update the initial board at the next iteration to be final state at the previous iteration
        is_solvable, board.InitialBoard = update(smvSolution, board)
        if not is_solvable:
            raise RuntimeError(f"The board is not solvable in iteration {iteration}")
        board.InitialBoardString = board.setInitialBoardString()
    # Obtain output file path
    IterModelFilePath = Opath+f"_{numBoxes}_boxes_IterationModel_iter{iteration}.smv"#getOutputPath()
    
    # Generate SMV model content and write to output file
    model = board.createSmvFileContent(inputFilePath, IterModelFilePath)
    writeStringToFile(model, IterModelFilePath)
    print(f"model from iteration {iteration} saved to {IterModelFilePath}")
    iteration +=1
    
    # Return tuple containing input and output file paths with double backslashes replaced
    if iteration == 1:
        return iteration, board, inputFilePath.replace("\\\\", "\\"), IterModelFilePath
    else:
        return iteration, board, inputFilePath, IterModelFilePath


def sampleNCreateBoards(Ipath, Opath, boardGoals, numBoxesInItter, board, engineType):
    iterationGoals = []
    iteration = 1
    totalRunTime = 0
    while len(boardGoals) >= numBoxesInItter:
        print(f"*********** Starting iteration {iteration} ***********")
        randomGoals = random.sample(boardGoals, numBoxesInItter)
        iterationGoals.extend(randomGoals)
        for goal in randomGoals:
            boardGoals.remove(goal)
        try:
            iteration, board, Ipath, IterModelFilePath = createSmvBoardFileIteration(Ipath, Opath, iterationGoals, numBoxesInItter, board, iteration, smvSolution=None if iteration == 1 else PrevIterOutFilePath)
        except RuntimeError as e:
            raise e

        #print("Initial board in current iteration:")
        #print_board(board.InitialBoard)
        curRunTime, PrevIterOutFilePath = MeasureRunTime(IterModelFilePath, engineType)
        totalRunTime += curRunTime
        is_solvable, _ = get_board_result(PrevIterOutFilePath, to_print=False)
        if not is_solvable:
            raise RuntimeError(f"The board is not solvable in iteration {iteration - 1}")
        locationsMsg = ""
        for goal in iterationGoals:
            locationsMsg += f"{goal}, "
        locationsMsg = locationsMsg[:-2]
        print(f"*** Iteration {iteration - 1} solved {len(iterationGoals)} boxes in location(s) {locationsMsg} : {curRunTime} seconds ***")

    # If there are fewer than n values remaining, take all of them
    if boardGoals:
        print(f"*********** Starting iteration {iteration} ***********")
        iterationGoals.extend(boardGoals)
        boardGoals.clear()
        try:
            iteration, board, Ipath, IterModelFilePath = createSmvBoardFileIteration(Ipath,Opath, iterationGoals, numBoxesInItter, board, iteration, smvSolution=None if iteration == 1 else PrevIterOutFilePath)
        except RuntimeError as e:
            raise e

        #print("Initial board in current iteration:")
        #print_board(board.InitialBoard)
        curRunTime, PrevIterOutFilePath = MeasureRunTime(IterModelFilePath, engineType)
        totalRunTime += curRunTime
        is_solvable, _ = get_board_result(PrevIterOutFilePath, to_print=False)
        if not is_solvable:
            raise RuntimeError(f"The board is not solvable in iteration {iteration - 1}")
        locationsMsg = ""
        for goal in iterationGoals:
            locationsMsg += f"{goal}, "
        locationsMsg = locationsMsg[:-2]
        print(f"*** Iteration {iteration - 1} solved {len(iterationGoals)} boxes in location(s) {locationsMsg} : {curRunTime} seconds ***")

    print(f"\n*** Total running time: {totalRunTime} ***")
    return iterationGoals
