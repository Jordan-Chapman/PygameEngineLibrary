# Author: Jordan Chapman
# Objects tested in these methods must have the following
# 'colliders' attribute - list containing 'CollisionBox' objects
# 'add_collision' method - void method that accepts an object to collide with this frame

from SpriteData.Collision import Collision


def check_all_objects(objects):
    """
    Takes a list of objects and checks collision between all of them
    :param objects: list of objects to check
    :return: None
    """
    todo = objects.copy()
    while len(todo) > 0:
        check_object(todo.pop(), todo)


def check_object(obj, objects):
    """
    Check the collision between one object and others, and adds collided objects
        using the 'add_collision' method of each
    :param obj: Object to check
    :param objects: objects to check against
    :return: None
    """
    for other in objects:  # Other is an object that has colliders
        for collider in obj.colliders:
            collisions = check_colliders(collider, other.colliders)
            if collisions:
                for col in collisions:
                    # Make a collision object and add it to the collisions
                    obj.add_collision(Collision(other, col, collider))
                    other.add_collision(Collision(obj, collider, col))


def check_colliders(col, others):
    """
    Check a single CollisionBox against a list of other CollisionBoxes
    :param col: Box to check
    :param others: list of others to check against
    :return: True if a collision is detected, False otherwise
    """
    collisions = []
    for other in others:  # Other is a collision box
        if col.check_collide(other):
            collisions.append(other)
    return collisions
