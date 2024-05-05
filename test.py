"""
import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Textbox Example')

# Colors
LIGHT_BLUE = (173, 216, 230)  # Light blue color
WHITE = (255, 255, 255)        # White color
BLACK = (0, 0, 0)              # Black color

# Function to draw a textbox
def draw_textbox(x, y, width, height, text):
    font = pygame.font.SysFont(None, 48)
    text_surface = font.render(text, True, BLACK)
    textbox_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(window, WHITE, textbox_rect)
    pygame.draw.rect(window, LIGHT_BLUE, textbox_rect, 2)  # Border
    text_rect = text_surface.get_rect(center=textbox_rect.center)
    window.blit(text_surface, text_rect)

# Main loop
def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        window.fill((255, 255, 255))  # Fill window with white background
        
        # Draw the first textbox
        draw_textbox(window_width // 3, window_height // 4, window_width // 3, window_height // 6, 'Theme')
        
        # Draw the second textbox
        draw_textbox(window_width // 3, window_height // 4 + window_height // 6 + 20, window_width // 3, window_height // 3, 'Another Textbox')
        
        pygame.display.update()

if __name__ == "__main__":
    main()
    """

import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Textbox Example')

# Colors
LIGHT_BLUE = (173, 216, 230)  # Light blue color
BLACK = (0, 0, 0)              # Black color

# Function to draw a textbox
def draw_textbox(x, y, width, height, text, font_size, color):
    font = pygame.font.SysFont(None, font_size)
    text_surface = font.render(text, True, BLACK)
    textbox_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(window, color, textbox_rect)  # Fill background with light blue
    text_rect = text_surface.get_rect(center=textbox_rect.center)
    window.blit(text_surface, text_rect)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    window.fill((255, 255, 255))
    
    # Draw the textboxes
    draw_textbox(window_width // 3, window_height // 4, window_width // 3, window_height // 6, 'Theme', 48, LIGHT_BLUE)
    draw_textbox(window_width // 3, window_height // 4 + window_height // 6 + 20, window_width // 3, window_height // 3, 'Another Textbox', 36, LIGHT_BLUE)

    # Update the display
    pygame.display.update()

pygame.quit()
