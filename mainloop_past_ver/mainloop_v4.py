#creating main loop

"""
import and visual set up:
"""
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
#hint_active = False 
hinted_cells = [] # to highlight hinted cells 
correct_words = [] # storing correct but non-theme words
current_hint_word = None
hint_button_rect = pygame.Rect(50, 650, 200, 50)


"""
getting words used in game:
"""
#searches for:
#words that have related meaning to query word/phrase
#max 50 words per query
#limited to words > 3 letters
def datamuse_api_get(query):
    url = 'https://api.datamuse.com'
    response = requests.get(f'{url}/words?rel_trg={query}&sp>???&max=50')
    return response.json()
    
global_select_theme = None
#getting related words from a theme
def get_related_words():
    global global_select_theme
    #chooses a random theme from a created list
    themes = ['music', 'literature', 'weather', 'school', 'technology', 'city', 'farm', 'shopping', 'biomes', 'beach', 'puzzles', 'party', 'sports','halloween']
    global_select_theme = random.choice(themes)
    #print(random_theme)    #debug
    retrieved = datamuse_api_get(global_select_theme)
    #print(retrieved)   #debug
    related_words_prot = [dic['word'] for dic in retrieved]
    #print(related_words_prot)   #debug
    related_words_fin = [term for term in related_words_prot if len(term) <= 10 and term.isalpha()]
    #print(related_words_fin)    #debug
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
        #add term if word doesn't pass limit
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
            else:
                break
    return combination

#running the combination system
#def find_words_by_count():
    #random_theme, related_words = get_related_words()
related_words = get_related_words()
file_path = creating_word_list_file(global_select_theme, related_words)
list = load_file(file_path)
combination = generate_random_combination(list, 25)
print(combination)

#checking word in list/valid word
def check_word(word): 
    url_2 = f'https://api.datamuse.com/words?sp={word}&md=d&max=1'
    response = requests.get(url_2).json() 
    is_valid = bool(response) # word is valid if any response from API 
    # locates words in combination list 
    is_theme_word = any(word == item['word'] for item in combination) # check the logic here!! 
    return is_valid, is_theme_word 

    return combination


"""
generating board:
"""
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
            cell_rect = pygame.Rect(x, y, cell_width, cell_height)
            
            #gray if clicked
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
def checking_valid_words():
    return 

#list = combination
def count_total_words():
    total_words = 0
    for word in combination:
        each_word = combination.split()
        total_words += len(each_word)
    return total_words

#draw clicked letters at the top of the board 
def draw_clicked_letters(screen, clicked_letters, font, x, y):
    display_text = ''.join(clicked_letters)
    text_surface = font.render(display_text, True, BLACK)
    screen.blit(text_surface, (x, y))

#visualizing hint button
def draw_hint_button(screen, active, words_until_hint):
    hint_button_color = LIGHTBLUE if active else GRAY 
    pygame.draw.rect(screen, hint_button_color, hint_button_rect)
    #display number of correct words until hint on hint button 
    hint_text_content = "Hint" if active else f"{words_until_hint} words until hint"
    hint_text = letter_font.render(hint_text_content, True, BLACK) 
    screen.blit(hint_text, hint_button_rect.center)
    return hint_button_rect

#updating progress for hint button
def update_hint_progress(): 
    #hint button becomes active when three correct word guesses
    words_until_hint = 3 - len(correct_words)
    hint_button_active = words_until_hint <= 0
    draw_hint_button(screen, hint_button_active, words_until_hint)

#calling this function in main loop when the hint button is activated 
#this function should, when the hint button is active, highlight a theme word blue 
def hint_cell_interaction(game_board, combination, row, col, hint_button_active):
    hint_cells = [] #hint cells stores cells of word from combination used as hint 
    for word in combination: 
        for row_index, row in enumerate(game_board):
            for col_index, letter in enumerate(row): 
                if letter in word:
                    hint_cells.append((row_index, col_index))
    for row, col in hint_cells: 
        if hint_button_active: 
        #copy paste code from above to pass cell_rect in this function - does not work otherwise
            start_board_x = 600
            start_board_y = 145
            cell_width = board_width // board_cols
            cell_height = board_height // board_rows
            x = start_board_x + col * cell_width
            y = start_board_y + row * cell_height 
            cell_rect = pygame.Rect(x, y, cell_width, cell_height)
            pygame.draw.rect(screen, LIGHTBLUE, cell_rect, 5) 

        return hint_cells


"""
running the game loop:
"""
def main():
    game_board = generate_board() #generating board
    clicked_cells = set() #to track any clicked cell
    last_clicked_cell = None #to track whether next letter is adjacent
    clicked_letters = [] #tracking clicked letters for display
    hint_button_active = False # initializing hint button within loop
    correct_words = [] # tracking words that are correct in general 
    theme_words = [] # tracking theme words 
    used_letters = set() # tracking letters that are already in guessed words

    global global_select_theme

    screen.fill(WHITE)
    #update_hint_progress()  - call later in game 
    #pygame.display.flip()

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # added absolute value function
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #if event.button in (1, 3): # left or right click
                #tracking position of mouse
                if event.button in (4, 5):
                    continue
                x_hit, y_hit = pygame.mouse.get_pos()
                col = (x_hit - 600) // (board_width // board_cols)
                row = (y_hit - 145) // (board_height // board_rows)

                if hint_button_rect.collidepoint(x_hit, y_hit): # if hint button is clicked
                        if hint_button_active: # if hint button is active 
                            print("hint button active") #debug 
                            # calling hint_cell_interaction to highlight hint button
                            hint_cell_interaction(game_board, combination, row, col, hint_button_active)
                            # calling update hint progress in order to update hint progress 
                            update_hint_progress()

                #click on cells
                if 0 <= row < board_rows and 0 <= col < board_cols: # check for valid click within cell area on board
                        cell_clicked = (row, col)
                        # making sure that the next click is adjacent to the last click 
                        if last_clicked_cell is None or (
                            abs(last_clicked_cell[0] - row) <= 1 and
                            abs(last_clicked_cell[1] - col) <= 1):

                            clicked_cells.add((row, col))
                            clicked_letters.append(game_board[row][col])
                            last_clicked_cell = (row, col)

                            #print(f"valid click") #debug
                        #else: 
                            #print(f'not a valid click')
                #else:
                       #print("Cleared board") #debug
                
            

        

      
        

        #generated theme word textbox
        draw_textbox(170, 324, 280, 100, global_select_theme, 40, WHITE, border=True) #f'{random_theme}'
        #'THEME' textbox
        draw_textbox(170, 300, 280, 24, 'THEME', 22, LIGHTBLUE, border=False)
        #strands board!
        draw_board(screen, board, clicked_cells, letter_font)
        #calling clicked letters to display them 
        draw_clicked_letters(screen, clicked_letters, letter_font, 600, 100)
        draw_hint_button(screen, hint_button_active, 3 - len(correct_words))

        pygame.display.flip()
        clock.tick(30)



    pygame.quit()

if __name__ == '__main__':
    
    main()
   
    