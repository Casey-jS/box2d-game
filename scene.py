import pygame as pg
class Scene:

    def __init__(self, engine, player):
        self.objects = []
        self.player = player
    
    def player_is_on_platform(self, object) -> bool:
        player_right = self.player.rect.right
        player_left = self.player.rect.left
        player_bottom = self.player.rect.bottom

        platform_top = object.rect.top
        platform_right = object.rect.right
        platform_left = object.rect.left

        above = player_bottom <= platform_top
        inside = player_left > platform_left and player_right < platform_right

        return above and inside


    def add_object(self, object):
        self.objects.append(object)

    def update(self, events):
        for obj in self.objects:
            if pg.sprite.collide_rect(obj, self.player) and self.player.velocity.y > 0:
                print("collision detected")
                self.player.last_y = self.player.y - 1 # -1 so the player doesnt continuously collide
                self.player.velocity.y = 0
                self.player.on_ground()
            obj.update(events)
        self.player.update(events)
        

    def draw(self, window):
        self.player.draw(window)
        for obj in self.objects:
            obj.draw(window)

