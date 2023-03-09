import pygame as pg
class Scene:

    def __init__(self, engine, player):
        self.objects = []
        self.player = player
        self.sprites = pg.sprite.Group()

    def add_object(self, object):
        self.objects.append(object)

    def update(self, events):
        for obj in self.objects:
            if pg.sprite.collide_rect(self.player, obj):
                pass         
            obj.update(events)

        self.player.update(events)
        

    def draw(self, window):
        self.player.draw(window)
        for obj in self.objects:
            obj.draw(window)

