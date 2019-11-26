# Author: Jordan Chapman

from pygameFunctions import *
from SpriteData.Animation import Animation

NO_GRAPHIC = None


class GraphicHandler:
    def __init__(self, graphics=None, current_graphic=NO_GRAPHIC):
        """
        Object that handles images and animations for a sprite
        """
        self.graphics = graphics if graphics else {}
        self.current_graphic = current_graphic
        self.__current_image = None
        self.__rotated_image = None
        self.__flipped_image = None
        self.__angle = 0
        self.__facing = RIGHT
        self.current_angle = self.__angle
        self.current_direction = self.__facing
        self.changed_image = False
        self.ops = 0

    def get_facing(self):
        return self.__facing

    def set_facing(self, face):
        if face != self.__facing:
            self.__facing = face
    facing = property(get_facing, set_facing)

    def get_angle(self):
        return self.__angle

    def set_angle(self, angle):
        if angle != self.__angle:
            self.__angle = angle
    angle = property(get_angle, set_angle)

    def add_animation(self, name, images, delay, mode=REPEAT):
        """
        Add an animation to the graphics handler
        :param name: Identifier for new animation
        :param images: Collection of images to animate. Should be a list-like datatype
        :param delay: Frame to delay for this animation
        :param mode: Animation mode:
            REPEAT = animation repeats when finished
            STAY = animation stays at the LAST frame when finished
            REVERT = animation stays at the FIRST frame when finished
        :return: None
        """
        if name in self.graphics:
            raise NameError("Graphic already exists")
        elif name == NO_GRAPHIC:
            raise NameError("Graphic identifier cannot be 'None'")
        else:
            animation = Animation(images, delay, mode)
            self.graphics[name] = animation

    def set_current_graphic(self, name):
        if name in self.graphics:
            if self.current_graphic != NO_GRAPHIC:
                self.reset()
            self.current_graphic = name
            self.update_image()
            self.__flipped_image = self.__current_image
            self.__rotated_image = self.__flipped_image
        else:
            raise NameError("Identifier not found")

    def reset(self):
        self.graphics[self.current_graphic].reset()
        self.current_direction = RIGHT
        self.angle = 0

    def get_graphic(self):
        return self.current_graphic

    def tick(self):
        self.graphics[self.current_graphic].tick()
        self.update_image()

    def update_image(self):
        image = self.__get_orig_image()
        if image != self.__current_image:
            self.__current_image = image
            self.current_angle = 0
            self.current_direction = RIGHT
            self.changed_image = True

    def get_image(self):
        flip = self.facing != self.current_direction
        rotate = self.angle != self.current_angle
        if flip: self.ops += 1
        if rotate: self.ops += 1
        if flip and rotate:
            self.current_direction = self.facing
            self.current_angle = self.angle
            if self.facing == LEFT:
                self.__flipped_image = pygame.transform.flip(self.__current_image, 1, 0)
            else:
                self.__flipped_image = self.__current_image
            if self.angle:
                self.__rotated_image = pygame.transform.rotate(self.__flipped_image, -self.angle)
            else:
                self.__rotated_image = self.__flipped_image
        elif flip:
            self.current_direction = self.facing
            if self.facing == LEFT:
                self.__flipped_image = pygame.transform.flip(self.__current_image, 1, 0)
            else:
                self.__flipped_image = self.__current_image
            self.__rotated_image = self.__flipped_image
        elif rotate:
            self.current_angle = self.angle
            if self.angle:
                self.__rotated_image = pygame.transform.rotate(self.__flipped_image, -self.angle)
            else:
                self.__rotated_image = self.__flipped_image
        elif self.changed_image:
            self.__rotated_image = self.__current_image
        self.changed_image = False
        return self.__rotated_image

    def __get_orig_image(self):
        """
        Gets the current image from the current graphic object.
        :return: Current image for current graphic
        """
        return self.graphics[self.current_graphic].get_current_image()
