import pygame


class Player:
    dt = 4

    img = pygame.image.load("img/my_player.png")
    img_exploding = pygame.image.load("img/my_exploding_player.png")

    width = img.get_size()[0]
    height = img.get_size()[1]

    def __init__(self, x, y, board_width, margin):
        # Position (in pixel) of the player (at top left)
        self.x = x - self.width // 2
        self.y = y

        # Min and max limits on x axis
        self.limit_x_min = margin
        self.limit_x_max = board_width - margin - self.img.get_size()[0]

        self.remaining_lives = 3

    def explosion(self, screen):
        self.remaining_lives -= 1

        # Get coordinates of where to display exploding image. They are not the
        # sames as self.x and self.y because the image does not have the same
        # resolution
        width, height = self.img.get_size()
        width_exploding, height_exploding = self.img_exploding.get_size()
        x = self.x - (width_exploding - width) // 2
        # Not // 2 because aligned on bottom
        y = self.y - (height_exploding - height)

        screen.blit(self.img_exploding, (x, y))

    def update_pos(self):
        keys = pygame.key.get_pressed()

        # Move right
        if keys[pygame.K_RIGHT]:
            self.x = min(self.limit_x_max, self.x + self.dt)
        # Move left
        if keys[pygame.K_LEFT]:
            self.x = max(self.limit_x_min, self.x - self.dt)
