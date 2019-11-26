# Author: Jordan Chapman


class CollisionBox:
    def __init__(self, parent, x, y, width, height):
        self.__x = x
        self.__y = y
        self.parent = parent
        self.width = width
        self.height = height

    def get_x(self):
        return self.__x

    def set_x(self, new_x):
        self.__x = new_x
    x = property(get_x, set_x)

    def get_y(self):
        return self.__y

    def set_y(self, new_y):
        self.__y = new_y
    y = property(get_y, set_y)

    def get_top(self):
        return self.__y - (self.height-1)/2

    def set_top(self, new_top):
        self.y = new_top + (self.height-1)/2
    top = property(get_top, set_top)

    def get_bottom(self):
        return self.__y + (self.height-1)/2

    def set_bottom(self, new_bottom):
        self.y = new_bottom - (self.height-1)/2
    bottom = property(get_bottom, set_bottom)

    def get_left(self):
        return self.__x - (self.width-1)/2

    def set_left(self, new_left):
        self.x = new_left + (self.width-1)/2
    left = property(get_left, set_left)

    def get_right(self):
        return self.__x + (self.width-1)/2

    def set_right(self, new_right):
        self.x = new_right - (self.width-1)/2
    right = property(get_right, set_right)

    def check_collide(self, other):
        """
        Checks collision between self and another collision box
        :param other: Object of type CollisionBox
        :return: boolean didCollide
        """

        if self.left <= other.right and self.right >= other.left:
            if self.top <= other.bottom and self.bottom >= other.top:
                return True
        return False
