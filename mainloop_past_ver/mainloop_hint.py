#creating main loop
#starting to put everything together
# make it so that you cannot click on a letter twice 
# make the words turn blue if correct and yellow if in the theme 
# hint button gives words 
# game over/replay 
# print related words — combination stores the words in the theme

# currently: 
    # displays clicked letters, but does not clear when click elsewhere 
    # does not correctly access dictionary API to check whether letter is valid and not within the theme words
    # hint button off center and text is larger than button — also, want to display number of words until hint 



"""
import and visual set up:
"""
#import and initialize
import random
import requests
import string
import pygame

pygame.init()
pygame.font.init()

#set up screen
screen_width = 1200
screen_height = 750
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
board_cols = 5
board_rows = 5
font_size = 32
board_width = 420
board_height = 420
letter_display_height = 50 
letter_font = pygame.font.SysFont('any_font', 32)

#definitions for hint button: 
hint_button_active = False 
hint_active = False 
hinted_cells = [] # to highlight hinted cells 
correct_words = [] # storing correct but non-theme words

############################accessing datamuse api and word list generation

#searches for:
#words that have related meaning to query word/phrase
#max 50 words per query
#limited to words > 3 letters

def datamuse_api_get(query):
    url = f'https://api.datamuse.com/words?ml={query}&sp>???&max=50'
    return requests.get(url).json()
    
#getting related words from a theme
def get_related_words():
    #chooses a random theme from a created list
    themes = ['music', 'literature', 'weather', 'school', 'technology', 'city', 'farm', 'shopping', 'biomes', 'beach', 'puzzle+games', 'party+goods', 'sports']
    random_theme = random.choice(themes)
    words = [word['word'] for word in datamuse_api_get(random_theme) if word['word'].isalpha() and len(word['word']) <= 10]
    return random_theme, words
       
#creating text file for retrieved words
def creating_word_list_file(theme, related_words):
    #creating the textfile
    file_path = f'{theme}.txt'
    with open(file_path, 'w') as file:
        for string in related_words:
            file.write(string + '\n')
    #print("Text file created successfully:", file_path)  # Print the path of the created file
    return file_path
#reloading the text file
def load_file(file_path):
    with open(file_path, 'r') as file:
        return file.read().splitlines()
    
#system to randomly find word combinations that add up to total of 25 letters
def generate_random_combination(list, target_length):
    #initiate 
    combination = []
    current_length = 0

    while current_length < target_length and list:
        term = random.choice(list)
        #add term if word doesn't pass limit
        if current_length + len(term) <= target_length:
            combination.append(term)
            current_length += len(term)
            list.remove(term) #remove once used terms to prevent repeats
        else:
            remaining_length = target_length - current_length
            shorter_word = [w for w in list if len(w) <= remaining_length]
            if shorter_word:
                term = random.choice(shorter_word)
                combination.append(term)
                current_length += len(term)
                list.remove(term)
            else:
                break
    return combination

#running the combination system
def find_words_by_count():
    file_path = creating_word_list_file(*get_related_words())
    list = load_file(file_path)
    combination = generate_random_combination(list, 25)
    print(combination)
    return combination

# function to check whether in list/valid word 

def check_word(word): 
    response = requests.get(f'https://api.datamuse.com/words?ml={word}&sp>???&max=50') # start editing here 
    return bool(response), response[0]['word'] if response else word 

                                                

def generate_board():
    all_letters = string.ascii_uppercase
    print('this runs')
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
            cell_rect = pygame.Rect(x, y, cell_width, cell_height)
            
            # changed if statement a bit for gray if clicked
            pygame.draw.rect(screen, BOARDGRAY if (row_index, col_index) in clicked_cells else WHITE, cell_rect)
            letter_surface = letter_font.render(letter, True, BLACK)
            screen.blit(letter_surface, letter_surface.get_rect(center=cell_rect.center))

#drawing textboxes
def draw_textbox(x, y, width, height, text, font_size, rectcolor, border=True):
    theme_font = pygame.font.SysFont('any_font', font_size)
    the_text = theme_font.render(text, True, BLACK)
    textbox_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, rectcolor, textbox_rect)
    #to create border for one box
    if border:
        pygame.draw.rect(screen, GRAY, textbox_rect, 2)
    text_alignment = the_text.get_rect(center = textbox_rect.center) #help by chatGPT
    screen.blit(the_text, the_text.get_rect(center = textbox_rect.center))
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
# new function to draw clicked letters at the top of the board 
# make sure this is cleared when click elsewhere
def draw_clicked_letters(screen, clicked_letters, font, x, y):
    display_text = ''.join(clicked_letters)
    text_surface = font.render(display_text, True, BLACK)
    screen.blit(text_surface, (x, y))

