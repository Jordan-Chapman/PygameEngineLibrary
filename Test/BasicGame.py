# Author: Jordan Chapman

from display import *
from Test.BasicSprite import *
from SpriteData.CollisionManager import *

p = BasicSprite(10, 10)
e = BasicSprite(100, 100)
p.add_collider(p.x, p.y, 16, 16)
p.add_collider(p.x-16, p.y, 16, 16)
p.add_collider(p.x+16, p.y, 16, 16)
p.add_collider(p.x, p.y-16, 16, 16)
p.add_collider(p.x, p.y+16, 16, 16)
e.add_collider(e.x, e.y, 16, 16)
e.add_collider(e.x-16, e.y, 16, 16)
e.add_collider(e.x+16, e.y, 16, 16)
e.add_collider(e.x, e.y-16, 16, 16)
e.add_collider(e.x, e.y+16, 16, 16)
p.p = True
display.show(p)
display.show(e)
while display.running:
    p.update()
    e.update()
    check_all_objects([p, e])
    display.sample_frame()
