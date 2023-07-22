# Example file showing a circle moving on screen
import pygame

# pygame setup
pygame.init()
pygame.display.set_caption('Space Invaders')
# 4:3 screen format
screen = pygame.display.set_mode((900, 600))
clock = pygame.time.Clock()
running = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
