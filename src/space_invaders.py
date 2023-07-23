import pygame
import board

# Pygame setup
pygame.init()
pygame.display.set_caption('Space Invaders')

# 4:3 screen format
screen = pygame.display.set_mode((900, 600))
clock = pygame.time.Clock()
running = True

board = board.Board(screen.get_width(), screen.get_height())

while running:
    # Pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a color to wipe away anything from last frame
    screen.fill("black")
    # Display the elements of the game (invaders, player)
    board.display_board(screen)

    # Flip() the display to put your work on screen
    pygame.display.flip()

    # Limits FPS to 60
    clock.tick(60)

pygame.quit()