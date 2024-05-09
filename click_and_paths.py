
# creating random game board 
import random 
import string 
import pygame

# defining colors 
black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)

# screen width, height, etc 
screen_width = 800 
screen_height = 600 
board_cols = 5
board_rows = 5
font_size = 32
letter_display_height = 50 

combination = ['DREAM', 'PIE', 'CHALK', 'TOP','SPOT', 'SPIKE']
board = [[ '_' for i in range(5)] for j in range(5)]
word_found = False #if a word has been found

def is_valid_move(x, y, rows, cols, visited):
    return 0 <= x < rows and 0 <= y < cols and (x, y) not in visited

def find_paths(x, y, rows, cols, path, visited, paths):
    path.append((x, y)) #appends the current position to the path
    visited.add((x, y)) #adds the current position to the visited list

    if len(path) == rows * cols: #checks if the length of the path is equal to all the spaces in the grid
        paths.append(path.copy()) #appends the current path to the path list as it is a valid path
        return #once a valid path is found, RETURN AND STOP HERE
        
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1),(-1,-1),(1,1),(1,-1),(-1,1)]: #looks over the 4 possible directions (up/down/left/right)
        nx, ny = x + dx, y + dy #calculates next direction
        if is_valid_move(nx, ny, rows, cols, visited): #checks if it is a valid move
            find_paths(nx, ny, rows, cols, path, visited, paths)
    
    visited.remove((x, y))
    path.pop()

def fill_board(board, combination,all_paths):

    split_list = []
    for word in combination:
        for letter in word:
            split_list.append(letter)

    for i in range (0, len(all_paths[0])): 
        x,y = all_paths[0][i]
        board[x][y] = split_list[i]

    return board

def generate_hamiltonian_paths(rows, cols):
    paths = []
    start_x, start_y = random.randint(0, rows-1), random.randint(0, cols-1) #randomly generate starting position for the path
    find_paths(start_x, start_y, rows, cols, [], set(), paths)
    return paths, (start_x, start_y)

#GENERATE PATHS IN A GRID
rows, cols = 5,5
all_paths, start_point = generate_hamiltonian_paths(rows, cols)
fill_board(board, combination,all_paths)

# function to format cells and stylize board 
def draw_board(screen, board, clicked_cells, font, clicked_letters): 
  cell_width = screen_width // board_cols
  cell_height = screen_height // board_rows

  #displaying letters at the top of the screen: 
  display_text = ''.join(clicked_letters)
  text_surface = font.render(display_text, True, white)
  screen.blit(text_surface, (10, 10))

  clicked_word = ''.join(clicked_letters)
  
  valid_word = clicked_word in combination #checks if clicked_word is in test_list (True or False)
  
  #valid/invalid cases (i.e. 2 ways to get one word)
  valid_path = False
  for path in all_paths:
      path_order = [board[row][col] for row,col in path]
      if clicked_word == ''.join(path_order):
          valid_path = True

  # drawing letters in the correct spaces
  for row_index in range(board_rows): 
    for col_index in range(board_cols):
      letter = board[row_index][col_index]
      x = col_index * cell_width
      y = row_index * cell_height + letter_display_height # adding display here
      
      # rectangular coordinates for fill  
      cell_rect = pygame.Rect(x, y, cell_width, cell_height)

      # drawing gray if clicked 
      if (row_index, col_index) in clicked_cells: 
        if valid_word and valid_path: #if true (it is a valid word)
            pygame.draw.rect(screen, (170,220,230), cell_rect) #turn blue
        else:
            pygame.draw.rect(screen, gray, cell_rect)

      else: 
        pygame.draw.rect(screen, black, cell_rect)

      text_surface = font.render(letter, True, white)
      screen.blit(text_surface, (x + 10, y + 10))

def main(): 
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Strands")
    font = pygame.font.SysFont(None, font_size)
    clock = pygame.time.Clock()

    game_board = fill_board(board, combination, all_paths)
    clicked_cells = set()
    clicked_letters = [] # tracking clicked letters for display
    last_clicked_cell = None # to track whether next letter is adjacent

    running = True 
    word_found = False
    while running: 
        
            for event in pygame.event.get():
            
                if event.type == pygame.QUIT: 
                    running = False 
                elif event.type == pygame.MOUSEBUTTONDOWN: 
                # edit 
                    x, y = pygame.mouse.get_pos()
                    col = x // (screen_width // board_cols) 
                    row = (y - letter_display_height) // ((screen_height - letter_display_height) // board_rows)
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

                                if word_found and clicked_word not in combination: 
                                    last_clicked_cell = (row, col)
                                    #if a word was found in the previous turn 

                                print(f"valid click") #debug
                            else: 
                                print(f'not a valid click')
                    else: # clear board if player clicks outside of cells
                    #    clicked_letters.clear()
                    #    clicked_cells.clear()
                    #    last_clicked_cell = None
                       print("Cleared board") #debug
            
        
            screen.fill(black)
            draw_board(screen, game_board, clicked_cells, font, clicked_letters)
            pygame.display.flip()
            clock.tick(30)


    pygame.quit()
      

if __name__ == '__main__':
    main()

#print (board)