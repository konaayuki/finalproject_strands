#creating main loop
#starting to put everything together
"""
import and visual set up:
"""
#import and initialize
import pygame
pygame.init()

#set up screen
screen_width = 1200
screen_height = 850
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Strands')

#define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (170, 170, 170)
LIGHTBLUE = (140, 206, 237)
YELLOW = (255, 217, 46)

"""
#sets background to white
screen.fill(WHITE)
pygame.display.update()
"""

#define grid (with location)
board_col = 6
board_rows = 8
font_size = 32

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
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    #generated theme display textbox
    draw_textbox(170, 324, 280, 180, 'YAY', 40, WHITE, border=True) #f'{random_theme}'
    #'THEME' textbox
    draw_textbox(170, 300, 280, 24, 'THEME', 22, LIGHTBLUE, border=False)

    pygame.display.update()

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
    #quit: pygame.quit()