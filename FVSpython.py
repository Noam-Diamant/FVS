import os  # Import the os module for file operations
import numpy as np  # Import numpy module

# Function to input the file name and validate it
def inputFileName():
    while (True):
        # Prompt the user to input the path to the input file
        print("Please input the path to the input file, ends with extension \".xsb\": ")
        
        # Read the input from the user
        FileName = str(input())
        
        # Check if the file name ends with ".xsb"
        if not (FileName.endswith(".xsb")):
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

def readFile(FileName):
        with open(FileName, 'r') as f:
            contents = f.read()
            print(type(contents))


class SokobanBoard:
    def __init__(self, rows, columns):
        self.rows = rows
        self.width = columns
        self.board = [[None for _ in range(rows)] for _ in range(columns)]
    
    def printBoard(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                print(self.board[i][j], end=",  ")
            print()




if __name__ == '__main__':
    print("Hello, and welcome to the Sokoban folder!")
    FileNameForRead = inputFileName()
    b = SokobanBoard(3,5)
    b.printBoard()
    readFile(FileNameForRead)

