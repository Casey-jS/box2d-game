from game_object import GameObject
from Box2D import b2Vec2
import pygame as pg
from scene import Message
import sys


pixels_to_meters = 1/100
meters_to_pixels = 100

MAX_HEIGHT = 628 - (200 * 100)

PLAYER_SIZE = 50 # Player will be .5m X .5m

class Player(GameObject):

    def __init__(self, world, game, scene = None):
        super().__init__(x=0, y=200, world=world, image="assets/player-right.png", width=PLAYER_SIZE, height=PLAYER_SIZE, type = "dynamic")
        self.ground_speed = .1
        self.air_speed = .4
        self.current_speed = self.air_speed
        self.jump_force = -2
        self.velocity = b2Vec2(0, 0)
        self.on_surface = False
        self.current_platform = None
        self.scene = scene
        self.time_on_platform = 0
        self.game = game
        self.max_height = 10

    def collision_occurred(self, platform):
        player_right = self.rect.right
        player_left = self.rect.left
        player_bottom = self.rect.bottom
        
        platform_right = platform.rect.right
        platform_left = platform.rect.left
        platform_bottom = platform.rect.bottom
        
        # TODO: Modify these values for more precise collision
        if player_bottom > platform_bottom:
            return
        
        # if the player is within the x bounds of the platform
        if player_right < platform_right and player_left > platform_left:
            self.current_platform = platform
            self.y = platform.rect.top - 1 # -1 so the player doesnt continuously collide
            self.velocity.y = 0
            self.on_ground()

    def check_platform_collisions(self):
        for platform in self.scene.objects:
            if pg.sprite.collide_rect(self, platform) and self.velocity.y > 0:
                self.collision_occurred(platform)
    
    # updates velocity, checks collisions, handles inputs
    # updates rect and body positions
    def update(self, events):

        if self.y > self.scene.screen_bottom:
            self.game.set_score(self.max_height)
            self.scene.engine.set_running(False)

        if self.y < MAX_HEIGHT:
            self.game.set_score(self.max_height)
            self.scene.engine.set_running(False)
            self.game.win = True

        self.velocity = self.body.linearVelocity

        self.check_platform_collisions()
        self.check_wall_collisions()
        if self.current_platform:
            self.time_on_platform += 1
            self.check_fall()
        self.handle_inputs(events)

        # apply velocity to body
        self.body.linearVelocity = self.velocity

        self.x, self.y = self.body.position * meters_to_pixels
        self.rect.x, self.rect.y = self.x, self.y

        if self.velocity.y < 0:
            self.max_height = int(abs(self.rect.y / 10))
        
        self.scene.text.update("Score: " + str(self.max_height))
        
    def check_fall(self):
        player_right = self.rect.right
        player_left = self.rect.left
        
        platform_right = self.current_platform.rect.right
        platform_left = self.current_platform.rect.left

        if player_left > platform_right or player_right < platform_left:
            self.on_surface = False
            self.current_platform = None
            self.body.gravityScale = 1.0

    def on_ground(self):
        self.on_surface = True
        self.body.gravityScale = 0.0
        self.current_speed = self.ground_speed

    def handle_inputs(self, events):

        # update velocity based on keys pressed
        if events[pg.K_a]:
            self.velocity -= b2Vec2(self.current_speed, 0)
        if events[pg.K_d]:
            self.velocity += b2Vec2(self.current_speed, 0)

        # only allow jumping when on a platform
        if events[pg.K_SPACE] and self.on_surface:
            if 0 < self.time_on_platform < 10:
                self.nice_jump()
            else:
                self.jump_force = -2.5
            self.time_on_platform = 0
            self.on_surface = False
            self.current_speed = self.air_speed
            self.body.ApplyLinearImpulse(b2Vec2(0, self.jump_force), self.body.position, True)
            self.current_platform = None
            self.body.gravityScale = 1.0

    def nice_jump(self):
        msg = Message("assets/nice.png", 550, 10, 100, 270, 30)
        self.scene.message = msg
        self.jump_force += -.15 # increase the jump force for combo'd good timing jumps

    def check_wall_collisions(self):

        #if the player is on the bottom of the screen
        if self.y > self.scene.engine.height - PLAYER_SIZE:
            self.on_ground()
            self.y = self.scene.engine.height - PLAYER_SIZE - 1 # - 1 so the player doesn't continue to collide with the ground
            self.body.position = (self.x * pixels_to_meters, self.y * pixels_to_meters)
            self.velocity.y = 0

        if self.x < 0:
            self.velocity.x = abs(self.velocity.x)  # reverse x velocity
        elif self.x > self.scene.engine.width - PLAYER_SIZE:
            self.velocity.x = -abs(self.velocity.x)
