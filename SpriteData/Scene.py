# Author: Jordan Chapman

from SpriteData.CollisionBox import CollisionBox


def load_scene(file):
    scene = []
    with open(file) as data:
        for line in data.readlines():
            box = [int(x) for x in line.split()]
            scene.append(CollisionBox(None, box[0], box[1], box[2], box[3]))
    return scene


class Scene:
    def __init__(self, file):
        self.colliders = load_scene(file)
        self.collisions = []

    def add_collision(self, collision):
        self.collisions.append(collision)
