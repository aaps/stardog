
from parts import *
from utils import loadImage

class Scrap(Part):
    baseImage = loadImage("res/goods/scrap.png")
    image = None

    def __init__(self, universe):
        # Part.__init__(self, universe)
        self.name = "Scrap"
        self.resources = True

    def update(self):
        # Part.update(self)
        pass

    def shortStats(self):
        return "Scrap"

    def stats(self):
        return "It is Scrap"
