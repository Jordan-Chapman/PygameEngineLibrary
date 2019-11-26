# Author: Jordan Chapman
# Version of glider that tests the graphics handler library

from Test.BasicSprite import BasicSprite
from SpriteData.GraphicHandler import GraphicHandler
from pygameFunctions import *

WALK = "walk"
STAND = "stand"
GLIDE = "glide"
JUMP = "jump"
HOP = "hop"
HELPLESS = "helpless"
SPIN = "spin"
TORNADO = "tornado"

HEAD_BOX = 0
FOOT_BOX = 1
LEFT_BOX = 2
RIGHT_BOX = 3

FREE_STYLE = 0  # Glide whenever, glide only cancels when landing
SMASH_STYLE = 1  # Glide only when moving forward or standing still, cancel on jump, landing, or stalling


class Glider(BasicSprite):
    GRAVITY = 12  # Terminal velocity (can fall faster when gliding downwards)
    GRAVITY_ACCELERATION = 0.5  # Gravity acceleration
    GLIDE_GRAVITY_ACCELERATION = 0.05  # Gravity acceleration while gliding
    MOVE_SPEED = 0.5  # Acceleration while running/jumping. Gets modified by traction values lower down
    MAX_MOVE_SPEED = 5  # Max velocity while running/jumping
    MAX_GLIDE_SPEED = 10  # Max velocity when gliding. Momentum over this gets saved for later
    JUMP_POWER = 12  # Jump power (straight dy modification)
    MAX_JUMPS = 6  # Maximum number of jumps.
    JUMP_FALLOFF = 1  # Jump power decrease rate per air jump. 1=1 jump power, 2=2, etc.
    AIR_TRACTION = 0.2  # Speed decrease modifier while in air
    TRACTION = 1  # Speed decrease modifier while on land
    ROTATE_SPEED = 2  # Base speed of rotation during a glide
    ROTATE_SPEED_BOOST = 4  # Max boost given when gliding fast
    GLIDE_MOD = 0.2  # Speed modifier for upwards and downwards gliding (Increase for down, decrease for up)
    GLIDE_RESPONSE = 0.5  # Response speed for directional change during a glide (1 is instant) DONT GO OVER 1
    GLIDE_CANCEL_THRESHOLD = 0  # Minimum speed threshold of when glide will auto-cancel
    GLIDE_MIN_START_SPEED = 2  # If entering a glide, it will always be at least this speed
    BOOST_MODIFIER = 1.1  # Free boost to glide per frame if gliding downward at full speed (multiplied)
    GROUND_SLOWDOWN_RATE = 0.5  # Speed of slowdown when not moving on ground
    AIR_SLOWDOWN_RATE = 0.01  # Speed of slowdown when not moving in the air
    SHUTTLE_DURATION = 24  # Duration in frames of a shuttle loop
    SHUTTLE_ROTATE_SPEED = 15  # Rotation speed during a shuttle loop
    SHUTTLE_SPEED = 5  # Flight speed during a shuttle loop
    SHUTTLE_JUMP = 2  # Height boost from shuttle loop
    images = load_img_map("../Images/metaknight.png", width=64, height=64, border=1, transparency_color=(69, 69, 69))
    jump_images = load_img_map("../Images/meta_jump.png",
                               width=80, height=60, border=1,
                               transparency_color=(69, 69, 69))
    hop_images = load_img_map("../Images/meta_hop.png",
                              width=40, height=48, border=1,
                              transparency_color=(69, 69, 69))
    spin_images = load_img_map("../Images/meta_spin.png",
                               width=48, height=65, border=0,
                               transparency_color=(69, 69, 69))
    tornado_images = load_img_map("../Images/meta_tornado.png",
                                  width=52, height=50, border=1,
                                  transparency_color=(255, 255, 255))

    def __init__(self, x, y):
        self.graphics = GraphicHandler()
        self.graphics.add_animation(name=STAND, images=Glider.images[0], delay=0)
        self.graphics.add_animation(name=WALK, images=Glider.images[1], delay=4)
        self.graphics.add_animation(name=GLIDE, images=[Glider.jump_images[0][1]], delay=0)
        self.graphics.add_animation(name=JUMP, images=Glider.jump_images[0], delay=4, mode=REVERT)
        self.graphics.add_animation(name=HOP, images=Glider.hop_images[0], delay=4, mode=STAY)
        self.graphics.add_animation(name=HELPLESS, images=[Glider.jump_images[0][0]], delay=0)
        self.graphics.add_animation(name=SPIN, images=Glider.spin_images[0], delay=1)
        self.graphics.add_animation(name=TORNADO, images=Glider.tornado_images[0], delay=1)
        self.set_graphic(STAND)

        super().__init__(x, y, self.graphics.get_image())
        self.x_radius = 14
        self.y_radius = 12
        self.add_collider(self.x, self.y-self.y_radius, 10, 1)  # TOP
        self.add_collider(self.x, self.y+self.y_radius, 10, 1)  # BOTTOM
        self.add_collider(self.x-self.x_radius, self.y, 1, 1)  # LEFT
        self.add_collider(self.x+self.x_radius, self.y, 1, 1)  # RIGHT

        self.fall_speed = 0
        self.glided = False
        self.jumped = False
        self.do_jump_animation = False
        self.do_move_animation = False
        self.jumps = Glider.MAX_JUMPS
        self.move_speed = 0
        self.vertical_speed = 0
        self.gliding = False
        self.on_object = False
        self.momentum = 0
        self.conserved_momentum = 0
        self.facing = RIGHT
        self.glide_style = SMASH_STYLE
        self.frozen = False
        self.shuttle = 0

    def set_graphic(self, graphic):
        if graphic != self.graphics.get_graphic():
            self.graphics.set_current_graphic(graphic)

    def handle_default_movement(self):
        keys = pygame.key.get_pressed()
        dist = 0
        if self.on_object:
            traction = Glider.TRACTION
        else:
            traction = Glider.AIR_TRACTION

        if keys[K_a]:
            dist -= Glider.MOVE_SPEED * traction
        if keys[K_d]:
            dist += Glider.MOVE_SPEED * traction

        if keys[K_w]:
            if not self.jumped and (self.on_object or self.jumps > 0):
                power = Glider.JUMP_POWER - (Glider.MAX_JUMPS-self.jumps) * Glider.JUMP_FALLOFF
                self.fall_speed = -power
                self.jumps -= 1
                self.do_jump_animation = True
            self.jumped = True
        elif self.jumped:
            self.jumped = False

        if keys[K_SPACE]:
            if not self.glided:
                self.glide()
            self.glided = True
        elif self.glided:
            self.glided = False

        if keys[K_r]:
            self.move_speed = Glider.MAX_GLIDE_SPEED/2 * self.facing
            self.glide()
            self.shuttle = Glider.SHUTTLE_DURATION
            self.vertical_speed -= Glider.SHUTTLE_JUMP

        if dist > 0:
            self.facing = RIGHT
            self.graphics.facing = RIGHT
        elif dist < 0:
            self.facing = LEFT
            self.graphics.facing = LEFT

        if keys[K_RSHIFT]:
            self.frozen = True
        else:
            self.frozen = False

        return dist

    def handle_glide_movement(self):
        keys = pygame.key.get_pressed()
        angle = 0
        if keys[K_a]:
            angle -= self.get_rotate_speed()
        if keys[K_d]:
            angle += self.get_rotate_speed()
        if angle:
            self.angle += angle

        if keys[K_w] and self.glide_style == SMASH_STYLE:
            self.cancel_glide()

        if keys[K_RSHIFT]:
            self.frozen = True
        else:
            self.frozen = False

    def update_logic(self):
        self.do_collisions()
        self.do_jump_animation = False
        self.do_move_animation = False

        # Check if landed, check if can jump, cancel glide if landed
        if not self.on_object:  # In air
            if self.fall_speed < Glider.GRAVITY:
                if self.gliding:
                    self.fall_speed += Glider.GLIDE_GRAVITY_ACCELERATION
                else:
                    self.fall_speed += Glider.GRAVITY_ACCELERATION
            if self.jumped and self.fall_speed >= 0:
                self.jumped = False
        else:  # Landed
            self.fall_speed = 0
            self.jumps = Glider.MAX_JUMPS
            if self.gliding:
                self.cancel_glide()

        # Do movement based on current status
        if self.gliding:
            if self.shuttle > 0:
                self.shuttle -= 1
                self.angle -= Glider.SHUTTLE_ROTATE_SPEED * self.facing
            else:
                self.handle_glide_movement()
            self.do_glide_physics()

        else:
            dist = self.handle_default_movement()
            slowdown = self.get_slowdown_rate()
            if dist:
                self.move(dist)
                self.do_move_animation = True
            elif abs(self.move_speed) > slowdown:
                self.move_speed -= (self.move_speed/abs(self.move_speed)) * slowdown
            else:
                self.move_speed = 0
        if not self.frozen:
            mod = (1 + self.shuttle/Glider.SHUTTLE_DURATION * Glider.SHUTTLE_SPEED) if self.gliding else 1
            self.x += self.move_speed * mod
            self.y += self.fall_speed
            self.y += self.vertical_speed * mod
        self.wrap()

    def update_graphics(self):
        """
        Tick graphics, set correct graphic for current operation
        :return: None
        """

        if self.gliding:
            self.set_graphic(GLIDE)
        elif self.fall_speed < 0:
            self.set_graphic(JUMP)
            if self.do_jump_animation:
                self.graphics.reset()
        elif not self.on_object:
            pass
            #self.set_graphic(HELPLESS)
        elif self.do_move_animation:
            self.set_graphic(WALK)
        else:
            self.set_graphic(STAND)
        self.graphics.angle = self.angle
        self.graphics.facing = self.facing
        self.set_image(self.graphics.get_image())
        self.graphics.tick()

    def do_glide_physics(self):
        self.fall_speed *= 0.95

        angle = self.angle
        if self.facing == LEFT:
            angle = 360 - angle

        # Angle restriction
        if not self.shuttle:
            if 180 <= angle <= 270:
                self.angle += self.get_rotate_speed() * self.facing
                angle += self.get_rotate_speed()
            if 90 <= angle <= 180:
                self.angle -= self.get_rotate_speed() * self.facing
                angle -= self.get_rotate_speed()

            # Angle to speed modifier calculation
            angle = (angle + 180) % 360 - 180
            if angle > 90:
                angle = 180 - angle
            if angle < -90:
                angle = -180 - angle
            mod = angle / 90
            self.momentum += Glider.GLIDE_MOD * mod * self.facing
            speed = self.momentum * self.facing - Glider.MAX_GLIDE_SPEED

            # Momentum conservation
            if speed > 0:
                self.momentum -= speed * self.facing
                self.conserved_momentum += speed * Glider.BOOST_MODIFIER
            elif self.conserved_momentum > 0:
                self.conserved_momentum += speed
                self.momentum -= speed * self.facing

        if self.gliding:
            y, x = get_increase(-self.momentum, -self.angle)
            self.move_speed -= (self.move_speed - x) * Glider.GLIDE_RESPONSE
            self.vertical_speed -= (self.vertical_speed - y) * Glider.GLIDE_RESPONSE

        # Cancel check
        dist = Glider.GLIDE_CANCEL_THRESHOLD - self.momentum * self.facing
        if dist > 0 and self.glide_style == SMASH_STYLE:
            self.cancel_glide()

    def get_slowdown_rate(self):
        """
        Get the speed at which the object slows down when not moving
        :return: Slowdown speed
        """
        if self.on_object:
            return Glider.GROUND_SLOWDOWN_RATE
        else:
            return Glider.AIR_SLOWDOWN_RATE

    def do_collisions(self):
        self.on_object = False
        for collision in self.collisions:
            if collision.box == self.colliders[HEAD_BOX]:
                dist = self.colliders[HEAD_BOX].top - collision.other_box.bottom
                self.y -= dist
            if collision.box == self.colliders[FOOT_BOX]:
                if self.y < collision.other_box.y:
                    dist = self.colliders[FOOT_BOX].bottom - collision.other_box.top
                    self.y -= dist
                    self.on_object = True
            if collision.box == self.colliders[LEFT_BOX]:
                self.x = collision.other_box.right + self.x_radius
                self.stop(LEFT)
            if collision.box == self.colliders[RIGHT_BOX]:
                self.x = collision.other_box.left - self.x_radius
                self.stop(RIGHT)
        self.collisions = []

    def move(self, dist):
        if abs(self.move_speed + dist) < Glider.MAX_MOVE_SPEED or abs(self.move_speed + dist) < abs(self.move_speed):
            self.move_speed += dist

    def glide(self):
        if self.glide_style == SMASH_STYLE:
            if self.move_speed * self.facing >= 0:
                self.momentum = max(self.move_speed*self.facing, Glider.GLIDE_MIN_START_SPEED) * self.facing
                self.gliding = True
        elif self.glide_style == FREE_STYLE:
            self.momentum = self.move_speed
            self.gliding = True

    def cancel_glide(self):
        self.gliding = False
        self.angle = 0
        self.momentum = 0
        self.conserved_momentum = 0
        self.vertical_speed = 0

    def stop(self, direction):
        if self.move_speed * direction > 0:
            self.move_speed = 0

    def wrap(self):
        if self.x > SCREENWIDTH + 10:
            self.x = -10
        if self.x < -10:
            self.x = SCREENWIDTH + 10
        # if self.y > SCREENHEIGHT + 10:
        #     self.y = -10
        # if self.y < -10:
        #     self.y = SCREENHEIGHT + 10

    def get_rotate_speed(self):
        return (abs(self.momentum)/Glider.MAX_GLIDE_SPEED) * Glider.ROTATE_SPEED_BOOST + Glider.ROTATE_SPEED
