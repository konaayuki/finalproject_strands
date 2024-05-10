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

############################accessing datamuse api and word list generation
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
    #prints out retrieved - a list of dictionaries
    
    #extract values of the 'word' key in each dictionary
    #put them into list of strings
    related_words_prot = [dic['word'] for dic in retrieved]
    #print(related_words_prot)   #debug

    #limit word length and omit non alphabetic symbols
    related_words_fin = [term for term in related_words_prot if len(term) <= 10 and term.isalpha()]
    #print(related_words_fin)    #debug
    return related_words_fin

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


############################generating letters in board
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
def checking_valid_words():
    return 

#list = combination
def count_total_words():
    total_words = 0
    for word in combination:
        each_word = combination.split()
        total_words += len(each_word)
    return total_words


"""
running the game loop:
"""
# new function to draw clicked letters at the top of the board 
def draw_clicked_letters(screen, clicked_letters, font, x, y):
    display_text = ''.join(clicked_letters)
    text_surface = font.render(display_text, True, BLACK)
    screen.blit(text_surface, (x, y))

def main():
    game_board = generate_board()
    clicked_cells = set()
    last_clicked_cell = None # to track whether next letter is adjacent
    clicked_letters = [] # tracking clicked letters for display

    global global_select_theme

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        #added click_function.py
        # added absolute value function
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in (4, 5):
                    continue
                x_hit, y_hit = pygame.mouse.get_pos()
                col = (x_hit - 600) // (board_width // board_cols)
                row = (y_hit - 145) // (board_height // board_rows)

                #print("Clicked cell (row, col):", (row, col))  # Print clicked cell coordinates for debugging
                if 0 <= row < board_rows and 0 <= col < board_cols: 
                    if (row, col) == last_clicked_cell: #to reset and try a new word (user initiated by clicking the same last letter twice)
                        clicked_cells.clear()
                        clicked_letters.clear()
                    else:
                            
                        # condition using absolute value to check distance between clicks
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
                
            

        screen.fill(WHITE)

      
        

        #generated theme display textbox
        
        draw_textbox(170, 324, 280, 100, global_select_theme, 40, WHITE, border=True) #f'{random_theme}'
        #'THEME' textbox
        draw_textbox(170, 300, 280, 24, 'THEME', 22, LIGHTBLUE, border=False)
        #strands board!
        draw_board(screen, game_board, clicked_cells, letter_font)
        #calling clicked letters to display them 
        draw_clicked_letters(screen, clicked_letters, letter_font, 600, 100)

        pygame.display.flip()
        clock.tick(30)



    pygame.quit()

if __name__ == '__main__':
    
    main()
   
    