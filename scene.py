import pygame as pg
class Scene:

    def __init__(self, engine, player):
        self.objects = []
        self.player = player
        self.camera_offset = (0, 0)
        self.engine = engine
    

    def add_object(self, object):
        self.objects.append(object)

    def update(self, events):
        
        for obj in self.objects:
            if pg.sprite.collide_rect(obj, self.player) and self.player.velocity.y > 0:
                self.player.collision_occurred(obj)
            obj.update(events)
        self.player.update(events)
        

    def draw(self, window):
        screen_width, screen_height = window.get_size()
        self.camera_offset = (-self.player.x + screen_width/2, -self.player.y + screen_height/2)
        self.player.draw(window, self.engine)
        for obj in self.objects:
            obj.draw(window, self.engine)

