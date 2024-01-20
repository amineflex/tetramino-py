###############################################
#                  Tetramino                  #
#            INFO-F106 : Project 1            #
#   Usage : python3 tetramino.py <card.txt>   #
###############################################

__title__ = "Tetramino"
__description__ = "Tetramino game inspired by \"Gagne ton papa\""
__course__ = "INFO-F106 — Project 1"
__authors__ = "Amine"
__contact__ = "@amineflex"
__date__ = "2023-11-22"

# Import modules
from getkey import getkey
import os, sys

# Consts
SPACE = " "
VERTICAL_SEP = "|"
HORIZONTAL_SEP = "--"
SEP_LINE = "–––––––––––––––––––––––––––––––––––––"
TETRAMINO_ASCII = """
 .---. .----..---. .----.   .--.  .-.   .-..-..-. .-. .----. 
{_   _}| {_ {_   _}| {}  } / {} \\ |  `.'  || ||  `| |/  {}  \\ 
  | |  | {__  | |  | .-. \\/  /\\  \\| |\\ /| || || |\\  |\\      /
  `-'  `----' `-'  `-' `-'`-'  `-'`-' ` `-'`-'`-' `-' `----'
"""
GREEN = "\033[92m"
RED = "\033[91m"
GRAY = "\033[90m"
BLUE = "\033[94m"
LIGHT_BLUE = "\033[96m"
LIGHT_GRAY = "\033[37m"
RESET_COLOR = "\x1b[0m"

# Functions
def title_screen():
    """
    Print a stylished welcome message
    :return: None
    """
    clear()
    print(BLUE + TETRAMINO_ASCII)
    print(SEP_LINE*2)
    print(LIGHT_BLUE + " Welcome to the Tetramino Game !")
    # Infos
    print(GRAY + "  " + __description__)
    print("  > Author :", __authors__,f"({__contact__})")
    print("  >",__course__ , RESET_COLOR)
    # Rules
    print(GREEN + "\nRules :")
    print(LIGHT_GRAY + " > To win the game, place all the tetraminos on the grid")
    print(" > To select a tetramino, use the numbers '1' to '8'")
    print(" > To move a tetramino, use the keys 'i', 'j', 'k', 'l'")
    print(" > To rotate a tetramino, use the keys 'u' and 'o'")
    print(" > To validate the move, press 'v'\n")
    # Start message
    print(GREEN + "To start the game, press any key")
    print(RED + "To quit the game, press 'q'")
    print(BLUE + SEP_LINE*2 + RESET_COLOR)
    # Wait for a key 
    key = getkey()
    if key != "q":
        clear()
    else:
        exit()
    

def clear():
    """
    Clear the terminal screen depending on the OS
    :return: None
    """
    if (os.name == 'posix'):
        os.system('clear')  # Clear console on Unix/Linux/MacOS
    else:
        os.system('cls')  # Clear console on Windows


def error(error_name, error_desc):
    """
    Print a stylished error message and terminate the game
    :return: None
    """
    print(SEP_LINE)
    print(RED + "Tetramino — Error")
    print(GRAY + error_name)
    print(error_desc + RESET_COLOR)
    print(SEP_LINE)
    exit()


