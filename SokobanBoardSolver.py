import os  # Import the os module for file operations
import time
from SokobanBoardGenerator import *
import subprocess

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
    print(f"Output saved to {outputFilename}")
    
    # Return output filename
    return outputFilename


def get_board_result(outputFilename):
    with open(outputFilename, 'r') as f:
        output = f.read()

    if 'true' in output:
        winning_movments = ''
        print(f"*******************************************")
        print(f"********    NOT SOLVABLE    ***************")
        print(f"*******************************************")

    elif 'false' in output:
        print(f"*******************************************")
        print(f"********    SOLVABLE    *******************")
        print(f"*******************************************")
        output_moves = output.split("-> State:")
        winning_movments = ''
        for i in range(1, len(output_moves)):
            if 'direction =' in output_moves[i]:
                winning_movments += (output_moves[i].split('direction =')[1]).split('\n')[0].strip().upper()+"-"
            else:
                winning_movments += f'{winning_movments[-2:-1]}-'
            if "-- Loop starts here" in output_moves[i - 1]:
                # This is the last move of the keeper
                break
        winning_movments = winning_movments.removesuffix("-")
        print(f"The wining stratergy for the keeper is:")
        print(f"*******************************************")
        print(f"*    {winning_movments}    *")
        print(f"*******************************************")

    else:
        winning_movments = ''
        print("error- no indication in output file")

    return winning_movments


def MeasureRunTime(modelFilename, engineType = None, steps = None):
    startTime = time.time()
    # Run nuXmv
    _ = run_nuxmv(modelFilename, engineType, steps)
    # Stop the timer
    endTime = time.time()
    runTime = endTime - startTime
    return runTime
