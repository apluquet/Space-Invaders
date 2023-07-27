class Bullet:
    __dt = 2

    def __init__(self, x, y, direction, enemy_bullet):
        self.x = x
        self.y = y
        self.__direction = direction
        self.enemy_bullet = False

    def update(self, max_y_pos):
        self.x = self.x + self.__direction[0] * self.__dt
        self.y = self.y + self.__direction[1] * self.__dt

        return self.y >= max_y_pos

    def collision(self, x, y, width, height):
        if x <= self.x and self.x <= x + width:
            if y <= self.y and self.y <= y + height:
                return True
        return False
