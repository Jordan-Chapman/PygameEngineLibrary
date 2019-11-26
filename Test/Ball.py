# Author: Jordan Chapman
from Test.BasicSprite import BasicSprite
from pygameFunctions import *


class Ball(BasicSprite):
    GRAVITY = 12
    GRAVITY_ACCELERATION = 0.5
    MOVE_SPEED = 0.2
    MAX_MOVE_SPEED = 5
    JUMP_POWER = 5
    MAX_JUMPS = 6
    AIR_TRACTION = 0.5
    TRACTION = 1
    images = load_img_map("../Images/ballman_bordered.png",
                          16, 16, border=1, scale=2,
                          transparency_color=(255, 255, 255))

    def __init__(self, x, y):
        super().__init__(x, y, Ball.images[0][0])
        self.current_img = 0
        self.fall_speed = 0
        self.jumped = False
        self.jumps = Ball.MAX_JUMPS
        self.move_speed = 0
        self.on_object = False

    def fall(self):
        self.y += self.fall_speed

    def handle_keyboard(self, can_jump, traction):
        keys = pygame.key.get_pressed()
        dist = 0
        if keys[K_w]:
            if not self.jumped and (can_jump or self.jumps > 0):
                self.fall_speed = -(Ball.JUMP_POWER + self.jumps)
                self.jumps -= 1
            self.jumped = True
        elif self.jumped:
            self.jumped = False
        if keys[K_a]:
            dist -= Ball.MOVE_SPEED * traction
        if keys[K_d]:
            dist += Ball.MOVE_SPEED * traction

        return dist

    def update(self):
        self.do_collisions()

        traction = Ball.AIR_TRACTION
        in_air = False
        if self.get_bottom() < SCREENHEIGHT and not self.on_object:
            in_air = True
        can_jump = False
        if in_air:
            if self.fall_speed < Ball.GRAVITY:
                self.fall_speed += Ball.GRAVITY_ACCELERATION
        else:
            self.fall_speed = 0
            self.set_bottom(SCREENHEIGHT)
            can_jump = True
            traction = Ball.TRACTION
            self.jumps = Ball.MAX_JUMPS
        dist = self.handle_keyboard(can_jump, traction)
        if dist:
            self.move(dist)
        self.x += self.move_speed
        self.animate()
        self.fall()

    def do_collisions(self):
        pass

    def animate(self):
        self.current_img += self.move_speed
        self.current_img = self.current_img % 80
        self.set_image(Ball.images[0][int(self.current_img//20)])

    def move(self, dist):
        if abs(self.move_speed + dist) < Ball.MAX_MOVE_SPEED:
            self.move_speed += dist
