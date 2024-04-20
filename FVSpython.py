import os
import numpy as np

def inputFileName():
    while (True):
        print("Please input the path to the input file, ends with extension \".xsb\": ")
        FileName = str(input())
        if not (FileName.endswith("xsb")):
            print("Invalid input, try again")
        else:
            break
    return FileName

class SokobanBoard:
    def __init__(self, rows, columns):
        self.rows = rows
        self.width = columns
        self.board = np.zeros((rows, columns))



if __name__ == '__main__':
    print("Hello, and welcome to the Sokoban folder!")
    FileName = inputFileName()
    b = SokobanBoard(3,5)
    print(b.board)    