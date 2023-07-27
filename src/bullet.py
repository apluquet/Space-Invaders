class Bullet:
    # Bullet move speed
    speed = 2

    # Size of bullet for display
    width = 2
    height = 6

    def __init__(self, x, y, direction, enemy_bullet):
        self.x = x
        self.y = y
        self.direction = direction
        self.enemy_bullet = enemy_bullet

    def update(self, max_y_pos):
        self.x = self.x + self.direction[0] * self.speed
        self.y = self.y + self.direction[1] * self.speed

        return self.y >= max_y_pos

    def collide(self, x, y, width, height):
        if x <= self.x and self.x <= x + width:
            if y <= self.y and self.y <= y + height:
                return True
        return False
