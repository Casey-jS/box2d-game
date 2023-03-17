import os
import pygame as pg
import sys
from Box2D import b2World
from time import sleep

FPS = 120

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

class Engine:

    def __init__(self, title, width=800, height=768):
        self.title = title
        self.width = width
        self.height = height
        self.delta = 0
        self.world = b2World(gravity=(0, 40), doSleep=False)
        self.scene = None
        self.events = None
        self.pg_init()

    # creates the screen, the clock, and defines the key repeat 
    def pg_init(self):
        pg.init()
        self.screen = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption(self.title)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500)

    def set_scene(self, scene):
        self.scene = scene

    def set_running(self, val):
        self.running = val

    def run(self):

        time_step = 1 / FPS
        accumulated_time = 0
        self.running = True
        while self.running:
            self.delta = self.clock.tick(FPS) / 1000.0 # update delta
            accumulated_time += self.delta

            while accumulated_time >= time_step:
                self.events = pg.key.get_pressed()
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        self.running = False    
                self.world.ClearForces()        # clear the world's forces
                self.scene.update(self.events)  # update all game objects in the scene
                accumulated_time -= time_step

            self.world.Step(time_step, 6, 2)    # step through world 
            self.screen.fill((255, 255, 255))   
            self.scene.draw(self.screen)        # draw the scene
            pg.display.flip()                   # flip the display
            self.clock.tick(FPS)                # tick the clock
        pg.quit()
        