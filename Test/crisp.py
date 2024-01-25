import pygame
import sys
import os

os.environ["SDL_HIGHDPI_DISABLED"] = "1"
pygame.init()


print(pygame.display.Info())
# Set display mode

print(pygame.display.get_desktop_sizes())
width, height = 800, 600
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption('Crisp Text Demo')

# Load font
font_size = 36
font = pygame.font.Font('/System/Library/Fonts/Supplemental/Arial Bold.ttf', font_size)

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Render text with anti-aliasing
    text_surface = font.render('Crisp Text Demo', True, (255, 255, 255))

    # Scale text manually if needed
    scaled_width, scaled_height = 400, 100
    text_surface = pygame.transform.scale(text_surface, (scaled_width, scaled_height))

    # Blit text to the center of the screen
    screen.fill((0, 0, 0))
    screen.blit(text_surface, ((width - scaled_width) // 2, (height - scaled_height) // 2))

    pygame.display.flip()
