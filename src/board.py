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
        # Screen width and height in pixels
        self.__width = width
        self.__height = height

        # Numpy array saving all invaders
        self.__invaders = np.ones((self.__nb_invaders_lines, self.__nb_invaders_cols),
        dtype=int)

        # Size in pixels of a screen subdivision to place one invader
        self.__invader_square_size = self.__width / self.__nb_squares_width

        # Time in ms between invaders move
        self.__move_time = 500
        # Last time a move was made
        self.__last_move_time = 0

        # For the invaders movement, save the last (x,y) positon of the top
        # right invader
        self.__invaders_last_x = 0
        self.__invaders_last_y = 0

        # For the invaders movement, save if invaders movement is goind right
        # or not
        self.__move_right = True
        # Count the number of moves to know when to shift down
        self.__nb_movements = 1


    # Class methods
    def display_board(self, screen, time):

        move = False
        # Set move to True if enough elapsed time since last movement
        if time - self.__last_move_time > self.__move_time:
            self.__last_move_time += self.__move_time
            move = True

        if move:
            # Set move right of left (!right) depending on the number of
            # movements
            self.__move_right = (((self.__nb_movements) // 10 % 2) == 0)

            # If at a border, shift down : movement on Y axis
            if (self.__nb_movements) % 10 == 0 and self.__nb_movements != 0:
                self.__invaders_last_y += self.__invader_square_size
            # Else, movement on X axis
            else:
                self.__invaders_last_x += self.__invader_square_size\
                    if self.__move_right else -self.__invader_square_size

            self.__nb_movements += 1

        # Display the invaders with movement
        for i in range (self.__nb_invaders_cols):
            for j in range (self.__nb_invaders_lines):

                if (self.__invaders[j,i]):
                    pygame.draw.rect(screen, "red",
                    pygame.Rect(self.__invaders_last_x + i * self.__invader_square_size,
                    self.__invaders_last_y + j * self.__invader_square_size,30, 30))

        # Display the player
        player_width = 40
        pygame.draw.rect(screen, "green", pygame.Rect(self.__width / 2 -\
            player_width / 2, self.__height - player_width, player_width,
            player_width))