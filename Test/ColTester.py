# Author: Jordan Chapman
# Simple class for testing the 'CollisionManager' file

from SpriteData.CollisionBox import *
from SpriteData.CollisionManager import *


class ColTester:
    def __init__(self):
        self.collisions = []
        self.colliders = []

    def add_collider(self, x, y, width, height):
        collider = CollisionBox(x, y, width, height)
        self.colliders.append(collider)

    def add_collision(self, obj):
        self.collisions.append(obj)

    def do_collisions(self):
        for obj in self.collisions:
            print("Collided with: " + obj.__str__())


os = [ColTester(), ColTester()]
os[0].add_collider(10, 10, 20, 20)
os[0].add_collider(20, 20, 20, 20)
os[1].add_collider(30, 12, 10, 10)
check_all_objects(os)
os[0].do_collisions()
os[1].do_collisions()
