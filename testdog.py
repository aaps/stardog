#!/usr/bin/python
import os

import unittest
import pygame
from code.utils import *
from code.menuElements import *
from code.particles import *
from code.SoundSystem import *

os.environ["SDL_AUDIODRIVER"] = "dummy"

class TestMenuElements(unittest.TestCase):

    def setUp(self):
        self.fps = 10
        pygame.display.set_mode((400, 400), hardwareFlag | pygame.SRCALPHA)
        pygame.init()
        self.reset()
        
    def reset(self):
        self.toplevel = TopLevelPanel(Rect(0,0,200,200), [10,0,10,0])
        self.firstpanel = Label(Rect(0, 0, 100, 20), "A test !", color=SUPER_WHITE, font=BIG_FONT)
        self.secondpanel = Button(Rect(0, 20, 100, 20), self.dummyCallback, "Button test !", font=BIG_FONT)
        self.toplevel.addPanel(self.firstpanel)
        self.toplevel.addPanel(self.secondpanel)

    def dummyCallback(self):
        pass

    def testAddPanels(self):
        self.assertTrue(len(self.toplevel.panels) == 2)

    def testRemovePanels(self):
        self.toplevel.removePanel(self.firstpanel)
        self.assertTrue(len(self.toplevel.panels) == 1)

    def testDrawPanels(self):
       
        surf = pygame.Surface((self.toplevel.rect.width, self.toplevel.rect.height))
        oldval = totalColorVal(surf)
        self.toplevel.draw(surf)
        newval = totalColorVal(surf)
        self.assertTrue(oldval is not newval)
        self.toplevel.addPanel(self.firstpanel)
        self.toplevel.draw(surf)
        newerval = totalColorVal(surf)
        self.assertTrue(newerval is not newval)


    def testInputField(self):
        
        self.inputfield = InputField(Rect(0,0,20,20), self, self.dummyCallback,  FONT)
        self.assertTrue(self.inputfield.cursortimeout > 0)
        self.inputfield.update()
        self.assertTrue(self.inputfield.cursortimeout == 0)

class TestParticles(unittest.TestCase):

    def setUp(self):
        self.fps = 10
        pygame.display.set_mode((400, 400), hardwareFlag | pygame.SRCALPHA)
        pygame.init()
        self.pos = Vec2d(0,0)
        self.dir = 0
        self.emitter = Emitter( self, self.condAlways , 180, 10, 20, BLACK, PARTICLE1, 4, 5, 5, 3, 5, True)

    def testParticleGeneration(self):
        self.assertTrue(len(self.emitter.particles) is 0)
        self.emitter.update()
        self.emitter.update()
        self.assertTrue(len(self.emitter.particles) is 2)

    def testParticleDraw(self):
        surf = pygame.Surface((400, 400))
        self.emitter.draw(surf)
        self.assertTrue(totalColorVal(surf) is 0)
        self.emitter.update()
        self.emitter.draw(surf)
        self.assertTrue(totalColorVal(surf) is not 0)


    def condAlways(self):
        return True

class TestSoundSystem(unittest.TestCase):

    def setUp(self):
        self.asfx = "hullimpact.wav"
        self.music = MusicSystem("./res/sound/ambientMusic")
        self.sfx = SoundSystem("./res/sound/sfxSounds")

    def testGetSetVolFX(self):
        self.assertTrue(self.sfx.getVolume() is not 99)
        self.sfx.setVolume(99)
        self.assertTrue(self.sfx.getVolume() is 99)

    def testGetSetVolMU(self):
        self.assertTrue(self.music.getVolume() is not 99)
        self.music.setVolume(99)
        self.assertTrue(self.music.getVolume() is 99)

    def testReg(self):
        self.assertTrue( len(self.sfx.sounds) is 0)
        self.sfx.register(self.asfx)
        self.assertTrue( len(self.sfx.sounds) is 1)
        
    def testGetFileNames(self):
        self.assertTrue( len(self.sfx.getSounds()) > 0)
        self.assertTrue( len(self.music.getMusicFiles()) > 0)


if __name__ == '__main__':
    unittest.main()