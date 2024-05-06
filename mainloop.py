#creating main loop
#starting to put everything together
"""
import and visual set up:
"""
#import and initialize
import random
import string
import pygame
pygame.init()
pygame.font.init()

#set up screen
screen_width = 1200
screen_height = 850
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Strands')
clock = pygame.time.Clock()

#define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (170, 170, 170)
LIGHTBLUE = (140, 206, 237)
YELLOW = (255, 217, 46)
BOARDGRAY = (128, 128, 128)

#define grid (with location)
board_cols = 6
board_rows = 8
font_size = 32
board_width = 420
board_height = 560
letter_font = pygame.font.SysFont('any_font', 32)

###taken from click_function.py; edited some variables
#generating letters in board
def generate_board():
    all_letters = string.ascii_uppercase
    return[[random.choice(all_letters) for _ in range (board_cols)] for _ in range(board_rows)]

#formatting the cells of the board
def draw_board(screen, board, clicked_cells, font):
    cell_width = board_width // board_cols
    cell_height = board_height // board_rows

    #added on by yuki for location of board
    start_board_x = 600
    start_board_y = 145

    #drawing letters in correct locations
    for row_index in range(board_rows):
        for col_index in range(board_cols):
            letter = board[row_index][col_index]
            x = start_board_x + col_index * cell_width
            y = start_board_y + row_index * cell_height

            #rectangular coordinates for letter fill: base code below are all from click_function.py
            cell_rect = pygame.Rect(x, y, cell_width, cell_height)

            letter_dim = pygame.draw.rect(screen, BOARDGRAY, cell_rect)
            #drawing the gray when clicked
            if (row_index, col_index) in clicked_cells:
                letter_dim
            else:
                pygame.draw.rect(screen, WHITE, cell_rect)
            #center alignment added by yuki
            letter_surface = letter_font.render(letter, True, BLACK)
            letter_alignment = letter_surface.get_rect(center = letter_dim.center)
            screen.blit(letter_surface, letter_alignment)


#i probably have to define the textfile and word strands here?


#creating the textbox
#given textbox text
def draw_textbox(x, y, width, height, text, font_size, rectcolor, border=True):
    theme_font = pygame.font.SysFont('any_font', font_size)
    the_text = theme_font.render(text, True, BLACK)
    textbox_dim = pygame.Rect(x, y, width, height)
    textbox_rect = pygame.draw.rect(screen, rectcolor, textbox_dim)
    #to create border for one box
    if border:
        pygame.draw.rect(screen, GRAY, textbox_dim, 2)
    text_alignment = the_text.get_rect(center = textbox_dim.center) #help by chatGPT
    screen.blit(the_text, text_alignment)
                


#text [blank] out of [blank] words found

"""
useful syntax?
    display.set.mode(): sets screen size, returns surface object we assign to variable screen
        screen = display.set.mode((640, 240))
    write colors using capitals to keep it constant
    screen.fill(): fill(color) fills whole screen with specified color
    pygame.display.update(): to show the changes
    event.type
    event.key
    from pygame.locals import *: to import all the keys, 280 constants defined in pygame
    pygame.display.set_caption(title): change caption title of the application window
"""


"""
running the game loop:
"""
def main():
    clock = pygame.time.Clock()

    game_board = generate_board()
    clicked_cells = set()

    running = True
    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
        #added click_function.py
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x_hit, y_hit = pygame.mouse.get_pos()
                col = (x_hit - 600) // 70
                row = (y_hit - 145) // 70
                clicked_cells.add((row,col))

                print("Clicked cell (row, col):", (row, col))  # Print clicked cell coordinates for debugging
                if 0 <= row < board_rows and 0 <= col < board_cols:
                    clicked_cells.add((row, col))  # Only add clicked cells within board dimensions
                else:
                    print("Clicked outside of board range.")

        screen.fill(WHITE)

        #generated theme display textbox
        draw_textbox(170, 324, 280, 100, 'YAY', 40, WHITE, border=True) #f'{random_theme}'
        #'THEME' textbox
        draw_textbox(170, 300, 280, 24, 'THEME', 22, LIGHTBLUE, border=False)
        #strands board!
        draw_board(screen, game_board, clicked_cells, letter_font)

        pygame.display.flip()
        clock.tick(30)

    """
    dictionary api:
    """



    """
    starting off the crossword:
    includes random textfile generation AND selecting words from file into a strand
    """
        #random generation of textfile



    """
    general other syntax for running game
    """
        #update display: pygame.display.flip()
        #control frame rate: pygame.time.Clock().tick(60)
    pygame.quit()

if __name__ == '__main__':
    main()