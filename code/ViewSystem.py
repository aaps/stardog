class ViewSystem(object):

    def __init__(self, resDir):

        self.resDir = resDir
        self.resFiles = os.listdir(resDir)
        self.reses = {}

    def register(self, res):
        location = str(self.resDir)+str(res)
        self.reses[res] = pygame.mixer.Sound(location)


    def getReses(self):
        return self.resFiles


    def draw(self, sound, scale_f=None, loops=0):
        self.reses[sound].play(loops)