import os  # Import the os module for file operations
import time
from SokobanBoardGenerator import *
import subprocess
import re

def run_nuxmv(modelFilename, engineType = None, steps = None):
    # Configure NuSMV process based on engineType
    if engineType == "BDD":
        nuxmvProcess = subprocess.Popen([".\\nuXmv.exe", "-int", modelFilename], stdin=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
        nuxmvProcess.stdin.write("go\n")
        nuxmvProcess.stdin.write("check_ltlspec\n")
        nuxmvProcess.stdin.write("quit\n")
    elif engineType == "SAT":
        nuxmvProcess = subprocess.Popen([".\\nuXmv.exe", "-int", modelFilename], stdin=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
        nuxmvProcess.stdin.write("go_bmc\n")
        if steps == None:
            nuxmvProcess.stdin.write(f"check_ltlspec_bmc\n")
        else:
            nuxmvProcess.stdin.write(f"check_ltlspec_bmc -k {steps}\n")
        nuxmvProcess.stdin.write("quit\n")
    else:
        nuxmvProcess = subprocess.Popen([".\\nuXmv.exe", modelFilename], stdin=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
    
    # Define output filename
    outputFilename = modelFilename.split(".")[0] + ".out"
    
    # Run NuSMV process and capture stdout
    stdout, _ = nuxmvProcess.communicate()
    
    # Write stdout to output file
    with open(outputFilename, "w") as f:
        f.write(stdout)
    
    # Print output filename
    print(f"The output of running Nuxmv on {modelFilename} saved to {outputFilename}")
    
    # Return output filename
    return outputFilename

def find_goal_tiles(output):
    pattern = r"-- specification !\( F(.*?)is false"
    matches = re.findall(pattern, output, re.DOTALL)
    goal_tiles_coordinates = []

    for match in matches:
        pattern = r"SokobanBoard\[(\d+)\]\[(\d+)\]"
        coordinate_matches = re.findall(pattern, match)
        goal_tiles_coordinates.extend([(int(coord1), int(coord2)) for coord1, coord2 in coordinate_matches])

    return goal_tiles_coordinates


def get_board_result(outputFilename):
    with open(outputFilename, 'r') as f:
        output = f.read()

    if 'true' in output:
        LURD_output = ''
        print(f"*******************************************")
        print(f"********    NOT SOLVABLE    ***************")
        print(f"*******************************************")

    elif 'false' in output:
        print(f"*******************************************")
        print(f"********    SOLVABLE    *******************")
        print(f"*******************************************")

        goal_tile_coordinates = find_goal_tiles(output)
        boxes_on_goal_tiles_coor = []
        output_moves = output.split("-> State:")
        movement_pattern = \
            rf"SokobanBoard\[(\d+)\]\[(\d+)\] = ({goal_states['floor']}|{goal_states['keeper']}|{goal_states['box']}|" \
            rf"{floor_states['floor']}|{floor_states['keeper']}|{floor_states['box']})"
        LURD_output = ''

        for i in range(1, len(output_moves)):
            coordinates_and_next_state = re.findall(movement_pattern, output_moves[i])
            for coord1, coord2, tile_state in coordinates_and_next_state:
                if tile_state == goal_states['box']:
                    boxes_on_goal_tiles_coor.append((int(coord1), int(coord2)))
                elif tile_state in goal_states.values() and (int(coord1), int(coord2)) in boxes_on_goal_tiles_coor:
                    boxes_on_goal_tiles_coor.remove((int(coord1), int(coord2)))
                else:
                    continue

            # If in this state, all boxes are on goals - this was the winning move
            if set(boxes_on_goal_tiles_coor) == set(goal_tile_coordinates):
                break

            # The previous move was a rho_i, since there was nowhere to go- remove the last movement
            if not coordinates_and_next_state:
                LURD_output = LURD_output[:-2]

            # Concatenate the last movement to the LURD string
            if 'direction =' in output_moves[i]:
                LURD_output += (output_moves[i].split('direction =')[1]).split('\n')[0].strip().upper()+"-"
            elif 'direction =' not in output_moves[i]:
                LURD_output += f'{LURD_output[-2:-1]}-'

        LURD_output = LURD_output.removesuffix("-")
        print(f"The wining strategy for the keeper is:")
        print(f"*******************************************")
        print(f"*    {LURD_output}    *")
        print(f"*******************************************")

    else:
        LURD_output = ''
        print("error- no indication in output file")

    return LURD_output


def MeasureRunTime(modelFilename, engineType = None, steps = None):
    startTime = time.time()
    # Run nuXmv
    _ = run_nuxmv(modelFilename, engineType, steps)
    # Stop the timer
    endTime = time.time()
    runTime = endTime - startTime
    return runTime
