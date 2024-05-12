import random
import requests
import string
import os
import pygame
#import pyenchant

# currently - need to make double click time longer
# need to make it so that the word clears from the top of board after 
# double click and if the word is 

pygame.init()
pygame.font.init()

#set up screen
screen_width = 1200 #
screen_height = 750 #
screen = pygame.display.set_mode((screen_width, screen_height)) #
pygame.display.set_caption('Strands')#
clock = pygame.time.Clock()#

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
font_size = 32 #
board_width = 420
board_height = 420
letter_display_height = 50 
letter_font = pygame.font.SysFont('any_font', 32) #

# global variables — making more variables global 

is_valid_word = [] # storing correct but non-theme words found
is_theme_word = [] # storing theme words found
correct_indices = [] # storing indices of the cells of correct but non-theme words for a possible hint button
theme_indices = [] # storing indices of the cells of theme words to highlight the word

combination, clicked_letters, used_letters = [], [], [] 
clicked_cells = set()
double_click_time = 0 
last_click_time = 0 
last_clicked_cell = None

# FOR DRAW_BOARD 

cell_width = board_width // board_cols
cell_height = board_height // board_rows
start_board_x = 600
start_board_y = 145




"""
getting words used in game:
"""
#searches for:
#words that have related meaning to query word/phrase
#max 50 words per query
#limited to words > 3 letters
def datamuse_api_get(query):
    url = 'https://api.datamuse.com'
    response = requests.get(f'{url}/words?rel_trg={query}&sp>???&max=100')
    return response.json()
    
global_select_theme = None
#getting related words from a theme
def get_related_words():
    global global_select_theme
    #chooses a random theme from a created list
    themes = ['music', 'literature', 'weather', 'school', 'technology', 'city', 'farm', 'shopping', 'biomes', 'beach', 'puzzles', 'party', 'sports','halloween']
    global_select_theme = random.choice(themes)
    retrieved = datamuse_api_get(global_select_theme)
    related_words_prot = [dic['word'] for dic in retrieved]
    related_words_fin = [term for term in related_words_prot if len(term) <= 10 and term.isalpha()]
    return related_words_fin


#creating text file for retrieved words
def creating_word_list_file(theme, related_words):
    file_path = f'{theme}.txt'
    with open(file_path, 'w') as file:
        for string in related_words:
            file.write(string + '\n')
    return file_path

#reloading the text file
def load_file(file_path):
    with open(file_path, 'r') as file:
        return file.read().splitlines()
    
#system to randomly find word combinations that add up to total of 25 letters
def generate_random_combination(list, target_length):
    combination = []
    current_length = 0

    while current_length < target_length and list:
        term = random.choice(list)
        if current_length + len(term) <= target_length:
            combination.append(term)
            current_length += len(term)
            list.remove(term)

        else:
            remaining_length = target_length - current_length
            shorter_word = [w for w in list if len(w) <= remaining_length]
            if shorter_word:
                term = random.choice(shorter_word)
                combination.append(term)
                current_length += len(term)
                list.remove(term)
            #when it doesn't reach 25, add blank spaces
            else:
                blank_length = target_length - current_length
                blank_space = '-' * blank_length
                combination.append(blank_space)
                current_length += blank_length
    return combination

#running the combination system
related_words = get_related_words()
file_path = creating_word_list_file(global_select_theme, related_words)
list = load_file(file_path)
combination = generate_random_combination(list, 25)
print(combination)

# this functions tracks whether a word matches any correct word in the english language and if it matches words in the theme 
def check_word(complete_word, board): 
    #dict_checker = pyenchant.Dict('en_US')
    #if dict_checker.check(complete_word):
        global theme_indices
        if complete_word in combination: 
            # appending theme word to complete word and indices to theme_indices 
            is_theme_word.append(complete_word) 
            word_length = len(complete_word)
            theme_indices = [i for i in range(len(combination)) if combination[i:i+word_length] == complete_word]
        
        else: 
            print("not a valid word")
        
    #return is_valid_word, is_theme_word

"""
generating board:
"""
#def generate_board():
    #all_letters = string.ascii_uppercase
    #return[[random.choice(all_letters) for _ in range (board_cols)] for _ in range(board_rows)]

#formatting the cells of the board
def draw_board(screen, board, clicked_cells):
    #cell_width = board_width // board_cols
    #cell_height = board_height // board_rows

    #added on by yuki for location of board

    #drawing letters in correct locations
    # changed row_index to row 

    
    for row in range(board_rows):
        for col in range(board_cols):
            x = start_board_x + col * cell_width
            y = start_board_y + row * cell_height
            cell_rect = pygame.Rect(x, y, cell_width, cell_height)
            
            color = WHITE
            if (row, col) in theme_indices:
                color = YELLOW 
            elif (row, col) in clicked_cells:
                color = GRAY

            pygame.draw.rect(screen, color, cell_rect)
    
            letter = board[row][col]
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
            
#display the word list

wordlist_font = pygame.font.SysFont('any_font', 30)
def display_wordlist(screen, font, x, y):
    wordlist_surface = ', '.join(combination)
    wordlist = font.render(wordlist_surface, True, BLACK)
    screen.blit(wordlist, (x, y))
    
