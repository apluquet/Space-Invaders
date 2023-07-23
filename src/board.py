import pygame
import numpy as np

# This class represents the bord of Space Invaders. It manages the position of
# each element.
class Board:
    # Private class variables
    __nb_squares_width = 20
    __nb_invaders_cols = 11
    __nb_invaders_lines = 5

    # Class initialization
    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self.__time = 0

        self.__invader_square_size = self.__width / self.__nb_squares_width

        self.__invaders = np.ones((self.__nb_invaders_lines, self.__nb_invaders_cols),
        dtype=int)


    # Class methods
    def display_board(self, screen):
        # Display the invaders
        for i in range (self.__nb_invaders_cols):
            for j in range (self.__nb_invaders_lines):

                if (self.__invaders[j,i]):
                    pygame.draw.rect(screen, "red",
                    pygame.Rect(i * self.__invader_square_size,
                    j * self.__invader_square_size,30, 30))

        # Display the player
        player_width = 40
        pygame.draw.rect(screen, "green", pygame.Rect(self.__width / 2 -\
            player_width / 2, self.__height - player_width, player_width,
            player_width))