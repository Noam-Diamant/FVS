import os  # Import the os module for file operations

# Dictionary mapping symbols to their names
symbol_dict = {
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


def remove_trailing_commas(input_string):
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
    # Initialize converted_content to an empty string
    converted_content = ""
    
    # Iterate over each character in the contents
    for char in contents:
        # Check if the character is a symbol
        if char in symbol_dict:
            # Replace the symbol with its corresponding name
            converted_content += symbol_dict[char]
            # Add a comma after the symbol
            converted_content +=","
        else:
            # If not a symbol, keep the character as it is
            converted_content += char
            
    # Remove trailing commas from converted_content
    converted_content = remove_trailing_commas(converted_content)
    
    # return the converted content, its number of rows and columns
    return rows, columns, converted_content


class SokobanBoard:
    def __init__(self, rows, columns, content):
        self.rows = rows
        self.columns = columns
        self.board = self.setBoard(content)
    
    def setBoard(self, content):
        # Split the input string into lines
        lines = content.strip().split('\n')
    
        # Initialize an empty 2D array
        Board = []
    
        # Iterate over the lines and split each line into elements
        for line in lines:
            elements = line.split(',')
            # Append the list of elements to the 2D array
            Board.append(elements)
    
        return Board
    
    def printBoard(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                print(self.board[i][j], end=",  ")
            print()




if __name__ == '__main__':
   # print("Hello, and welcome to the Sokoban folder!")
    FileNameForRead = inputFileName()
    #b = SokobanBoard(3,5)
   # b.printBoard()
    rows, columns, content = readFile(FileNameForRead)
    b = SokobanBoard(rows, columns, content)
    b.printBoard()



