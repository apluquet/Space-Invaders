import pygame

from player import Player
from invaders import Invaders


# This class represents the game of Space Invaders. It manages the position of
# each element and saves all object of the game.
class Game:
    # Margin between borders of the window and the game in pixels
    margin = 20

    # Class initialization
    def __init__(self, width, height):
        # Screen width and height in pixels
        self.width = width
        self.height = height
        self.bottom_screen_game = self.height - 100

        # Time in ms between invaders move
        self.move_time = 100
        # Last time a move was made
        self.last_move_time = 0

        self.invaders = Invaders(
            self.margin, self.margin, self.margin, self.height - 150
        )
        self.player = Player(self.width / 2, self.height - 150, self.width, self.margin)
        self.bullets = []

    def display_invaders(self, screen):
        for i in range(self.invaders.nb_cols):
            for j in range(self.invaders.nb_lines):
                if self.invaders.invaders[j, i]:
                    x = self.invaders.x + i * (
                        self.invaders.width + self.invaders.margin_x
                    )
                    y = self.invaders.y + j * (
                        self.invaders.height + self.invaders.margin_y
                    )
                    screen.blit(self.invaders.img, (x, y))

    def display_player(self, screen):
        self.player.update_pos()
        screen.blit(self.player.img, (self.player.x, self.player.y))

    def display_elements(self, screen):
        # Display the bottom line
        pygame.draw.line(
            screen,
            "green",
            (self.margin, self.bottom_screen_game),
            (self.width - self.margin, self.bottom_screen_game),
            2,
        )

        # Display player lives
        img_lives = pygame.transform.rotozoom(self.player.img, 0, 0.7)
        y_lives = self.height - 60
        margin_btw_lives = 10
        live_width = img_lives.get_size()[0]
        for i in range(self.player.remaining_lives):
            screen.blit(
                img_lives,
                (self.margin + i * (live_width + margin_btw_lives), y_lives),
            )

        # Display remaining invaders
        text_font = pygame.font.Font("fonts/moder_dos_437.ttf", 20)
        text_remaining_invaders = text_font.render(
            "Remaining invaders " + str(self.invaders.remaining()), False, "white"
        )
        screen.blit(text_remaining_invaders, (self.width - 350, self.height - 60))

        # Display bullets
        bullet_height = 6
        bullet_width = 2
        for i, bullet in enumerate(self.bullets):
            remove_bullet = bullet.update(self.bottom_screen_game - bullet_height)
            if (
                self.player.x <= bullet.x
                and bullet.x <= self.player.x + self.player.width
            ):
                if (
                    self.player.y + self.player.height // 2 <= bullet.y
                    and bullet.y <= self.player.y + self.player.height
                ):
                    # Bullet touches player
                    remove_bullet = True
                    self.player.remaining_lives -= 1

            if remove_bullet:
                del self.bullets[i]
            rect = pygame.Rect(bullet.x, bullet.y, bullet_width, bullet_height)
            pygame.draw.rect(screen, color="white", rect=rect)

    def endgame(self, screen, win):
        # Update screen a last time to display correct remaining lives and invaders
        screen.fill("black")
        self.display_board(screen)

        # Display window

        # Define width and height of window depending of the game screen's size
        rect_width = (self.width / 4) * 3
        rect_height = 300

        # Get coordinates of the top left corner of the window
        x_top_left = (self.width - rect_width) / 2
        y_top_left = (self.height - rect_height) / 2 - 100

        rect = pygame.Rect(x_top_left, y_top_left, rect_width, rect_height)

        # Display window and window's border
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
            "Remaining invaders " + str(self.invaders.remaining()), False, "white"
        )

        # Get width of each text in order to center them
        w_text_end = text_end.get_width()
        w_text_title = text_title.get_width()
        w_text_score = text_score.get_width()

        # Display the texts
        screen.blit(text_title, (self.width // 2 - w_text_title // 2, y_top_left + 30))
        screen.blit(text_end, (self.width // 2 - w_text_end // 2, y_top_left + 140))
        screen.blit(text_score, (self.width // 2 - w_text_score // 2, y_top_left + 230))

    def check_victory(self, screen):
        # If no more invaders, player win
        if self.invaders.remaining() == 0:
            self.endgame(screen, win=True)
            return False

        # If invaders are too low (same level as the player), player loses
        if self.invaders.too_low():
            self.endgame(screen, win=False)
            return False

        # If player has no more lives, player loses
        if self.player.remaining_lives == 0:
            self.endgame(screen, win=False)
            return False

        return True  # Continue game

    def display_board(self, screen):
        self.display_invaders(screen)
        self.display_elements(screen)
        self.display_player(screen)

    def play(self, screen, time):
        # Update invaders' position
        if time - self.last_move_time > self.move_time:
            self.last_move_time += self.move_time
            self.invaders.move(self.width)

        self.bullets += self.invaders.shoot(screen)
        self.display_board(screen)
        game_continues = self.check_victory(screen)

        return game_continues
