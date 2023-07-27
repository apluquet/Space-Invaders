import pygame


class Player:
    __dt = 4
    player_img = pygame.image.load("img/my_player.png")
    width = player_img.get_size()[0]
    height = player_img.get_size()[1]

    def __init__(self, x, y, board_width, margin):
        # Position (in pixel) of the player (at top left)
        self.x = x - self.width // 2
        self.y = y

        # Min and max limits on x axis
        self.limit_x_min = margin
        self.limit_x_max = board_width - margin - self.player_img.get_size()[0]

        self.remaining_lives = 3

    def update_pos(self):
        keys = pygame.key.get_pressed()

        # Move right
        if keys[pygame.K_RIGHT]:
            self.x = min(self.limit_x_max, self.x + self.__dt)
        # Move left
        if keys[pygame.K_LEFT]:
            self.x = max(self.limit_x_min, self.x - self.__dt)