def draw_hint_button(screen, active, words_until_hint):
    hint_button_rect = pygame.Rect(50, 650, 200, 50)
    hint_button_color = LIGHTBLUE if active else GRAY 
    pygame.draw.rect(screen, hint_button_color, hint_button_rect)
    # display number of correct words until hint on hint button 
    hint_text_content = "Hint" if active else f"{words_until_hint} words until hint"
    hint_text = letter_font.render("Hint" if active else "get x more letters to display hint", True, BLACK) 
    screen.blit(hint_text, hint_text.get_rect(center=hint_button_rect.center))
    return hint_button_rect

def update_hint_progress(): 
    words_until_hint = 3 - len(correct_words)
    hint_button_active = words_until_hint <= 0
    draw_hint_button(screen, hint_button_active, words_until_hint)

def find_hint_cells(hinted_word, game_board): # locating cells of the letters in the hinted word
    hint_cells = []
    for row_index, row in enumerate(game_board):
        for col_index, letter in enumerate(row):
            if letter in hinted_word: 
                hint_cells.append((row_index, col_index))
    return hint_cells

def hint_cell_interaction(game_board, row, col):
    if (row, col) in hinted_cells:
        # copy paste code from above to pass cell_rect in this function - does not work otherwise
        start_board_x = 600
        start_board_y = 145
        cell_width = board_width // board_cols
        cell_height = board_height // board_rows
        x = start_board_x + col * cell_width
        y = start_board_y + row * cell_height 
        cell_rect = pygame.Rect(x, y, cell_width, cell_height)
        pygame.draw.rect(screen, LIGHTBLUE, cell_rect, 5) 
        
        hinted_cells.remove((row, col)) # when a player clicks, remove cells 


def main():
    theme, words = get_related_words()
    game_board = generate_board()
    clicked_cells = set()
    last_clicked_cell = None # to track whether next letter is adjacent
    clicked_letters = [] # tracking clicked letters for display
    words_until_hint = 3
    hint_active = False
    correct_words = []

    screen.fill(WHITE)
    hint_button_rect = draw_hint_button(screen, hint_button_active, words_until_hint)
    pygame.display.flip()

    running = True

    while running:
        screen.fill(WHITE)
        # checking whether to activate hint button 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        #added click_function.py
        # added absolute value function
            elif event.type == pygame.MOUSEBUTTONDOWN:
            
                if event.button in (1, 3): # left or right click
                    x_hit, y_hit = pygame.mouse.get_pos()
                    col = (x_hit - 600) // (board_width // board_cols)
                    row = (y_hit - 145) // (board_height // board_rows)

                    if 0 <= row < board_rows and 0 <= col < board_cols: # check for valid click
                        if hint_active: 
                            if hint_button_rect and hint_button_rect.collidepoint(x_hit, y_hit):
                                hint_active = False
                                hinted_cells.clear() #clearing previosuly hinted cells 
                            
                            elif (row, col) in hinted_cells:
                                hint_cell_interaction(game_board, row, col)
                                continue 
                        else:
                            if hint_button_active and hint_button_rect and hint_button_rect.collidepoint(x_hit, y_hit):
                                hint_active = True 
                                hinted_word = random.choice(combination) #choose to hint random word
                                hinted_cells = find_hint_cells(hinted_word, game_board) 
                            elif (row, col) == last_clicked_cell: 
                                #ADD CODE TO CHECK WHETHER IN API
                                complete_word = ''.join(clicked_letters).lower()
                                if complete_word: 
                                    is_valid, is_theme_word = check_word(combination, word)
                                    if is_valid: 
                                        if is_theme_word: 
                                            hint_cell_interaction(game_board, row, col) 
                                            clicked_letters.clear()
                                            last_clicked_cell = None

                                        else: 
                                            update_hint_progress()
                                            clicked_letters.clear()
                                            last_clicked_cell = None
                                            clicked_cells.clear()


                            elif last_clicked_cell is None or (
                                abs(last_clicked_cell[0] - row) <= 1 and
                                abs(last_clicked_cell[1] - col) <= 1):
                                    clicked_cells.add((row, col))
                                    clicked_letters.append(game_board[row][col])
                                    last_clicked_cell = (row, col)
                            else: 
                                clicked_cells.clear()
                                clicked_letters.clear()
                                last_clicked_cell = None #reset on click outside grid boundaries

                                    #print(f"valid click") #debug
                                #else: 
                                    #print(f'not a valid click')
                        #else:
                            #print("Cleared board") #debug        

        #generated theme display textbox

        draw_textbox(170, 324, 280, 100, random_theme, 40, WHITE, border=True) #f'{random_theme}'
        #'THEME' textbox
        draw_textbox(170, 300, 280, 24, 'THEME', 22, LIGHTBLUE, border=False)
        #strands board!
        draw_board(screen, game_board, clicked_cells, letter_font)
        #calling clicked letters to display them 
        draw_clicked_letters(screen, clicked_letters, letter_font, 600, 50)

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
    """        #update display: pygame.display.flip()
        #control frame rate: pygame.time.Clock().tick(60)
    pygame.quit()

if __name__ == '__main__':
    random_theme, _ = get_related_words()
    combination = find_words_by_count()
    main(random_theme, combination)