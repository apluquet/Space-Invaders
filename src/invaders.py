import random
import pygame
import numpy as np

from bullet import Bullet

class Invaders:
    img = pygame.image.load("img/my_invader.png")
    img_exploding = pygame.image.load("img/my_exploding_invader.png")
    width = img.get_size()[0]
    height = img.get_size()[1]

    margin_x = 25
    margin_y = 10

    step_x = 5
    step_y = 30

    nb_cols = 11
    nb_lines = 5

    shoot_probability = 0.0025

    def __init__(self, x, y, board_margin, bottom_limit):
        self.invaders = np.ones((self.nb_lines, self.nb_cols), int)

        # Position (in pixel) of the top left invader of the group
        self.x = x
        self.y = y

        self.board_margin = board_margin
        self.bottom_limit = bottom_limit

        self.move_right = True

    def remaining(self):
        return self.invaders.sum()

    def too_low(self):
        y_lowest_invader = self.y + self.nb_lines * (self.height + self.margin_y)
        return y_lowest_invader > self.bottom_limit

    def is_at_right_border(self, board_width):
        max_right = board_width - self.board_margin

        # Get the position the most at right of the group if moves to right
        # If higher than the right limit of the board (max_right), then, is
        # at right border
        right_invaders = self.x + self.nb_cols * (self.width + self.margin_x)
        right_invaders += self.step_x - self.margin_x

        return right_invaders >= max_right

    def is_at_left_border(self):
        # Check if at left border
        return self.x - self.step_x < self.board_margin

    def can_move_side(self, board_width):
        # Check if it can move side according to the direction and position of
        # the borders
        return (self.move_right and not self.is_at_right_border(board_width)) or (
            not self.move_right and not self.is_at_left_border()
        )

    def move(self, board_width):
        if self.can_move_side(board_width):
            self.x += self.step_x if self.move_right else -self.step_x
        else:
            self.y += self.step_y
            self.move_right = not self.move_right

    def get_invader_pos(self, line, col):
        x = self.x + col * (self.width + self.margin_x)
        y = self.y + line * (self.height + self.margin_y)
        return (x, y)

    def shoot(self, screen):
        # Lit of new bullets
        bullets = []

        # Find for each column, the invader at the lowest spot
        for i in range(self.nb_cols):
            j = self.nb_lines - 1

            while not self.invaders[j][i] and j >= 0:
                j -= 1

            if j >= 0:
                nb = random.random()
                if nb <= self.shoot_probability:

                    # Invader explose if it shoots until the player will be able
                    # shoot too. This way, the invader's explosion could be tried
                    # and could explore the tree ways of finishing the game (no
                    # more invader, invaders reached player, player killed)
                    explode_width = self.img_exploding.get_size()[0]
                    explode_height = self.img_exploding.get_size()[1]
                    x, y = self.get_invader_pos(j, i)
                    x = x - (explode_width - self.width) // 2
                    y = y - (explode_height - self.height) // 2
                    screen.blit(self.img_exploding, (x,y))

                    self.invaders[j][i] = 0

                    x, y = self.get_invader_pos(j, i)
                    x += self.width // 2
                    y += self.height
                    new_bullet = Bullet(x, y, (0, 1), True)
                    bullets.append(new_bullet)

        return bullets
