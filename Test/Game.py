# Author: Jordan Chapman

from display import *
from Test.Ball import *
from Test.Glider2 import *
from SpriteData.CollisionManager import *
from SpriteData.Text import Text
from SpriteData.CollisionBox import *
from SpriteData.Scene import Scene

s = Scene("scene.txt")
objs = []
for i in range(1):
    b = Glider(32*i, 32)
    display.show(b, layer=ENTITY_LAYER)
    objs.append(b)
b = objs[0]

bg = BasicSprite(SCREENWIDTH/2, SCREENHEIGHT/2, load_img("../Images/Background.png"))
display.show(bg, layer=BACKGROUND_LAYER)

t = Text("", 40, 10, 30, (255, 255, 255))
display.show(t, layer=OVER_LAYER)
display.canvas.set_alpha(None)
while display.running:
    x, y = b.x, b.y
    for obj in objs:
        obj.update_logic()
        obj.update_graphics()
    t.set_text(str(display.show_frame))
    check_all_objects(objs+[s])
    #display.lines.append([(x, y), (b.x, b.y)])
    display.sample_frame()
    s.collisions = []
