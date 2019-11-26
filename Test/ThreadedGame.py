# Author: Jordan Chapman

import threading
from display import *
from Test.Ball import *
from Test.Glider2 import *
from SpriteData.CollisionManager import *
from SpriteData.Text import Text
from SpriteData.CollisionBox import *
from SpriteData.Scene import Scene


class Drawer(threading.Thread):
    def __init__(self, objs):
        super().__init__()
        self.objs = objs
        self.can_draw = 0
        self.running = True

    def run(self):
        while self.running:
            if self.can_draw:
                self.can_draw -= 1
                for obj in self.objs:
                    obj.update_graphics()


class Thinker(threading.Thread):
    def __init__(self, objs):
        super().__init__()
        self.objs = objs
        self.can_think = 0
        self.running = True

    def run(self):
        while self.running:
            if self.can_think:
                self.can_think -= 1
                for obj in self.objs:
                    obj.update_logic()


s = Scene("scene.txt")
objs = []
for i in range(40):
    b = Glider(32*i, 32)
    display.show(b, layer=ENTITY_LAYER)
    objs.append(b)

bg = BasicSprite(SCREENWIDTH/2, SCREENHEIGHT/2, load_img("../Images/Background.png"))
display.show(bg, layer=BACKGROUND_LAYER)

t = Text("", 150, 10, 30, (255, 255, 255))
display.show(t, layer=OVER_LAYER)
dr = Drawer(objs)
tr = Thinker(objs)
dr.start()
tr.start()
while display.running:
    t.set_text("FPS: " + str(display.show_frame) +
               " Video Lag: " + str(dr.can_draw) +
               " Think Lag: " + str(tr.can_think))
    check_all_objects(objs+[s])
    display.sample_frame()
    s.collisions = []
    dr.can_draw += 1
    tr.can_think += 1
dr.running = False
tr.running = False
