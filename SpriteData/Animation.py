# Author: Jordan Chapman

from pygameFunctions import *


class Animation:
    def __init__(self, images, delay, mode=REPEAT):
        """
        Object that keeps track of animation frames
        :param images: Images to track
        :param delay: Number of ticks before moving to the next image
        """
        self.images = images
        self.delay = delay
        self.ticker = 0
        self.frame = 0
        self.total_images = len(self.images)
        self.mode = mode
        self.finished = False

    def tick(self):
        """
        Update the animation. Should be called each frame
        :return: None
        """
        if not self.delay:
            return
        if self.finished:
            return
        self.ticker += 1
        if self.ticker >= self.delay:
            self.ticker -= self.delay
            self.frame += 1
            if self.frame >= self.total_images:
                if self.mode == REPEAT:
                    self.frame = 0
                else:
                    self.finished = True
                    if self.mode == STAY:
                        self.frame = -1
                    if self.mode == REVERT:
                        self.frame = 0

    def get_current_image(self):
        """
        Get the current image of the animation
        :return: Image at position 'frame'
        """
        return self.images[self.frame]

    def reset(self):
        self.ticker = 0
        self.frame = 0
        self.finished = False
