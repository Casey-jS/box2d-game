import os
import pygame as pg
import sys
from Box2D import b2World

FPS = 60

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"


class Engine:

    def __init__(self, title, width=1024, height=768):
        self.title = title
        self.width = width
        self.height = height
        self.delta = 0
        self.paused = False
        self.world = b2World(gravity=(0, 400), doSleep=False)
        self.scene = None
        self.pg_init()

    def pg_init(self):
        pg.init()
        pg.key.set_repeat(500)
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

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
            self.world.Step(1.0 / 60, 6, 2)
            self.world.ClearForces()
            self.scene.update()
            
            self.screen.fill((255, 255, 255))
            self.scene.draw(self.screen)
            pg.display.flip()

            self.delta = pg.time.get_ticks() - self.last_time_checked
            self.clock.tick(FPS)
            self.last_time_checked = pg.time.get_ticks()
        
        pg.quit()
        sys.exit()

      
