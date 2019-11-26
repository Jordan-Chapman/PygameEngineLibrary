# Author: Jordan Chapman #

# Simple test module
# Explaining the use of the display module

from display import display, BaseObject  # 'display' here is an already instantiated display object
from pygameFunctions import *


class D(BaseObject):  # Inherit from BaseObject to work with display
    """ Most basic form of object to work with the display module """

    def __init__(self, image):
        self.image = image
        self.box = image.get_rect()  # Built in to pygame, gets the image size and position
        # 'box' looks like a list [x,y,width,height]

    def get_bottom(self):  # Only required method for an object to work with display
        """
        Get the bottom pixel y location of the objects image
        :return:
        """
        # In this case, return the 'y' of the box + the 'height' of the box
        return self.box[1] + self.box[3]


img = loadimg("../Images/dum.png")  # Load up a dummy image, method is from 'pygameFunctions.py'

obj = D(image=img)  # Make an object

display.show(obj)  # Add object to display

while True:  # Main loop
    display.sample_frame()  # Do a frame (this draws and waits a frames time
    keys = pygame.key.get_pressed()  # Get the pressed keys

    # Move the object by key. Remembering that obj.box is a list '[x,y,width,height]'
    if keys[K_w]:
        obj.box[1] -= 1
    if keys[K_s]:
        obj.box[1] += 1
    if keys[K_a]:
        obj.box[0] -= 1
    if keys[K_d]:
        obj.box[0] += 1

    # Note that you can't just change obj.box[2] and obj.box[3] to adjust image size
    # These numbers are generated from the image, and modifying them has no effect