def generate_gap(number, width, height):
    """
    Generate a gap for a tetramino
    :param number: number of the tetramino
    :param width: width of the grid
    :param height: height of the grid
    :return: tuple with the gap
    """
    list_gaps = [(0, 0), (width//3 +1, 0), (width//3*2 +2, 0), # 1 2 3
                 (0, height//3+1), (width//3*2 +2, height//3+1), # 4 5
                 (0, height//3*2 +2), (width//3 +2, height//3*2+2), (width//3*2 +2, height//3*2+2) # 6 7 8
                ]
    return list_gaps[number-1]


def create_grid(w: int, h: int):
    """
    Create a grid on a matrix
    :param w: width of the grid
    :param h: height of the grid
    :return: list of the grid
    """
    # Initialize vars
    width = 3 * w + 2
    height = 3 * h + 2

    # Generate the list (matrix)
    grid = [[SPACE*2] * width for _ in range(height)]

    # Vertical lines
    for i in range(h+1, 2*h+1):
        grid[i][w] = SPACE+VERTICAL_SEP  # left
        grid[i][w+w+1] = VERTICAL_SEP+SPACE  # right

    # Horizontal lines
    for i in range(w+1, 2*w+1):
        grid[h][i] = HORIZONTAL_SEP  # top
        grid[h+h+1][i] = HORIZONTAL_SEP  # bottom

    return grid


def import_card(file_path: str):
    """
    Import the card from a .txt file
    :param file_path: path of the .txt file
    :return: tuple with dimension of plate and tetraminos list
    """
    # Check if file_path exists
    try:
        # Open the file and append each line in a list
        with open(file_path, "r") as card:
            card_lines = [line.strip() for line in card.readlines()]
    except FileNotFoundError:
        error_name = f"The file '{file_path}' doesn't exist"
        error_desc = "File not found"
        error(error_name, error_desc)

    # Size of grid
    size = eval(card_lines[0])  # transform to a tuple
    card_lines.remove(card_lines[0])  # remove the size in the list

    # list of tetraminos components
    tetramino_list = []
    i = 0
    for elem in card_lines:
        if elem != "":
            elem = elem.split(";;")
            color = elem[1]
            pos = []
            # generate the tetramino
            tetramino = elem[0].split(";")
            for tetra_pos in tetramino:
                # transform to a tuple
                tetra_pos = eval(tetra_pos)
                pos.append(tetra_pos)

            gap = (0, 0)

            tetramino = [pos, color, gap]
            tetramino_list.append(tetramino)
            i += 1

    return size, tetramino_list


def setup_tetraminos(tetraminos, grid):
    """
    Set up the tetraminos on the grid by adding a gap to each tetramino
    :param tetraminos: list of tetraminos
    :param grid: list of the grid
    :return: tuple : grid with tetraminos inside and updated tetraminos
    """
    # Initialize vars
    width = len(grid[0])
    height = len(grid)
    number = 1


    for tetramino in tetraminos:
        # Initialize vars
        pos = tetramino[0]
        color_code = tetramino[1]
        default_gap = generate_gap(number, width, height)
        gap = [tetramino[2][0] + default_gap[0], tetramino[2][1] + default_gap[1]]
        tetramino[2] = gap

        # place the tetramino on the grid
        for x, y in pos:
            grid[y + gap[1]][x + gap[0]] = '\x1b[' + color_code + 'm' + f"{number} " + RESET_COLOR

        number += 1

    return grid, tetraminos


def place_tetraminos(tetraminos: list, grid: list):
    """
    Place the tetraminos on the grid
    :param tetraminos: list of tetraminos
    :param grid: list of the grid
    :return: new grid with placed tetraminos
    """
    # Create a new grid with the same size as the grid
    grid = create_grid((len(grid[0])-2)//3, (len(grid)-2)//3)
    number = 1
    for tetramino in tetraminos:
        # Initialize vars
        pos = tetramino[0]
        color_code = tetramino[1]
        gap = tetramino[2]

        # place the tetramino on the grid
        for x, y in pos:
            # Check if the bloc is empty
            if grid[y + gap[1] ][x + gap[0] ] == SPACE*2:
                tetramino_index = str(number) + SPACE
            else:
                tetramino_index = "XX"
            grid[y + gap[1] ][x + gap[0]] = ('\x1b[' + color_code + 'm' + tetramino_index + RESET_COLOR)

        number += 1

    return grid


def rotate_tetramino(tetramino, clockwise: bool = True):
    """
    Rotate the tetramino clockwise or counterclockwise
    :param tetramino: tetramino to rotate
    :param clockwise: boolean to rotate clockwise or counterclockwise
    :return: new tetramino rotated with new coordinates
    """
    # Initialize vars
    pos = tetramino[0]

    for pos_x, pos_y in pos:
        if clockwise:
            new_pos = (-pos_y, pos_x)
        else:
            new_pos = (pos_y, -pos_x)
        pos[pos.index((pos_x, pos_y))] = new_pos # replace the old pos by the new pos

    return tetramino


def check_move(tetramino, grid):
    """
    Check if the tetramino can move
    :param tetramino: tetramino to move
    :param grid: grid 
    :return: True if the pos is valid, False otherwise
    """
    # Initialize vars
    tetramino_pos = tetramino[0]
    gap = tetramino[2]
    color_code = tetramino[1]

    for x, y in tetramino_pos:
        try:
            bloc_pos = grid[y + gap[1]][x + gap[0]]
        except:
            return False
        # Check if the bloc is empty or if its already the current tetramino
        validate_bloc_pos = [('\x1b[' + color_code + 'm' + str(i) + SPACE + RESET_COLOR) for i in range(1,9) ]
        if bloc_pos != SPACE*2 and bloc_pos not in validate_bloc_pos:
            return False
    return True


def check_win(grid):
    """
    Check if the player won
    :param grid: grid
    :return: True if the player won, False otherwise
    """
    # Initialize vars
    w = (len(grid[0])-2)//3
    h = (len(grid)-2)//3

    # Check if the grid is full
    for i in range(w+1, 2*w+1):
        for j in range(h+1, 2*h+1):
            if grid[j][i] == SPACE*2:
                return False

    return True


def print_grid(grid: list, no_number: bool):
    """
    Print the grid
    :param grid: list of the grid
    :param no_number: boolean to print the number of the grid
    :return: None
    """

    # Initialize vars
    width = len(grid[0])
    display_grid = list(map(list, grid))
    START_CASE_NUMBER = 10
    END_CASE_NUMBER = 12

    if no_number:
        # Remove the number of each valid tetraminos
        for row in display_grid:
            for i in range(width):
                # Check if the bloc is a valid tetramino
                if "\x1b[" in row[i] and row[i][START_CASE_NUMBER:END_CASE_NUMBER] != "XX":
                    row[i] = row[i][0:START_CASE_NUMBER] + SPACE*2 + RESET_COLOR

    # Vertical Border
    for row in display_grid:
        row.insert(0, VERTICAL_SEP) # left
        row.append(VERTICAL_SEP) # right
    # Horizontal Border
    display_grid.insert(0, [HORIZONTAL_SEP for _ in range(width+1)]) # top
    display_grid.append([HORIZONTAL_SEP for _ in range(width+1)]) # bottom

    # Print the grid
    for row in display_grid:
        print("".join(row)) # Print each row

    return None


def main():
    """
    Tetramino game
    :return: True when the player won
    """
    title_screen()  # Welcome message

    # Initialize vars
    win = False

    # Import the card from the .txt file specified in the command line
    try:
        card = sys.argv[1]
    except:
        error("No card specified", "Usage : python3 tetramino.py <card.txt>")

    size, map_tetraminos = import_card(card)  # Get the size and the tetraminos
    grid = create_grid(size[0], size[1])  # Create the grid with the size of the cards
    grid, tetraminos = setup_tetraminos(map_tetraminos, grid)  # Set up the tetraminos 

    while not win:
        # Print the grid
        print_grid(grid, False)

        num_tetramino = None
        range_tetramino = len(tetraminos)+1

        # Select a tetramino
        while num_tetramino not in range(1,range_tetramino):
            num_tetramino = getkey()
            try:
                num_tetramino = int(num_tetramino)
            except:
                num_tetramino = None

        # Initialize vars
        selected_tetramino = tetraminos[num_tetramino-1]
        old_gap = selected_tetramino[2]
        select_move = None
        validate_move = None

        # Print the grid
        clear()
        print_grid(grid, True)

        validate_move = False

        while not validate_move:
            # get the key pressed
            select_move = getkey()
            # Convert the selected tetramino to a list to modify it
            selected_tetramino[2] = list(selected_tetramino[2])
            
            try:
                match select_move:
                    case "i": selected_tetramino[2][1] -= 1  # up
                    case "k": selected_tetramino[2][1] += 1  # down
                    case "j": selected_tetramino[2][0] -= 1  # left
                    case "l": selected_tetramino[2][0] += 1  # right
                    case "u": selected_tetramino = rotate_tetramino(selected_tetramino, False)  # rotate counterclockwise
                    case "o": selected_tetramino = rotate_tetramino(selected_tetramino, True)  # rotate clockwise
                    case "v": validate_move = True if check_move(selected_tetramino, grid) else None  # validate the move 
                    case "r": selected_tetramino[2] = old_gap  # reset the tetramino position to his previous pos
            except: 
                pass # If the tetramino is out of the grid, pass
            finally:
                grid = place_tetraminos(tetraminos, grid)
                clear()
                print_grid(grid, True)  # Print the grid

        # Check if the player won
        clear()
        win = check_win(grid)

    # Win message    
    print_grid(grid, True)
    print(LIGHT_BLUE + SEP_LINE)
    print(GRAY + "  Tetramino — Game Finished")
    print(GREEN + "  🎉 GG, you won !")
    print(LIGHT_BLUE + SEP_LINE + RESET_COLOR)

    return True


if __name__ == '__main__':
    main()
