import pygame
import numpy as np

import player

# This class represents the board of Space Invaders. It manages the position of
# each element.
class Board:
    # Private class variables

    # Step size in pixels for invaders movement
    __step_x_size = 1
    __step_y_size = 15

    __nb_invaders_cols = 11
    __nb_invaders_lines = 5

    __space_btw_invaders = 45
    __invader_size = 20

    # Margin between borders of the window and the game in pixels
    __margin = 20

    # Image of an invader
    __invader_img = pygame.image.load("img/my_invader.png")

    # Class initialization
    def __init__(self, width, height):
        # Screen width and height in pixels
        self.__width = width
        self.__height = height

        # Numpy array saving all invaders
        self.__invaders = np.ones((self.__nb_invaders_lines, self.__nb_invaders_cols),
        dtype=int)

        # Size in pixels of a screen subdivision to place one invader
        #self.__invader_square_size = self.__width / self.__nb_squares_width

        # Time in ms between invaders move
        self.__move_time = 10
        # Last time a move was made
        self.__last_move_time = 0

        # For the invaders movement, save the last (x,y) positon of the top
        # right invader
        self.__invaders_last_x = self.__margin
        self.__invaders_last_y = self.__margin

        # For the invaders movement, save if invaders movement is goind right
        # or not
        self.__move_right = True

        self.__player = player.Player(self.__width / 2, self.__width)

    def __is_at_right_border(self):
        # Check if at right border
        # Current x_pos + nb_cols * size_of_square_with_invader + width_invader
        if self.__invaders_last_x + self.__space_btw_invaders *\
            self.__nb_invaders_cols + self.__invader_size >\
                self.__width - self.__margin:
            return True
        return False

    def __is_at_left_border(self):
        # Check if at left border
        if self.__invaders_last_x - self.__step_x_size < self.__margin:
            return True
        return False

    def __can_move_side(self):
        return (self.__move_right and not self.__is_at_right_border()) or\
            (not self.__move_right and not self.__is_at_left_border())

    # Class methods
    def display_board(self, screen, time):

        move = False
        # Set move to True if enough elapsed time since last movement
        if time - self.__last_move_time > self.__move_time:
            self.__last_move_time += self.__move_time
            move = True

        if move and self.__can_move_side():
            self.__invaders_last_x += self.__step_x_size if self.__move_right else\
                -self.__step_x_size

        elif move and not self.__can_move_side():
            self.__invaders_last_y += self.__step_y_size
            self.__move_right = not self.__move_right

        # Display the invaders with movement
        for i in range (self.__nb_invaders_cols):
            for j in range (self.__nb_invaders_lines):

                if (self.__invaders[j,i]):
                    x = self.__invaders_last_x + i * self.__space_btw_invaders
                    y = self.__invaders_last_y + j * self.__space_btw_invaders + 3
                    screen.blit(self.__invader_img, (x,y))

        # Display the player
        player_width = 40
        self.__player.get_keyboard_input()
        player_pos_x = self.__player.pos_x
        pygame.draw.rect(screen, "green", pygame.Rect(player_pos_x,\
            self.__height - 150, player_width, player_width))

        # Display the rest of the bord style
        pygame.draw.line(screen, "green", (20, self.__height - 100),\
            (580, self.__height - 100), 2)