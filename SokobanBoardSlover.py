import subprocess
import os  # Import the os module for file operations
import time

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

def MeasureRunTime():
    startTime = time.time()
    # Run nuXmv
    output_file_name = run_nuxmv(modelFilename, engine=engine, k=k)
    # Stop the timer
    endTime = time.time()
    runTime = endTime - startTime
    return runTime