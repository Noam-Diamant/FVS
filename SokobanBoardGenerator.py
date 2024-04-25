import os  # Import the os module for file operations
import time
from SokobanBoardSolver import *
import subprocess


symbol_dict = {
    # Dictionary mapping symbols to their names
    '%': 'percent',
    '$': 'dollar',
    '*': 'asterisk',
    '#': 'hashtag',
    '@': 'at',
    '+': 'plus',
    '.': 'dot',
    '-': 'dash'
    # Add more mappings as needed
}


def getInputFileName():
    # Function to input the file name and validate it
    while (True):
        # Prompt the user to input the path to the input file
        print("Please input the path to the input file, ends with extension \".txt\": ")
        
        # Read the input from the user
        FileName = str(input())
        
        # Check if the file name ends with ".xsb"
        if not (FileName.endswith(".txt")):
            print("Invalid input, try again!")  # Print error message for invalid input
        else:
            FileNameForRead = ""
            # Process the file name to handle escape characters
            for char in FileName:
                if char == "\\":
                    FileNameForRead += "\\"  # Escape the backslash character
                FileNameForRead += char
            # Check if the file exists
            if (os.path.exists(FileNameForRead)):
                return FileNameForRead  # Return the validated file name
            else:
                print("File does not exist, try again!")  # Print error message for non-existent file


def removeTrailingCommas(input_string):
    # Split the string into lines
    lines = input_string.split('\n')
    
    # Remove trailing commas from each line
    lines = [line.rstrip(',') for line in lines]
    
    # Join the lines back together
    result = '\n'.join(lines)
    
    return result

def readFile(FileName):
    with open(FileName, 'r') as f:
        contents = f.read()
    
    # Split the contents into lines
    lines = contents.split('\n')
    
    # Count the number of rows (number of lines)
    rows = len(lines)
    
    # Count the number of columns (length of the first line)
    columns = len(lines[0])

    # Iterate over the content character by character    
    # Initialize convertedContent to an empty string
    convertedContent = ""
    
    # Iterate over each character in the contents
    for char in contents:
        # Check if the character is a symbol
        if char in symbol_dict:
            # Replace the symbol with its corresponding name
            convertedContent += symbol_dict[char]
            # Add a comma after the symbol
            convertedContent +=","
        else:
            # If not a symbol, keep the character as it is
            convertedContent += char
            
    # Remove trailing commas from convertedContent
    convertedContent = removeTrailingCommas(convertedContent)
    
    # return the converted content, its number of rows and columns
    return rows, columns, convertedContent

class SokobanBoard:
    def __init__(self, rows, columns, content):
        self.rows = rows
        self.columns = columns
        self.InitialBoard = self.setInitialBoard(content)
        self.InitialBoardString = self.setInitialBoardString()
        self.winConditions = self.setWinConditions()
        self.transitionRelations = self.setTransitionRelations()
    
    def setInitialBoard(self, content):
        # Split the input string into lines
        lines = content.strip().split('\n')
    
        # Initialize an empty 2D array
        InitialBoard = []
    
        # Iterate over the lines and split each line into elements
        for line in lines:
            elements = line.split(',')
            # Append the list of elements to the 2D array
            InitialBoard.append(elements)
        return InitialBoard
    
    def setInitialBoardString(self):
        InitialBoardString = ""
        for rowIdx in range(self.rows):
            for columnIdx in range(self.columns):
                InitialBoardString += f"SokobanBoard[{rowIdx}][{columnIdx}] = {str(self.InitialBoard[rowIdx][columnIdx]):<10}&\t\t"
            InitialBoardString += "\n\t"     
        # Find the last occurrence of "&"
        lastAmpersandIndex = InitialBoardString.rfind("&")

        # Replace the last "&" with ";"
        InitialBoardString = InitialBoardString[:lastAmpersandIndex] + ";" + InitialBoardString[lastAmpersandIndex + 1:]   
        return InitialBoardString
    
    def printBoard(self):
        print(f"({len(self.InitialBoard)},{len(self.InitialBoard[0])})")
        for i in range(self.rows):
            for j in range(self.columns):
                print(self.InitialBoard[i][j], end=",  ")
            print()

    def setWinConditions(self):
        winConditionsString = f"LTLSPEC !(F("
        for rowIdx in range(self.rows):
            for columnIdx in range(self.columns):
                # For each goal position put an asterisk at the end of the run
                if (self.InitialBoard[rowIdx][columnIdx] == 'dot' or
                    self.InitialBoard[rowIdx][columnIdx] == 'asterisk' or
                    self.InitialBoard[rowIdx][columnIdx] == 'plus'):
                    winConditionsString += f"(SokobanBoard[{rowIdx}][{columnIdx}] = asterisk) & "
        # Check if the string ends with " & " before removing it
        if winConditionsString.endswith(" & "):
            # Remove the last " & " by slicing the string
            winConditionsString = winConditionsString[:-3]  # Remove the last 3 characters
        winConditionsString += "));"
        return winConditionsString

    def setTransitionRelations(self):
        return ''

    def createSmvFileContent(self, inputFilePath, outputFilePath):    
        inputFilePath = inputFilePath.replace("\\\\", "\\")
        fileContent = f"""-- This smv model was built by the automation code produced as part of the project 
-- in the formal verification and synthesis course by Noam Diamant and Ora Wetzler.

-- This smv model is built according to the input file found in the following path:
-- {inputFilePath}
-- The model is in the following path:
-- {outputFilePath}
MODULE main

DEFINE rows := {self.rows}; columns := {self.columns};

VAR
    -- In this section we describe the variables of the model of the Sokoban board

    -- 2D array for the Sokoban borad
    SokobanBoard : array 0..(rows - 1) of array 0..(columns - 1) of {{percent, dollar, asterisk, hashtag, at, plus, dot, dash}};
    
    -- Movement options 
    Movement : {{l, u, r, d}}; 

INIT
    -- In this section we describe the initial state of the Sokoban board model

    {self.InitialBoardString}

ASSIGN
    -- In this section we describe the transition relations of the Sokoban board model

    {self.transitionRelations}

    -- In this section we describe the win conditions for the Sokoban board model

    {self.winConditions}
"""
        return fileContent


def getOutputPath():
    # Prompt user for the output folder path
    print("Please input the path to the output folder: ")
    OutputPath = str(input())
    
    # Prompt user for the name of the output file
    print("Please input the name to the output file: ")
    OutputFile = str(input())
    
    # Append ".smv" extension to the output file name
    OutputFile += ".smv"
    
    # Join output folder path and output file name to construct the output file path
    outputFilePath = os.path.join(OutputPath, OutputFile)
    
    # Return the constructed output file path
    return outputFilePath


def writeStringToFile(string, outputFilePath):      
    with open(outputFilePath, 'w') as file:
        file.write(string)

def createSmvBoardFile():
    # Obtain input file path
    inputFilePath = getInputFileName()
    
    # Read rows, columns, and content from input file
    rows, columns, content = readFile(inputFilePath)
    
    # Initialize SokobanBoard object with obtained data
    b = SokobanBoard(rows, columns, content)
    
    # Obtain output file path
    outputFilePath = getOutputPath()
    
    # Generate SMV model content and write to output file
    model = b.createSmvFileContent(inputFilePath, outputFilePath)
    writeStringToFile(model, outputFilePath)
    
    # Return tuple containing input and output file paths with double backslashes replaced
    return inputFilePath.replace("\\\\", "\\"), outputFilePath




import subprocess
import os  # Import the os module for file operations
import time



