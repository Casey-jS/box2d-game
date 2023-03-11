import os
import pygame as pg
import sys
import Box2D
from abc import abstractmethod
import random




FPS = 120

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"


class Engine:

    def __init__(self, title, width=1024, height=768):
        self.title = title
        self.width = width
        self.height = height
        self.delta = 0
        self.world = Box2D.b2World(gravity=(0, 30), doSleep=False)
        self.scene = None
        self.events = None
        self.pg_init()

    def pg_init(self):
        pg.init()
        self.screen = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption(self.title)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500)

    def set_scene(self, scene):
        self.scene = scene


    def run(self):

        time_step = 1 / FPS
        accumulated_time = 0
        self.running = True
        while self.running:

            self.delta = self.clock.tick(FPS) / 1000.0
            accumulated_time += self.delta

            while accumulated_time >= time_step:
                self.events = pg.key.get_pressed()

                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()
                self.world.ClearForces()
                self.scene.update(self.events)
                accumulated_time -= time_step

            self.world.Step(time_step, 6, 2)
            self.screen.fill((255, 255, 255))
            self.scene.draw(self.screen)
            pg.display.flip()
            self.clock.tick(FPS)
            
        
        pg.quit()
        sys.exit()

      
class Scene:

    def __init__(self, engine, player):
        self.objects = []
        self.player = player
    

    def add_object(self, object):
        self.objects.append(object)

    def update(self, events):
        for obj in self.objects:
            if pg.sprite.collide_rect(obj, self.player) and self.player.velocity.y > 0:
                self.player.collision_occurred(obj)
            obj.update(events)
        self.player.update(events)
        

    def draw(self, window):
        self.player.draw(window)
        for obj in self.objects:
            obj.draw(window)

'''
GameObject
- Position (x, y)
- Image
- Rectangle
- Speed
'''

meters_to_pixels = 100
pixels_to_meters = 1/100

class GameObject(pg.sprite.Sprite):

    def __init__(self, x, y, world, image, width, height, type):
        super().__init__()
        self.x = x
        self.y = y
        
        image_temp = pg.image.load(image).convert_alpha()
        self.image = pg.transform.scale(image_temp, (width, height))
        print(self.image.get_width())
        
        self.rect = self.image.get_rect()
        print(self.rect.width)
        self.rect.x = x
        self.rect.y = y

        self.world = world

        if type == "dynamic":
            self.body = self.world.CreateDynamicBody(position=(self.rect.x * pixels_to_meters, self.rect.y * pixels_to_meters), fixedRotation=True)
        else:
            self.body = self.world.CreateStaticBody(position=(self.rect.x, self.rect.y), fixedRotation=True)
        self.shape = Box2D.b2PolygonShape()
        self.shape.SetAsBox(self.rect.width / 2 * pixels_to_meters, self.rect.height / 2 * pixels_to_meters)
        
        self.fixture = self.body.CreateFixture(shape=self.shape, density=.1, friction=0.3, restitution=0.5)
    
    



    def draw(self, window):
        window.blit(self.image, self.rect)

    @abstractmethod
    def update(self, events):
        pass

pixels_to_meters = 1/100
meters_to_pixels = 100
PLATFORM_WIDTH = 300

PLAYER_SIZE = 100 # Player will be 1m X 1m

class Player(GameObject):

    def __init__(self, world):
        super().__init__(x=768/2, y=600, world=world, image="assets/default.png", width=PLAYER_SIZE, height=PLAYER_SIZE, type = "dynamic")
        self.ground_speed = .15
        self.air_speed = .3
        self.current_speed = self.air_speed
        self.jump_force = -1.5
        self.velocity = Box2D.b2Vec2(0, 0)
        self.on_surface = False
        self.current_platform = None

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
            self.last_y = platform.rect.top - 1 # -1 so the player doesnt continuously collide
            self.velocity.y = 0
            self.on_ground()

        
    def update(self, events):
        self.velocity = self.body.linearVelocity

        self.check_wall_collisions()
        if self.current_platform:
            self.check_fall()
        self.handle_inputs(events)

        # apply velocity to body
        self.body.linearVelocity = self.velocity

        self.x, self.y = self.body.position * meters_to_pixels
        self.rect.x, self.rect.y = self.x, self.y

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
            self.velocity -= Box2D.b2Vec2(self.current_speed, 0)
        if events[pg.K_d]:
            self.velocity += Box2D.b2Vec2(self.current_speed, 0)

        # only allow jumping when on a platform
        if events[pg.K_SPACE] and self.on_surface:
            self.on_surface = False
            self.current_speed = self.air_speed
            self.body.ApplyLinearImpulse(Box2D.b2Vec2(0, self.jump_force), self.body.position, True)
            self.current_platform = None
            self.body.gravityScale = 1.0

    

    def check_wall_collisions(self):

        #if the player is on the bottom of the screen
        if self.y > 768 - PLAYER_SIZE:
            self.on_ground()
            self.y = 768 - PLAYER_SIZE - 1 # - 1 so the player doesn't continue to collide with the ground
            self.body.position = (self.x * pixels_to_meters, self.y * pixels_to_meters)
            self.velocity.y = 0

        if self.x < 0:
            self.velocity.x = abs(self.velocity.x)  # reverse x velocity
        elif self.x > 1024 - PLAYER_SIZE:
            self.velocity.x = -abs(self.velocity.x)

class Platform(GameObject):
    def __init__(self, x, y, world):
        super().__init__(x, y, world=world, image="assets/platform.png", width = PLATFORM_WIDTH, height = 40, type = "static")  


def generate_platform(y, world):
    x = random.randint(0, 1024 - PLATFORM_WIDTH)
    p = Platform(x, y, world)
    return p

def main():

    engine = Engine("Icy Tower")

    player = Player(engine.world)
    level = Scene(engine, player)

    platform_heights = [628, 528, 428, 328]
    for h in platform_heights:
        p = generate_platform(h, engine.world)
        level.add_object(p)
    
    engine.set_scene(level)
    engine.run()

if __name__ == "__main__":
    main()