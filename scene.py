
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

