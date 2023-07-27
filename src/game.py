import pygame
import numpy as np

from bullet import Bullet
from player import Player
from invaders import Invaders


# This class represents the game of Space Invaders. It manages the position of
# each element and saves all object of the game.
class Game:
    # Private class variables

    # Margin between borders of the window and the game in pixels
    __margin = 20

    # Class initialization
    def __init__(self, width, height):
        # Screen width and height in pixels
        self.__width = width
        self.__height = height

        # Time in ms between invaders move
        self.__move_time = 100
        # Last time a move was made
        self.__last_move_time = 0

        self.__invaders = Invaders(
            self.__margin, self.__margin, self.__margin, self.__height - 150
        )

        self.__player = Player(
            self.__width / 2, self.__height - 150, self.__width, self.__margin
        )

        self.__bullets = []
        self.__bottom_screen_game = self.__height - 100

    # Private class methods

    def __display_invaders(self, screen, time):
        # Set move to True if enough elapsed time since last movement
        if time - self.__last_move_time > self.__move_time:
            self.__last_move_time += self.__move_time
            self.__invaders.move(self.__width)

        # Display the invaders with movement
        for i in range(self.__invaders.nb_cols):
            for j in range(self.__invaders.nb_lines):
                if self.__invaders.invaders[j, i]:
                    x = self.__invaders.x + i * (
                        self.__invaders.width + self.__invaders.margin_x
                    )
                    y = self.__invaders.y + j * (
                        self.__invaders.height + self.__invaders.margin_y
                    )
                    screen.blit(self.__invaders.img, (x, y))

    def __display_player(self, screen):
        self.__player.get_keyboard_input()
        player_pos_x = self.__player.pos_x
        player_pos_y = self.__player.pos_y

        screen.blit(self.__player.player_img, (player_pos_x, player_pos_y))

    def __display_elements(self, screen):
        # Display the bottom line
        pygame.draw.line(
            screen,
            "green",
            (self.__margin, self.__bottom_screen_game),
            (self.__width - self.__margin, self.__bottom_screen_game),
            2,
        )

        # Display player lives
        img_lives = pygame.transform.rotozoom(self.__player.player_img, 0, 0.7)
        y_lives = self.__height - 60
        margin_btw_lives = 10
        live_width = img_lives.get_size()[0]
        for i in range(self.__player.remaining_lives):
            screen.blit(
                img_lives,
                (self.__margin + i * (live_width + margin_btw_lives), y_lives),
            )

        # Display remaining invaders
        text_font = pygame.font.Font("fonts/moder_dos_437.ttf", 20)
        text_remaining_invaders = text_font.render(
            "Remaining invaders " + str(self.__invaders.remaining()), False, "white"
        )
        screen.blit(text_remaining_invaders, (self.__width - 350, self.__height - 60))

        # Display bullets
        bullet_height = 6
        bullet_width = 2
        for i, bullet in enumerate(self.__bullets):
            remove_bullet = bullet.update(self.__bottom_screen_game - bullet_height)
            if (
                self.__player.pos_x <= bullet.x
                and bullet.x <= self.__player.pos_x + self.__player.width
            ):
                if (
                    self.__player.pos_y + self.__player.height // 2 <= bullet.y
                    and bullet.y <= self.__player.pos_y + self.__player.height
                ):
                    # Bullet touches player
                    remove_bullet = True
                    self.__player.remaining_lives -= 1

            if remove_bullet:
                del self.__bullets[i]
            rect = pygame.Rect(bullet.x, bullet.y, bullet_width, bullet_height)
            pygame.draw.rect(screen, color="white", rect=rect)

    def __endgame(self, screen, win):
        # Display window

        # Define width and height of window depending of the game screen's size
        rect_width = (self.__width / 4) * 3
        rect_height = 300

        # Get coordinates of the top left corner of the window
        x_top_left = (self.__width - rect_width) / 2
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
        text_title = title_font.render("Space Invaders", False, "white")

        if win:
            text_end = text_win_font.render("Victory", False, "green")
        else:
            text_end = text_win_font.render("Defeat", False, "red")

        text_score = text_score_font.render(
            "Remaining invaders " + str(self.__invaders.remaining()), False, "white"
        )

        # Get width of each text in order to center them
        w_text_end = text_end.get_width()
        w_text_title = text_title.get_width()
        w_text_score = text_score.get_width()

        # Display the texts
        screen.blit(
            text_title, (self.__width // 2 - w_text_title // 2, y_top_left + 30)
        )
        screen.blit(text_end, (self.__width // 2 - w_text_end // 2, y_top_left + 140))
        screen.blit(
            text_score, (self.__width // 2 - w_text_score // 2, y_top_left + 230)
        )

    def __invaders_shoot(self, screen):
        self.__bullets += self.__invaders.shoot()

    def __check_victory(self, screen):
        # If no more invaders, player win
        if self.__invaders.remaining() == 0:
            self.__endgame(screen, win=True)
            return False

        # If invaders are too low (same level as the player), player loses
        if self.__invaders.too_low():
            self.__endgame(screen, win=False)
            return False

        # If player has no more lives, player loses
        if self.__player.remaining_lives == 0:
            self.__endgame(screen, win=False)
            return False

        return True  # Continue game

    def __display_board(self, screen, time):
        self.__display_invaders(screen, time)
        self.__display_player(screen)
        self.__display_elements(screen)

    # Public class methods
    def play(self, screen, time):
        game_continues = self.__check_victory(screen)

        self.__display_board(screen, time)
        self.__invaders_shoot(screen)

        return game_continues
