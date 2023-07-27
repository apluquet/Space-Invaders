import pygame

class Player:

    __dt = 4
    player_img = pygame.image.load("img/my_player.png")
    width = player_img.get_size()[0]
    height = player_img.get_size()[1]

    def __init__(self, pos_x, pos_y, board_width, margin):
        self.pos_x = pos_x - self.width // 2
        self.pos_y = pos_y

        self.limit_x_min = margin
        self.limit_x_max = board_width - margin - self.player_img.get_size()[0]

        self.remaining_lives = 3


    def get_keyboard_input(self):
        keys = pygame.key.get_pressed()

        # Move right
        if keys[pygame.K_RIGHT]:
            self.pos_x = min(self.limit_x_max, self.pos_x + self.__dt)
        # Move left
        if keys[pygame.K_LEFT]:
            self.pos_x = max(self.limit_x_min, self.pos_x - self.__dt)