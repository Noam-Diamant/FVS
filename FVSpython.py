import os
import numpy as np

def inputFileName():
    while (True):
        print("Please input the path to the input file, ends with extension \".xsb\": ")
        FileName = str(input())
        if not (FileName.endswith(".xsb")):
            print("Invalid input, try again")
        else:
            break
    FileNameForRead = ""
    for char in FileName:
        if char == "\\":
            FileNameForRead += "\\"
        FileNameForRead += char
    return FileNameForRead

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
    #FileNameForRead = inputFileName()
    b = SokobanBoard(3,5)
    b.printBoard()
    #readFile(FileNameForRead)

