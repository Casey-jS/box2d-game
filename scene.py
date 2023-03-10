import pygame as pg
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

