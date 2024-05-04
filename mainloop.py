#creating main loop
#starting to put everything together
"""
import and visual set up:
"""
#import and initialize
import pygame
pygame.init()

#setup display window
screen = pygame.display.set_mode((1200,850))
pygame.display.set_caption('Strands')

#define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHTBLUE = (140, 206, 237)
YELLOW = (255, 217, 46)

#define grid

#i probably have to define the textfile and word strands here?

#define grid (location?)

#theme textbox

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