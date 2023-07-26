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
        
        # Display player lives
        img_lives = pygame.transform.rotozoom(self.__player.player_img, 0, 0.7)
        y_lives = self.__height - 60
        margin_btw_lives = 10
        live_width = img_lives.get_size()[0]
        for i in range (self.__player.remaining_lives):
            screen.blit(img_lives, (self.__margin + i * (live_width + margin_btw_lives), y_lives))


    def __endgame(self, screen, win):
        # Display window

        # Define width and height of window depending of the game screen's size
        rect_width = (self.__width / 4) * 3
        rect_height = 300

        # Get coordinates of the top left corner of the window
        x_top_left = (self.__width   - rect_width) / 2
        y_top_left = (self.__height - rect_height) / 2 - 100
        
        rect = pygame.Rect(x_top_left, y_top_left, rect_width, rect_height)

        # Display wondow and window's border
        pygame.draw.rect(screen, color="black", rect=rect)
        pygame.draw.rect(screen, color="white", rect=rect, width=4)

        # Fonts for text
        title_font = pygame.font.Font("fonts/hannover_messe_sans.otf", 60)
        text_win_font = pygame.font.Font("fonts/moder_dos_437.ttf", 40)
        text_score_font = pygame.font.Font("fonts/moder_dos_437.ttf", 30)

        # Define the texts
        text_title = title_font.render('Space Invaders', False, "white")

        if win:
            text_end = text_win_font.render('Victory', False, "green")
        else:
            text_end = text_win_font.render('Defeat', False, "red")

        text_score = text_score_font.render("Remaining invaders " + str(self.__invaders.sum()), False, "white")

        # Get width of each text in order to center them
        w_text_end = text_end.get_width()
        w_text_title = text_title.get_width()
        w_text_score = text_score.get_width()
        
        # Display the texts
        screen.blit(text_title, (self.__width // 2 - w_text_title // 2,y_top_left + 30))
        screen.blit(text_end, (self.__width // 2 - w_text_end // 2,y_top_left + 140))
        screen.blit(text_score, (self.__width // 2 - w_text_score // 2, y_top_left + 230))

    def check_victory(self, screen):
        # If no more invaders, player win
        if self.__invaders.sum() == 0:
            self.__endgame(screen, win=True)
            return False
        # If invaders are too low (same level as the player), player loose
        if  self.__invaders_last_y + self.__nb_invaders_lines *\
            (self.__invader_height + self.__margin_btw_invaders) >\
                self.__height - 150:
            self.__endgame(screen, win=False)
            return False
        return True # Continue game
    
    # Public class methods
    def display_board(self, screen, time):
        self.__display_invaders(screen, time)
        self.__display_player(screen)
        self.__display_elements(screen)
