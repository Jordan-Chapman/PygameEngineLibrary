# Author: Jordan Chapman

from SpriteData.CollisionBox import *
from pygameFunctions import *


class BasicSprite:
    image = load_img("../Images/col.png", transparency_color=(255, 255, 255))

    def __init__(self, x, y, image):
        self.__x = 0
        self.__y = 0
        self.__angle = 0
        self.colliders = []
        self.collisions = []
        self.image = image
        self.box = self.image.get_rect()
        self.x = x
        self.y = y
        self.p = False
        self.toggle = 0

    def set_image(self, new_image):
        if self.image != new_image:
            self.image = new_image
            self.box = new_image.get_rect()
            self.x = self.x
            self.y = self.y

    def get_x(self):
        return self.__x

    def set_x(self, new_x):
        dist = new_x - self.__x
        if dist != 0:
            for col in self.colliders:
                col.x += dist
        self.__x = new_x
        self.box[0] = int(new_x - self.box[2]/2)
    x = property(get_x, set_x)

    def get_y(self):
        return self.__y

    def set_y(self, new_y):
        dist = new_y - self.__y
        if dist != 0:
            for col in self.colliders:
                col.y += dist
        self.__y = new_y
        self.box[1] = int(new_y - self.box[3]/2)
    y = property(get_y, set_y)

    def get_top(self):
        return self.y - self.box[3]/2

    def set_top(self, new_top):
        self.y = new_top + self.box[3]/2
    top = property(get_top, set_top)

    def get_bottom(self):
        return self.y + self.box[3]/2

    def set_bottom(self, new_bottom):
        self.y = new_bottom - self.box[3]/2
    bottom = property(get_bottom, set_bottom)

    def get_left(self):
        return self.x - self.box[2]/2

    def set_left(self, new_left):
        self.x = new_left + self.box[2]/2
    left = property(get_left, set_left)

    def get_right(self):
        return self.x + self.box[2]/2

    def set_right(self, new_right):
        self.x = new_right - self.box[2]/2
    right = property(get_right, set_right)

    def add_collider(self, x, y, width, height):
        collider = CollisionBox(self, x, y, width, height)
        self.colliders.append(collider)

    def add_collision(self, obj):
        self.collisions.append(obj)

    def do_collisions(self):
        """
        Call once per frame, after collisions have been calculated
        This flushes the collisions
        :return: None
        """
        if self.collisions:
            if self.toggle % 4 < 2:
                self.image = BasicSprite.image
            else:
                self.image = pygame.Surface((0, 0))
            self.toggle += 1
        else:
            self.image = BasicSprite.image
            self.toggle = 0
        self.collisions = []

    def get_angle(self):
        return self.__angle

    def set_angle(self, angle):
        if angle != self.__angle:
            while angle < 0:
                angle += 360
            angle = angle % 360
            self.__angle = angle
    angle = property(get_angle, set_angle)

    def update(self):
        self.do_collisions()
        if self.p:
            keys = pygame.key.get_pressed()
            if keys[K_w]:
                self.y -= 1
            if keys[K_s]:
                self.y += 1
            if keys[K_a]:
                self.x -= 1
            if keys[K_d]:
                self.x += 1
