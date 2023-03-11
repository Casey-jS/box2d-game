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
            # check if player collided with another game object
            if pg.sprite.collide_rect(obj, self.player) and self.player.velocity.y > 0:
                # tell player that a collision occurred
                self.player.collision_occurred(obj)
            obj.update(events)
        self.player.update(events)
        

    def draw(self, window):
        _, screen_height = window.get_size()

        # set the camera offset based on the height of the player
        self.camera_offset = (0, -self.player.y + screen_height/2)

        # draw the player
        self.player.draw(window, self.engine)

        # draw all other game objects
        for obj in self.objects:
            obj.draw(window, self.engine)

