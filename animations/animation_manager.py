class AnimationManager:
    def __init__(self):
        self.anims = dict()
        self.lastKey = None

    def addAnimation(self, key, animation):
        self.anims[key] = animation
        self.lastKey = key
        
    def __getitem__(self, index):
        return self.anims[index]

    def update(self, key):
        if key in self.anims:
            self.anims[key].start()
            self.anims[key].update()
            self.lastKey = key
        else:
            self.anims[self.lastKey].stop()
            self.anims[self.lastKey].reset()

    def draw(self, surface, position, flip=False):
        self.anims[self.lastKey].draw(surface, position, flip)
