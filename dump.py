import os
import pygame as pg
import sys
import Box2D
from abc import abstractmethod


FPS = 60

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"


class Engine:

    def __init__(self, title, width=1024, height=768):
        self.title = title
        self.width = width
        self.height = height
        self.delta = 0
        self.world = Box2D.b2World(gravity=(0, 1000), doSleep=False)
        self.scene = None
        self.events = None
        self.pg_init()

    def pg_init(self):
        pg.init()
        self.screen = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption(self.title)
        self.clock = pg.time.Clock()
        self.last_time_checked = pg.time.get_ticks()
        pg.key.set_repeat(500)

    def set_scene(self, scene):
        self.scene = scene


    def run(self):
        self.running = True
        while self.running:

            self.events = pg.key.get_pressed()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
            self.world.Step(1.0 / 120, 6, 2)
            self.world.ClearForces()
            self.scene.update(self.events)
            
            self.screen.fill((255, 255, 255))
            self.scene.draw(self.screen)
            pg.display.flip()

            self.delta = pg.time.get_ticks() - self.last_time_checked
            self.clock.tick(FPS)
            self.last_time_checked = pg.time.get_ticks()
        
        pg.quit()
        sys.exit()

      
class Scene:

    def __init__(self, engine, player):
        self.objects = []
        self.player = player
        self.sprites = pg.sprite.Group()

    def add_object(self, object):
        self.objects.append(object)

    def update(self, events):
        for obj in self.objects:
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
        if not image:
            image_temp = pg.Surface((width, height))
            image_temp.fill((0, 0, 0))
            self.image = image_temp
        else:
            image_temp = pg.image.load(image).convert_alpha()
            self.image = pg.transform.scale(image_temp, (width, height))
        self.rect = self.image.get_rect() # rect is 100px by 100px
        self.rect.x = x
        self.rect.y = y

        self.world = world

        if type == "dynamic":
            self.body = self.world.CreateDynamicBody(position=(self.rect.x, self.rect.y), fixedRotation=True)
        else:
            self.body = self.world.CreateStaticBody(position=(self.rect.x, self.rect.y), fixedRotation=True)
        print(self.body.mass)
        self.shape = Box2D.b2PolygonShape()
        self.shape.SetAsBox(self.rect.width / 2 * pixels_to_meters, self.rect.height / 2 * pixels_to_meters)
        
        self.fixture = self.body.CreateFixture(shape=self.shape, density=.5, friction=0.3, restitution=0.5)
    
    



    def draw(self, window):
        window.blit(self.image, self.rect)

    @abstractmethod
    def update(self, events):
        pass


pixels_to_meters = 1/100
meters_to_pixels = 100

PLAYER_SIZE = 100

class Player(GameObject):

    def __init__(self, world):
        super().__init__(x=768/2, y=400, world=world, image="default.png", width=PLAYER_SIZE, height=PLAYER_SIZE, type = "dynamic")
        self.speed = 10 # lower speed for smoother momentum
        self.jump_force = -250
        self.velocity = Box2D.b2Vec2(0, 0)
        self.on_ground = False
        
    def update(self, events):
        self.velocity = self.body.linearVelocity

        self.check_walls()
        # update velocity based on keys pressed
        if events[pg.K_a]:
            self.velocity -= Box2D.b2Vec2(self.speed, 0)
        if events[pg.K_d]:
            self.velocity += Box2D.b2Vec2(self.speed, 0)
        
        if events[pg.K_SPACE]:
            self.body.ApplyForceToCenter(Box2D.b2Vec2(0, self.jump_force), True)
            print("Rect.x: ", self.rect.x)
            print("Self.x: ", self.x)
            print("Position.x: ", self.body.position.x)


        

        # apply velocity to body
        self.body.linearVelocity = self.velocity

        self.x, self.y = self.body.position * meters_to_pixels
        self.rect.x, self.rect.y = self.x, self.y

    def check_walls(self):
        if self.y > 768 - PLAYER_SIZE:
            self.y = 768 - PLAYER_SIZE
            self.body.position = (self.x, self.y)
            self.velocity.y = 0
            self.on_ground = True
        if self.x < 0:
            self.velocity.x = abs(self.velocity.x)  # reverse x velocity
        elif self.x > 1024 - PLAYER_SIZE:
            self.velocity.x = -abs(self.velocity.x)

class Ground(GameObject):
    def __init__(self, world):
        super().__init__(x = 0, y = 668, world=world, image=None, width = 1024, height = 50, type = "static")  

def main():

    engine = Engine("Icy Tower")

    player = Player(engine.world)
    #ground = Ground(engine.world)
    level = Scene(engine, player)

    
    #level.add_object(ground)
    engine.set_scene(level)
    engine.run()

if __name__ == "__main__":
    main()