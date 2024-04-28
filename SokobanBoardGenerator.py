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

    def new_line(self, in_str):
        return f'{in_str}\n{self.tab_as_needed()}'

    def setTransitionRelations(self):
        TransitionRelationString = ""
        TransitionRelationString += self.movement_trans()
        for row_idx in range(self.rows):
            for col_idx in range(self.columns):
                TransitionRelationString += self.new_line(f"next(SokobanBoard[{row_idx}][{col_idx}]) :=")
                TransitionRelationString += self.open_case()
                TransitionRelationString += self.case_keeper(row_idx, col_idx)
                TransitionRelationString += self.case_box(row_idx, col_idx)
                TransitionRelationString += self.case_floor(row_idx, col_idx)
                TransitionRelationString += self.case_wall(row_idx, col_idx)
                TransitionRelationString += self.close_case()
        return TransitionRelationString

    def movement_trans(self):
        case_str = ''
        case_str += self.new_line(f"next(direction) :=")
        case_str += self.open_case()
        case_str += self.new_line(f"direction = u : d;") +\
                    self.new_line(f"direction = d : l;") +\
                    self.new_line(f"direction = l : r;") +\
                    self.new_line(f"direction = r : u;")
        case_str += self.close_case()
        return case_str

    def case_keeper(self, i, j):
        """If this tile is the guard, check if it can move towards the direction it needs.
         Either the next tile is a floor (or goal), or that it has where to push the box
         (the tile after the box is floor or goal) Otherwise - don't move"""

        cases_str = ''
        cases_str += self.new_line(self.check_state(i, j, self.keeper_states, ":"))
        cases_str += self.open_case()

        for direction in ['l', 'u', 'r', 'd']:
            if self.is_boarder(i, j, direction, 1):
                continue
            cases_str += self.new_line('')
            i_idx, j_idx = self.first_neighbor(i,j,direction)
            cases_str += f'(direction = {direction} & '
            cases_str += f'(({self.check_state(i_idx, j_idx, self.floor_states, "")})'
            if self.is_boarder(i, j, direction, 2):
                cases_str += ')) |'
                continue
            i_2_idx, j_2_idx = self.second_neighbor(i,j,direction)
            cases_str += f' | (({self.check_state(i_idx, j_idx, self.box_states, "")}) & ({self.check_state(i_2_idx, j_2_idx, self.floor_states, "")})))) |'

        cases_str = cases_str.removesuffix(' |')
        cases_str += self.new_line(' :')

        cases_str += self.open_case()
        cases_str += self.swap(i, j, self.keeper_states, self.floor_states)
        cases_str += self.close_case()

        cases_str += self.new_line(f"TRUE :")
        cases_str += self.open_case()
        cases_str += self.rho_i(i, j, symbol_dict['@'])
        cases_str += self.rho_i(i, j, symbol_dict['+'])
        cases_str += self.close_case()

        cases_str += self.close_case()
        return cases_str


    def case_box(self, i, j):
        """In case this tile is a box, it can move only if the previous tile
        (that corresponds to the direction) is the guard, and there is place to push the box"""
        cases_str = ''
        cases_str += self.new_line(self.check_state(i, j, self.box_states, ":"))
        cases_str += self.open_case()
        if i < 1 or i > (self.rows - 2) or j < 1 or j > (self.columns - 2):
            pass  # The only valid option is rho_i
        else:
            for direction in ['l', 'u', 'r', 'd']:
                opposite_direction = 'u' if direction == 'd' else 'd' if direction == 'u' else 'l' if direction == 'r' else 'r'
                if self.is_boarder(i, j, direction, 1) or self.is_boarder(i, j, opposite_direction, 1):
                    continue
                cases_str += self.new_line('')
                i_idx, j_idx = self.first_neighbor(i,j,direction)
                i_opp_idx, j_opp_idx = self.first_neighbor(i,j,opposite_direction)
                cases_str += f'(direction = {direction} & '
                cases_str += f'(({self.check_state(i_idx, j_idx, self.keeper_states, "")}) & ({self.check_state(i_opp_idx, j_opp_idx, self.keeper_states, "")}))) |'

            cases_str = cases_str.removesuffix(' |')
            cases_str += self.new_line(' : ')

            cases_str += self.open_case()
            cases_str += self.swap(i, j, self.box_states, self.keeper_states)
            cases_str += self.close_case()

        # rho_i
        cases_str += self.new_line("TRUE :")
        cases_str += self.open_case()
        cases_str += self.rho_i(i, j, symbol_dict['$'])
        cases_str += self.rho_i(i, j, symbol_dict['*'])
        cases_str += self.close_case()

        cases_str += self.close_case()

        return cases_str

    def case_floor(self, i, j):
        """In this case, the floor will change if the guard tries to go on it, or if the guard tries to push a box on to it"""
        cases_str = ''
        cases_str += self.new_line(self.check_state(i, j, self.floor_states, ":"))
        cases_str += self.open_case()
        for direction in ['l', 'u', 'r', 'd']:
            opposite_direction = 'u' if direction == 'd' else 'd' if direction == 'u' else 'l' if direction == 'r' else 'r'
            if self.is_boarder(i, j, opposite_direction, 1):
                continue
            i_idx, j_idx = self.first_neighbor(i,j,opposite_direction)
            cases_str += self.new_line('')
            cases_str += f'(direction = {direction} & {self.check_state(i_idx, j_idx, self.keeper_states, "")}) |'
        cases_str = cases_str.removesuffix(' |')
        cases_str += self.new_line(' :')

        cases_str += self.open_case()
        cases_str += self.swap(i, j, self.floor_states, self.keeper_states)
        cases_str += self.close_case()

        for direction in ['l', 'u', 'r', 'd']:
            opposite_direction = 'u' if direction == 'd' else 'd' if direction == 'u' else 'l' if direction == 'r' else 'r'
            if self.is_boarder(i, j, opposite_direction, 2):
                continue
            i_idx, j_idx = self.first_neighbor(i,j,opposite_direction)
            i_2_idx, j_2_idx = self.second_neighbor(i,j,opposite_direction)
            cases_str += self.new_line('')
            cases_str += f'(direction = {direction} & '\
                         f'({self.check_state(i_idx, j_idx, self.box_states, "")}) & ({self.check_state(i_2_idx, j_2_idx, self.keeper_states, "")})) |'
        cases_str = cases_str.removesuffix(' |')
        cases_str += self.new_line(' :')

        cases_str += self.open_case()
        cases_str += self.swap(i, j, self.floor_states, self.box_states)
        cases_str += self.close_case()

        # rho_i
        cases_str += self.new_line("TRUE :")
        cases_str += self.open_case()
        cases_str += self.rho_i(i, j, symbol_dict['-'])
        cases_str += self.rho_i(i, j, symbol_dict['.'])
        cases_str += self.close_case()

        cases_str += self.close_case()

        return cases_str


    def case_wall(self, i, j):
        """ Any tile that is a wall always stays the same. Therefore, it's : Rho_i
        This covers also tiles that are on the edge of the board"""
        # return self.rho_i(i, j, self.wall_states[0])
        return self.new_line(f"TRUE: {self.wall_states[0]};")


    def createSmvFileContent(self, inputFilePath, outputFilePath):
        inputFilePath = inputFilePath.replace("\\\\", "\\")
        fileContent = f"""-- This smv model was built by the automation code produced as part of the project 
-- in the formal verification and synthesis course by Noam Diamant and Ora Wetzler.

-- This smv model is built according to the input file found in the following path:
-- {inputFilePath}
-- The model is in the following path:
-- {outputFilePath}
MODULE main

VAR
    -- In this section we describe the variables of the model of the Sokoban board

    -- 2D array for the Sokoban borad
    SokobanBoard : array 0..{self.rows - 1} of array 0..{self.columns - 1} of {{percent, dollar, asterisk, hashtag, at, plus, dot, dash}};
    
    -- Movement options 
    direction : {{l, u, r, d}}; 

ASSIGN
    -- In this section we describe the initial state of the Sokoban board model

    {self.InitialBoard}

    -- In this section we describe the transition relations of the Sokoban board model

    {self.transitionRelations}

    -- In this section we describe the win conditions for the Sokoban board model

    {self.winConditions}
"""
        return fileContent

    ####################
    # Helper functions #
    ####################

    def swap(self, i, j, origin_states, dest_states):
        swap_str = ''
        for k in range(len(origin_states)):
            swap_str += self.new_line(f"SokobanBoard[{i}][{j}] = {origin_states[k]} : {dest_states[k]};")
        return swap_str

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

    def rho_i(self, i, j, tile_str):
        return self.new_line(f"SokobanBoard[{i}][{j}] = {tile_str} : {tile_str};")

    def second_neighbor(self, i, j, d):
        if d == 'u': i_idx = (i-2); j_idx = j
        if d == 'd': i_idx = (i+2); j_idx = j
        if d == 'r': i_idx = i; j_idx = j + 2
        if d == 'l': i_idx = i; j_idx = j - 2
        return i_idx, j_idx


    def first_neighbor(self, i, j, d):
        if d == 'u': i_idx = (i-1); j_idx = j
        if d == 'd': i_idx = (i+1); j_idx = j
        if d == 'r': i_idx = i; j_idx = j + 1
        if d == 'l': i_idx = i; j_idx = j - 1
        return i_idx, j_idx

    def is_boarder(self, i, j, direction, distance):
        if direction == 'u' and ((i - distance) < 0) or direction == 'd' and ((i + distance) > self.rows-1)\
                    or direction == 'l' and ((j - distance) < 0) or direction == 'r' and ((j + distance) > self.columns-1):
            return True
        return False

    def check_state(self, i, j, states, end_with):
        check_state_str = ''
        for state in states:
            check_state_str += f"SokobanBoard[{i}][{j}] = {state} |"

        cases_str = check_state_str.removesuffix(' |')
        cases_str += end_with
        return cases_str


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



