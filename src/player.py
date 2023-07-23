import pygame

class Player:

    __dt = 8

    def __init__(self, pos_x, board_width):
        self.pos_x = pos_x

        self.limit_x_min = 20
        self.limit_x_max = board_width - 20 - 40


    def get_keyboard_input(self):
        keys = pygame.key.get_pressed()

        # Move right
        if keys[pygame.K_RIGHT]:
            self.pos_x = min(self.limit_x_max, self.pos_x + self.__dt)
        # Move left
        if keys[pygame.K_LEFT]:
            self.pos_x = max(self.limit_x_min, self.pos_x - self.__dt)