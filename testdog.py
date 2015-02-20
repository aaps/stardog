#!/usr/bin/python

import unittest
import pygame
from code.utils import *
from code.menuElements import *
from code.floaters import *
from code.parts import *

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
        
        self.inputfield = InputField(Rect(0,0,20,20), self)
        self.assertTrue(self.inputfield.cursortimeout > 0)
        self.inputfield.update()
        self.assertTrue(self.inputfield.cursortimeout == 0)

# class TestMenuElements(unittest.TestCase):

#     def setUp(self):
#         cockpit = Interceptor(self)
#         engine = Engine(self)


if __name__ == '__main__':
    unittest.main()