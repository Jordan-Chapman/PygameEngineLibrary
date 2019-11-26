# Author: Jordan Chapman
# Collision objects get created when the collision manager detects a collision
# These objects contain data about the collision that happened


class Collision:
    def __init__(self, other_object, other_box, box):
        self.other_object = other_object
        self.other_box = other_box
        self.box = box
