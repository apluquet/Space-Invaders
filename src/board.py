import pygame
import numpy as np

import player

# This class represents the board of Space Invaders. It manages the position of
# each element.
class Board:
    # Private class variables

    # Step size in pixels for invaders movement
    __step_x_size = 15
    __step_y_size = 30

    # Image of an invader
    __invader_img = pygame.image.load("img/my_invader.png")

    __margin_btw_invaders = 15

    # Size in pxl of the invader image
    __invader_width = __invader_img.get_size()[0]
    __invader_height = __invader_img.get_size()[1]

    __nb_invaders_cols = 11
    __nb_invaders_lines = 5

    # Margin between borders of the window and the game in pixels
    __margin = 20
    
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

        # For the invaders movement, save the last (x,y) position of the top
        # right invader
        self.__invaders_last_x = self.__margin
        self.__invaders_last_y = self.__margin

        # For the invaders movement, save if invaders movement is goind right
        # or not
        self.__move_right = True

        self.__player = player.Player(self.__width / 2, self.__width, self.__margin)

    # Private class methods
    def __is_at_right_border(self):
        # Check if at right border

        # x_pos + nb_cols * (invader_width + margin_btw_invaders) - margin_btw_invaders + width_invader
        # Remove one margin for the invader furthest to the right

        if self.__invaders_last_x + self.__nb_invaders_cols * (self.__invader_width +\
            self.__margin_btw_invaders) - self.__margin_btw_invaders + self.__step_x_size >=\
                self.__width - self.__margin:
            return True
        return False

    def __is_at_left_border(self):
        # Check if at left border

        if self.__invaders_last_x - self.__step_x_size < self.__margin:
            return True
        return False

    def __can_move_side(self):
        # Check if it can move side according to the direction and position of
        # the borders
        return (self.__move_right and not self.__is_at_right_border()) or\
            (not self.__move_right and not self.__is_at_left_border())

    def __display_invaders(self, screen, time):
        
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
                    x = self.__invaders_last_x + i * (self.__invader_width + self.__margin_btw_invaders)
                    y = self.__invaders_last_y + j * (self.__invader_height + self.__margin_btw_invaders)
                    screen.blit(self.__invader_img, (x,y))


    def __display_player(self, screen):
        self.__player.get_keyboard_input()
        player_pos_x = self.__player.pos_x

        screen.blit(self.__player.player_img, (player_pos_x, self.__height - 150))

    def __display_elements(self, screen):
        # Display the bottom line 
        pygame.draw.line(screen, "green", (self.__margin, self.__height - 100),\
            (self.__width - self.__margin, self.__height - 100), 2)


    def check_victory(self):
        # If no more invaders, player win
        if self.__invaders.sum() == 0:
            return 1
        # If invaders are too low (same level as the player), player loose
        if  self.__invaders_last_y + self.__nb_invaders_lines *\
            (self.__invader_height + self.__margin_btw_invaders) >\
                self.__height - 150:
            return -1
        else:
            return 0

    # Public class methods
    def display_board(self, screen, time):
        self.__display_invaders(screen, time)
        self.__display_player(screen)
        self.__display_elements(screen)  
