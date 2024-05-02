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
board_cols = 6
board_rows = 8
font_size = 32


def generate_board(): 
  all_letters = string.ascii_uppercase
  return [[random.choice(all_letters) for _ in range (board_cols)] for _ in range(board_rows)]

# function to format cells and stylize board 
def draw_board(screen, board, clicked_cells, font): 
  cell_width = screen_width // board_cols
  cell_height = screen_height // board_rows

  # drawing letters in the correct spaces
  for row_index in range(board_rows): 
    for col_index in range(board_cols):
      letter = board[row_index][col_index]
      x = col_index * cell_width
      y = row_index * cell_height
      
      # rectangular coordinates for fill  
      cell_rect = pygame.Rect(x, y, cell_width, cell_height)

      # drawing gray if clicked 
      if (row_index, col_index) in clicked_cells: 
        pygame.draw.rect(screen, gray, cell_rect)
      else: 
        pygame.draw.rect(screen, black, cell_rect)
        # edit: 
      text_surface = font.render(letter, True, white)
      screen.blit(text_surface, (x + 10, y + 10))

def main(): 
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Strands")
    font = pygame.font.SysFont(None, font_size)
    clock = pygame.time.Clock()

    game_board = generate_board()
    clicked_cells = set()

    running = True 
    while running: 
      
      for event in pygame.event.get():
        
        if event.type == pygame.QUIT: 
          running = False 
        elif event.type == pygame.MOUSEBUTTONDOWN: 
          # edit 
          x, y = pygame.mouse.get_pos()
          col = x // (screen_width // board_cols) 
          row = y // (screen_height // board_rows)
          #edit 
          clicked_cells.add((row, col))
          
     
      screen.fill(black)
      draw_board(screen, game_board, clicked_cells, font)
      pygame.display.flip()

      clock.tick(30)

    pygame.quit()
      

if __name__ == '__main__':
  main()