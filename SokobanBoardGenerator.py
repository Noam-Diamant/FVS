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
        # FileName = os.path.join(os.getcwd(), "aaa.txt")
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
    floor_states = {'floor': symbol_dict['-'], 'keeper':symbol_dict['@'], 'box': symbol_dict['$']}
    goal_states = {'floor': symbol_dict['.'], 'keeper':symbol_dict['+'], 'box': symbol_dict['*']}
    wall_state = symbol_dict['#']
    current_tab_level = 1

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
        TransitionRelationString = ""
        TransitionRelationString += self.new_line("next(direction) := {l, u, r, d};")
        for row_idx in range(self.rows):
            for col_idx in range(self.columns):
                if self.InitialBoard[row_idx][col_idx] == self.wall_state:
                    TransitionRelationString += self.new_line(f"next(SokobanBoard[{row_idx}][{col_idx}]) := {self.wall_state};")
                else:
                    TransitionRelationString += self.new_line(f"next(SokobanBoard[{row_idx}][{col_idx}]) :=")
                    TransitionRelationString += self.open_case()
                    TransitionRelationString += self.case_keeper(row_idx, col_idx)
                    TransitionRelationString += self.case_box(row_idx, col_idx)
                    TransitionRelationString += self.case_floor(row_idx, col_idx)
                    TransitionRelationString += self.rho_i(row_idx, col_idx)
                    TransitionRelationString += self.close_case()

        return TransitionRelationString

    def case_keeper(self, i, j):
        """If this tile is the guard, check if it can move to floor (or goal), or that it has where to push the box"""
        i_self, j_self, current_state = self.tile_check(i, j, 'u', 0, 'keeper')
        keeper_str = self.new_line('-- case keeper')
        for direction in ['l', 'u', 'r', 'd']:
            i_self, j_self, dest_state = self.tile_check(i, j, 'u', 0, 'floor')
            i_n1, j_n1, n1_state_to_check = self.tile_check(i, j, direction, 1, 'floor')
            if n1_state_to_check == self.wall_state:  # Wall is static, no point in checking
                continue
            keeper_str += self.new_line(f"SokobanBoard[{i_self}][{j_self}] = {current_state} & direction = {direction} & "
                                        f"SokobanBoard[{i_n1}][{j_n1}] = {n1_state_to_check} : "
                                        f"{dest_state};")

            i_n1, j_n1, n1_state_to_check = self.tile_check(i, j, direction, 1, 'box')
            i_n2, j_n2, n2_state_to_check = self.tile_check(i, j, direction, 2, 'floor')
            if n2_state_to_check == self.wall_state:  # Wall is static, no point in checking
                continue
            keeper_str += self.new_line(f"SokobanBoard[{i}][{j}] = {current_state} & direction = {direction} & "
                                        f"SokobanBoard[{i_n1}][{j_n1}] = {n1_state_to_check} & "
                                        f"SokobanBoard[{i_n2}][{j_n2}] = {n2_state_to_check} : "
                                        f"{dest_state};")
        return self.new_line(keeper_str)

    def case_box(self, i, j):
        """Tile is a box, it can move only if the previous tile is the guard, and there is place to push the box"""
        box_str = self.new_line('-- case box')
        i_self, j_self, current_state_to_check = self.tile_check(i, j, 'u', 0, 'box')
        i_self, j_self, dest_state = self.tile_check(i, j, 'u', 0, 'keeper')
        for direction in ['l', 'u', 'r', 'd']:
            opposite_direction = 'u' if direction == 'd' else 'd' if direction == 'u' else 'l' if direction == 'r' else 'r'
            i_n1, j_n1, n1_state_to_check = self.tile_check(i, j, direction, 1, 'floor')
            i_no, j_no, no_state_to_check = self.tile_check(i, j, opposite_direction, 1, 'keeper')
            if n1_state_to_check == self.wall_state or no_state_to_check == self.wall_state:  # Wall is static, no point in checking
                continue
            box_str += self.new_line(f"SokobanBoard[{i}][{j}] = {current_state_to_check} & direction = {direction} & "
                                     f"SokobanBoard[{i_n1}][{j_n1}] = {n1_state_to_check} & "
                                     f"SokobanBoard[{i_no}][{j_no}] = {no_state_to_check}: "
                                     f"{dest_state};")
        return self.new_line(box_str)

    def case_floor(self, i, j):
        """In this case, the floor will change if the guard tries to go on it, or if the guard tries to push a box on to it"""
        floor_str = self.new_line('-- case floor')
        i_self, j_self, current_state = self.tile_check(i, j, 'u', 0, 'floor')
        for direction in ['l', 'u', 'r', 'd']:
            opposite_direction = 'u' if direction == 'd' else 'd' if direction == 'u' else 'l' if direction == 'r' else 'r'
            i_self, j_self, dest_state = self.tile_check(i, j, 'u', 0, 'keeper')
            i_no1, j_no1, no1_state_to_check = self.tile_check(i, j, opposite_direction, 1, 'keeper')
            if no1_state_to_check == self.wall_state:  # Wall is static, no point in checking
                continue
            floor_str += self.new_line(f"SokobanBoard[{i}][{j}] = {current_state} & direction = {direction} & "
                                       f"SokobanBoard[{i_no1}][{j_no1}] = {no1_state_to_check} : "
                                       f"{dest_state};")

            i_self, j_self, dest_state = self.tile_check(i, j, 'u', 0, 'box')
            i_no1, j_no1, no1_state_to_check = self.tile_check(i, j, opposite_direction, 1, 'box')
            i_no2, j_no2, no2_state_to_check = self.tile_check(i, j, opposite_direction, 2, 'keeper')
            if no2_state_to_check == self.wall_state:  # Wall is static, no point in checking
                continue
            floor_str += self.new_line(f"SokobanBoard[{i}][{j}] = {current_state} & direction = {direction} & "
                                       f"SokobanBoard[{i_no1}][{j_no1}] = {no1_state_to_check} & "
                                       f"SokobanBoard[{i_no2}][{j_no2}] = {no2_state_to_check} : "
                                       f"{dest_state};")
        return self.new_line(floor_str)

    def createSmvFileContent(self, inputFile, outputFilePath):
        inputFile = inputFile.replace("\\\\", "\\")
        fileContent = f"""-- This smv model was built by the automation code produced as part of the project 
-- in the formal verification and synthesis course by Noam Diamant and Ora Wetzler.

-- This smv model is built according to the input file found in the following path:
-- {inputFile}
-- The model is in the following path:
-- {outputFilePath}
MODULE main

VAR
    -- In this section we describe the variables of the model of the Sokoban board

    -- 2D array for the Sokoban borad
    SokobanBoard : array 0..{self.rows - 1} of array 0..{self.columns - 1} of {{percent, dollar, asterisk, hashtag, at, plus, dot, dash}};
    
    -- Movement options 
    direction : {{l, u, r, d}}; 

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

    ####################
    # Helper functions #
    ####################
    def open_case(self):
        self.current_tab_level += 1
        tab_str1 = self.new_line('')
        self.current_tab_level += 1
        return tab_str1 + self.new_line('case')

    def close_case(self):
        self.current_tab_level -= 1
        tab_str1 = self.new_line('')
        self.current_tab_level -= 1
        return tab_str1 + self.new_line('esac;')

    def tab_as_needed(self):
        return_str = ''
        for i in range(self.current_tab_level):
            return_str += '\t'
        return return_str

    def new_line(self, in_str):
        return f'{in_str}\n{self.tab_as_needed()}'

    def rho_i(self, i, j):
        if self.InitialBoard[i][j] in self.floor_states.values():
            states = self.floor_states
        elif self.InitialBoard[i][j] in self.goal_states.values():
            states = self.goal_states
        else:
            print(f"error, state in i = {i}, j = {j} is: {self.InitialBoard[i][j]}")
            exit(-1)

        rho_i_str = self.new_line("-- rho_i")
        rho_i_str += self.new_line("TRUE:")
        rho_i_str += self.open_case()
        for state in states.values():
            rho_i_str += self.new_line(f"SokobanBoard[{i}][{j}] = {state} : {state};")
        rho_i_str += self.new_line("-- to avoid nuXmv error. SHOULD NOT HAPPEN!!")
        rho_i_str += self.new_line(f"TRUE : {self.wall_state};")
        rho_i_str += self.close_case()
        return rho_i_str

    def tile_check(self, i, j, d, dis_from_current, key):
        if d == 'u': i_idx = (i-dis_from_current); j_idx = j
        if d == 'd': i_idx = (i+dis_from_current); j_idx = j
        if d == 'r': i_idx = i; j_idx = j + dis_from_current
        if d == 'l': i_idx = i; j_idx = j - dis_from_current
        if self.InitialBoard[i_idx][j_idx] in self.floor_states.values():
            value_to_check = self.floor_states[key]
        elif self.InitialBoard[i_idx][j_idx] in self.goal_states.values():
            value_to_check = self.goal_states[key]
        elif self.InitialBoard[i_idx][j_idx] == self.wall_state:
            value_to_check = self.wall_state
        else:
            print(f"tile_check: invalid input given!")
            exit(-1)
        return i_idx, j_idx, value_to_check


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
    # outputFilePath = os.path.join(os.getcwd(), "bbb.smv")
    
    # Return the constructed output file path
    return outputFilePath


def writeStringToFile(string, outputFilePath):      
    with open(outputFilePath, 'w') as file:
        file.write(string)

def createSmvBoardFile(inputFilePath=None,outputModelPath=None):
    # Obtain input file path
    if inputFilePath == None:
        inputFile = getInputFileName()
    else:
        inputFile = inputFilePath
    
    # Read rows, columns, and content from input file
    rows, columns, content = readFile(inputFile)
    
    # Initialize SokobanBoard object with obtained data
    b = SokobanBoard(rows, columns, content)
    
    # Obtain output file path
    if outputModelPath == None:
        outputPath = getOutputPath()
    else:
        outputPath = outputModelPath
    
    # Generate SMV model content and write to output file
    model = b.createSmvFileContent(inputFile, outputPath)
    writeStringToFile(model, outputPath)
    print(f"smv model that have been created from {inputFile} saved at {outputPath}")
    
    # Return tuple containing input and output file paths with double backslashes replaced
    return inputFile.replace("\\\\", "\\"), outputPath

# if __name__ == '__main__':
#     createSmvBoardFile()



