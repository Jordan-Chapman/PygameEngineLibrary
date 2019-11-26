# Author: Jordan Chapman
from Test.BasicSprite import BasicSprite
from pygameFunctions import *

LEFT = -1
RIGHT = 1


class Glider(BasicSprite):
    GRAVITY = 12
    GRAVITY_ACCELERATION = 0.5
    MOVE_SPEED = 0.5
    MAX_MOVE_SPEED = 5
    MAX_GLIDE_SPEED = 10
    JUMP_POWER = 6
    MAX_JUMPS = 6
    AIR_TRACTION = 0.2
    TRACTION = 1
    ROTATE_SPEED = 4
    GLIDE_MOD = 0.2
    GLIDE_RESPONSE = 0.1
    GLIDE_CANCEL_THRESHOLD = 1
    GROUND_SLOWDOWN_RATE = 0.5  # Speed of slowdown when not moving on ground
    AIR_SLOWDOWN_RATE = 0.01  # Speed of slowdown when not moving in the air
    base_image = load_img("../Images/meta.png", transparency_color=(255, 255, 255))
    image = base_image

    def __init__(self, x, y):
        super().__init__(x, y, Glider.base_image)
        self.fall_speed = 0
        self.jumped = False
        self.jumps = Glider.MAX_JUMPS
        self.move_speed = 0
        self.vertical_speed = 0
        self.gliding = False
        self.on_object = False
        self.angle = 0
        self.momentum = 0
        self.conserved_momentum = 0
        self.facing = LEFT

    def handle_default_movement(self, can_jump, traction):
        keys = pygame.key.get_pressed()
        dist = 0
        if keys[K_w]:
            if not self.jumped and (can_jump or self.jumps > 0):
                self.fall_speed = -(Glider.JUMP_POWER + self.jumps)
                self.jumps -= 1
            self.jumped = True
        elif self.jumped:
            self.jumped = False
        if keys[K_a]:
            dist -= Glider.MOVE_SPEED * traction
        if keys[K_d]:
            dist += Glider.MOVE_SPEED * traction
        if keys[K_SPACE]:
            self.gliding = True
            self.momentum = self.move_speed

        if dist > 0:
            self.facing = RIGHT
        elif dist < 0:
            self.facing = LEFT

        return dist

    def handle_glide_movement(self):
        keys = pygame.key.get_pressed()
        angle = 0
        if keys[K_a]:
            angle -= Glider.ROTATE_SPEED
        if keys[K_d]:
            angle += Glider.ROTATE_SPEED

        if angle:
            self.angle += angle
            while self.angle < 0:
                self.angle += 360
            self.angle = self.angle % 360

    def rotate(self, angle):
        self.set_image(pygame.transform.rotate(self.base_image, -angle))

    def update(self):
        self.do_collisions()

        traction = Glider.TRACTION
        slowdown = Glider.GROUND_SLOWDOWN_RATE
        can_jump = False
        if self.get_bottom() < SCREENHEIGHT and not self.on_object:
            traction = Glider.AIR_TRACTION
            slowdown = Glider.AIR_SLOWDOWN_RATE
            if self.fall_speed < Glider.GRAVITY:
                self.fall_speed += Glider.GRAVITY_ACCELERATION
        else:
            self.fall_speed = 0
            self.set_bottom(SCREENHEIGHT)
            can_jump = True
            self.jumps = Glider.MAX_JUMPS
            self.cancel_glide()

        if not self.gliding:
            dist = self.handle_default_movement(can_jump, traction)
            if dist:
                self.move(dist)
            elif abs(self.move_speed) > slowdown:
                self.move_speed -= (self.move_speed/abs(self.move_speed)) * slowdown
            else:
                self.move_speed = 0
        else:
            self.fall_speed *= 0.80
            self.handle_glide_movement()

            angle = self.angle
            if self.facing == LEFT:
                angle = 360 - angle

            if 180 <= angle <= 270:
                self.angle += Glider.ROTATE_SPEED * self.facing
                angle += Glider.ROTATE_SPEED
            if 90 <= angle <= 180:
                self.angle -= Glider.ROTATE_SPEED * self.facing
                angle -= Glider.ROTATE_SPEED

            mod = ((angle + 90) % 360 - 90) / 90
            self.momentum += Glider.GLIDE_MOD * mod * self.facing
            speed = abs(self.momentum) - Glider.MAX_GLIDE_SPEED
            if speed > 0:
                self.momentum -= speed * self.facing
                self.conserved_momentum += speed
            elif self.conserved_momentum > 0:
                self.conserved_momentum += speed
                self.momentum -= speed * self.facing
            dist = Glider.GLIDE_CANCEL_THRESHOLD - abs(self.momentum)
            if dist > 0:
                self.cancel_glide()
            if self.gliding:
                y, x = get_increase(-self.momentum, -self.angle)
                self.move_speed -= (self.move_speed - x) * Glider.GLIDE_RESPONSE
                self.vertical_speed -= (self.vertical_speed - y) * Glider.GLIDE_RESPONSE

        self.x += self.move_speed
        self.y += self.fall_speed
        self.y += self.vertical_speed
        # self.wrap()
        self.rotate(self.angle)

    def do_collisions(self):
        pass

    def move(self, dist):
        if abs(self.move_speed + dist) < Glider.MAX_MOVE_SPEED:
            self.move_speed += dist

    def glide(self, dist):
        pass

    def cancel_glide(self):
        self.gliding = False
        self.angle = 0
        self.rotate(0)
        self.momentum = 0
        self.conserved_momentum = 0
        self.vertical_speed = 0

    def wrap(self):
        if self.x > SCREENWIDTH:
            self.x -= SCREENWIDTH
        if self.x < 0:
            self.x += SCREENWIDTH
        if self.y > SCREENHEIGHT:
            self.y -= SCREENHEIGHT
        if self.y < 0:
            self.y += SCREENHEIGHT