#draw clicked letters at the top of the board 
def draw_clicked_letters(screen, clicked_letters, font, x, y):
    display_text = ''.join(clicked_letters)
    text_surface = font.render(display_text, True, BLACK)
    screen.blit(text_surface, (x, y))

#GENERATING PATHS FUNCTIONS BELOW
#function to check if the next move in the path is a valid one
def is_valid_move(x, y, board_rows, board_cols, visited):
    return 0 <= x < board_rows and 0 <= y < board_cols and (x, y) not in visited

#function to find paths
def find_paths(x, y, board_rows, board_cols, path, visited, paths):
    path.append((x, y)) #appends the current position to the path
    visited.add((x, y)) #adds the current position to the visited list

    if len(path) == board_rows * board_cols: #checks if the length of the path is equal to all the spaces in the grid
        paths.append(path.copy()) #appends the current path to the path list as it is a valid path
        return #once a valid path is found, RETURN AND STOP HERE
        
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1),(-1,-1),(1,1),(1,-1),(-1,1)]: #looks over the 4 possible directions (up/down/left/right)
        nx, ny = x + dx, y + dy #calculates next direction
        if is_valid_move(nx, ny, board_rows, board_cols, visited): #checks if it is a valid move
            find_paths(nx, ny, board_rows, board_cols, path, visited, paths)
    
    visited.remove((x, y))
    path.pop()

#function that replaces the spaces on the board with letters in the combination list
def fill_board(board, combination,all_paths):

    split_list = [] #define an empty list to store each letter in combination individually

    for word in combination: #a loop to run through each word in combination
        for letter in word: #a loop to run through each letter in each word
            split_list.append(letter) #append the letter to the list
    #print('length of split_list:', len(split_list))
    #print("length of hamiltonian path:", all_paths[0])

    for i in range (0, len(all_paths[0])):  #a loop that runs from 0 to the length of the hamiltonian path
        x,y = all_paths[0][i] #assigns a letter to the coordinate x,y
        board[x][y] = split_list[i] #replaces the board at x,y with the corresponding letter for that position

    return board #return the variable

def generate_hamiltonian_paths(board_rows, board_cols):
    paths = [] #define empty list
    start_x, start_y = random.randint(0, board_rows-1), random.randint(0, board_cols-1) #randomly generate starting position for the path
    find_paths(start_x, start_y, board_rows, board_cols, [], set(), paths) #call the function to find paths
    return paths #return the variable

#chatgpt was consulted for the generation of hamiltonian paths


# new function to handle click and check for double click based on time 
def handle_click(board, col, row): 
    global last_click_time, clicked_letters, last_clicked_cell, clicked_cells

    # tracking time of current click
    current_time = pygame.time.get_ticks() 
    # if click within the board space 
    if 0 <= row < board_rows and 0 <= col < board_cols: 
        # making sure that the next click is adjacent to the last click 
        if last_clicked_cell is None or (
            abs(last_clicked_cell[0] - row) <= 1 and
            abs(last_clicked_cell[1] - col) <= 1):

            if current_time - last_click_time < 500: # large margin to detect double click - still have to click fast 
                complete_word = ''.join(clicked_letters).lower()
                # entering word into check word function if double clicked
                check_word(complete_word, board)
                clicked_letters = [] # clear letters from top of board 
                last_clicked_cell = None
                #clicked_cells = []
                clicked_celss = set()
            else: 
                # should interact with draw_board to turn letters gray
                clicked_letters.append(board[row][col])
                last_clicked_cell = (row, col)
                clicked_cells.add((row, col))


            last_click_time = current_time # reset 
    else: 
        # clearing clicked cells if someone clicks elsewhere
        clicked_letters = [] # clear letters from top of board 
        last_clicked_cell = None
        clicked_cells.clear()
        # do I have to call draw_board? 

"""
running the game loop:
"""
def main():
    board = [[ '_' for i in range(board_rows)] for j in range(board_cols)]
    all_paths = generate_hamiltonian_paths(board_rows, board_cols)
    board = fill_board(board, combination,all_paths)
 
    global global_select_theme


    running = True
    while running:

        pygame.display.flip()
        draw_board(screen, board, clicked_cells)
        screen.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x_hit, y_hit = pygame.mouse.get_pos()
                col = (x_hit - 600) // (board_width // board_cols)
                row = (y_hit - 145) // (board_height // board_rows)

                if 0 <= row < board_rows and 0 <= col < board_cols: # repeat from handle_click, dk where it should go
                    handle_click(board, col, row)

        

        #generated theme word textbox
        draw_textbox(150, 324, 280, 100, global_select_theme, 40, WHITE, border=True) #f'{random_theme}'
        #'THEME' textbox
        draw_textbox(150, 300, 280, 24, 'THEME', 22, LIGHTBLUE, border=False)
        #strands board!
        draw_board(screen, board, clicked_cells)
        #calling clicked letters to display them 
        draw_clicked_letters(screen, clicked_letters, letter_font, 600, 100)
        #drawing wordlist
        display_wordlist(screen, wordlist_font, 150, 450)
        #draw_hint_button(screen, hint_button_active, 3 - len(correct_words))

        pygame.display.flip()
        clock.tick(30)



    pygame.quit()

if __name__ == '__main__':
    
    main()