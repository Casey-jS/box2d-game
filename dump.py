import os
import pygame as pg
import sys
import Box2D 
from abc import abstractmethod

FPS = 60

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

class Engine:

    delta = 0 # time elapsed since last frame
    events = None # current set of events for this frame
    current_scene = None # scene we are currently running

    def __init__(self, title, width=1024, height=768):
        self.title = title
        self.running = False
        self.width = width
        self.height = height
        self.pg_init()
        self.scene = None
        self.world = Box2D.b2World(gravity = (0, -10))


    
    # sets the screen dimensions, clock, and title
    def pg_init(self):
        pg.init()
        self.screen = pg.display.set_mode((self.width, self.height)) # set screen
        pg.display.set_caption(self.title) # screen caption
        self.clock = pg.time.Clock()
        self.last_time_checked = pg.time.get_ticks()
        pg.key.set_repeat(500) # set repeat delay for key presses
        self.paused = False

    def run(self):
        self.running = True
        while self.running:
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            if self.scene:
                self.scene.update()

            self.screen.fill((255, 255, 255))
            self.scene.draw(self.screen)
            pg.display.flip()

            self.delta = pg.time.get_ticks() - self.last_time_checked
            self.clock.tick(FPS)
            self.last_time_checked = pg.time.get_ticks()
        
        pg.quit()
        sys.exit()





'''
GameObject
- Position (x, y)
- Image
- Rectangle
- Speed
'''

class GameObject(pg.sprite.Sprite):

    def __init__(self, x, y, image="default.png", speed=10):
        super().__init__()
        self.x = x
        self.y = y
        self.speed = speed

        self.image: pg.Surface = pg.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()

    
    def draw(self, window):
        window.blit(self.image, self.rect)

    @abstractmethod
    def update(self):
        pass




class Scene:

    def __init__(self, engine):
        self.objects = []

    def add_object(self, object):
        self.objects.append(object)

    def update(self):
        for obj in self.objects:
            obj.update()

    def draw(self, window):
        for obj in self.objects:
            obj.draw(window)

w2b = 1/100
b2w = 100
gravity = Box2D.b2Vec2(0.5, -10.0)
world = Box2D.b2World(gravity,doSleep=False)


class Player(GameObject):

    def __init__(self, world):
        super().__init__(0, 0, "default.png")
        self.speed = 500
        self.world = world
        self.jump_force = 25000

        body_def = Box2D.b2BodyDef()
        body_def.type = Box2D.b2_dynamicBody
        body_def.position = (self.x/w2b, self.y/w2b)
        self.body = world.CreateBody(body_def)

        shape = Box2D.b2PolygonShape()
        shape.SetAsBox(0.5, 0.5)
        fixture_def = Box2D.b2FixtureDef(shape=shape, density=1, friction=0.3)
        self.body.CreateFixture(fixture_def)

    def update(self):

        keys = pg.key.get_pressed()

        if keys[pg.K_a]: self.body.ApplyForce((-self.speed, 0), self.body.worldCenter, True)
        
        
        if keys[pg.K_d]: self.body.ApplyForce((self.speed, 0), self.body.worldCenter, True)
        
        if keys[pg.K_SPACE]:
            print("Jumping")
            self.body.ApplyLinearImpulse((0, self.jump_force), self.body.worldCenter, True)

        print(self.body.position)
        self.x, self.y = self.body.position * w2b * b2w
        self.rect.x, self.rect.y = self.x - self.rect.width/2, self.y - self.rect.height/2



class Ground(GameObject):
    def __init__(self, x, y):
        super().__init__()
        self.body = world.createStaticBody()

def main():
    engine = Engine("Icy Tower")
    player = Player(world)

    level = Scene(engine)
    engine.scene = level

    level.add_object(player)
    engine.run()

if __name__ == "__main__":
    main()