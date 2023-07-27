import pygame
from game import Game

# Pygame setup
pygame.init()
pygame.display.set_caption("Space Invaders")

screen = pygame.display.set_mode((700, 800))
clock = pygame.time.Clock()
running = True
playing = True

game = Game(screen.get_width(), screen.get_height())


def wait_enter_key():
    # Wait for enter before quit
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return


while running and playing:
    # Pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a color to wipe away anything from last frame
    screen.fill("black")
    # Display the elements of the game (invaders, player, other elements)
    time = pygame.time.get_ticks()
    playing = game.play(screen, time)

    # Flip() the display to put your work on screen
    pygame.display.flip()

    # Limits FPS to 60
    clock.tick(60)

# Wat for ENTER key before leaving the game
if not playing:
    wait_enter_key()

pygame.quit()
