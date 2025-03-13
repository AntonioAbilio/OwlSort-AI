class AnimationManager:
    def __init__(self):
        self.anims = dict()
        self.lastKey = None

    def addAnimation(self, key, animation):
        self.anims[key] = animation
        self.lastKey = key

    def update(self, key):
        if key in self.anims:
            self.anims[key].start()
            self.anims[key].update()
            self.lastKey = key
        else:
            self.anims[self.lastKey].stop()
            self.anims[self.lastKey].reset()

    def draw(self, surface, position):
        self.anims[self.lastKey].draw(surface, position)
