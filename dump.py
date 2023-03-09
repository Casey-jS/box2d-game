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
        self.paused = False
        self.world = Box2D.b2World(gravity=(0, -10))
        self.scene = None
        self._init_pygame()


    def run(self):

        while True:
            self._handle_events()
            self._game_loop()
            pg.display.flip()
            self._update_delta()

    def set_scene(self, scene):
        self.scene = scene

    def _init_pygame(self):
        pg.init()
        pg.key.set_repeat(500)
        self.screen = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption(self.title)
        self.clock = pg.time.Clock()
        self.last_time_checked = pg.time.get_ticks()


    def _handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

    def _game_loop(self):
        if not self.paused:
            if self.scene:
                self.scene.update()
                self.world.Step(self.delta_seconds, 6, 2)
            self.screen.fill((255, 255, 255))
            if self.scene:
                self.scene.draw(self.screen)

    def _update_delta(self):
        now = pg.time.get_ticks()
        self.delta = now - self.last_time_checked
        self.last_time_checked = now

    @property
    def delta_seconds(self):
        return self.delta / 1000.0

    @property
    def events(self):
        return pg.event.get()




'''
GameObject
- Position (x, y)
- Image
- Rectangle
- Speed
'''

class GameObject(pg.sprite.Sprite):

    def __init__(self, x, y, world, image="default.png", speed=10):
        super().__init__()
        self.x = x
        self.y = y
        self.speed = speed

        self.image: pg.Surface = pg.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


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

    def __init__(self, world, x=768/2, y=400):
        super().__init__(x, y, world)
        self.speed = 100
        self.jump_force = 10
        
        self.body = world.CreateDynamicBody(
            position = (x, y),
            fixedRotation = True
        )
        self.fixture = self.body.CreatePolygonFixture(
            box = (1, 1),
            density = 1,
            friction = 0.3,
            restitution = 0.0
        )


    def update(self):

        keys = pg.key.get_pressed()

        if keys[pg.K_a]: self.body.ApplyForce((-self.speed, 0), self.body.worldCenter, True)
        
        if keys[pg.K_d]: self.body.ApplyForce((self.speed, 0), self.body.worldCenter, True)
        
        if keys[pg.K_SPACE]:
            print("Jumping")
            self.body.ApplyLinearImpulse((0, self.jump_force), self.body.worldCenter, True)
            print(self.body.position)
        self.rect.x, self.rect.y = self.body.position
        self.x = self.rect.x
        self.y = self.rect.y
        

def main():
    engine = Engine("Icy Tower")
    player = Player(world)
    level = Scene(engine)
    level.add_object(player)
    engine.set_scene(level)
    engine.run()

if __name__ == "__main__":
    main()