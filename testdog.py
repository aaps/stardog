#!/usr/bin/python
import os

import unittest
import pygame
from code.utils import *
from code.menuElements import *
from code.particles import *
from code.SoundSystem import *
from code.vec2d import *
import pickle

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
class UnitTestVec2D(unittest.TestCase):

        def setUp(self):
            pass

        def testCreationAndAccess(self):
            v = Vec2d(111,222)
            self.assert_(v.x == 111 and v.y == 222)
            v.x = 333
            v[1] = 444
            self.assert_(v[0] == 333 and v[1] == 444)

        def testMath(self):
            v = Vec2d(111,222)
            self.assertEqual(v + 1, Vec2d(112,223))
            self.assert_(v - 2 == [109,220])
            self.assert_(v * 3 == (333,666))
            self.assert_(v / 2.0 == Vec2d(55.5, 111))
            self.assert_(v / 2 == (55.5, 111))
            self.assert_(v ** Vec2d(2,3) == [12321, 10941048])
            self.assert_(v + [-11, 78] == Vec2d(100, 300))
            self.assert_(v / [10,2] == [11.1,111])

        def testReverseMath(self):
            v = Vec2d(111,222)
            self.assert_(1 + v == Vec2d(112,223))
            self.assert_(2 - v == [-109,-220])
            self.assert_(3 * v == (333,666))
            self.assert_([222,888] / v == [2,4])
            self.assert_([111,222] ** Vec2d(2,3) == [12321, 10941048])
            self.assert_([-11, 78] + v == Vec2d(100, 300))

        def testUnary(self):
            v = Vec2d(111,222)
            v = -v
            self.assert_(v == [-111,-222])
            v = abs(v)
            self.assert_(v == [111,222])

        def testLength(self):
            v = Vec2d(3,4)
            self.assert_(v.length == 5)
            self.assert_(v.get_length_sqrd() == 25)
            self.assert_(v.normalize_return_length() == 5)
            self.assert_(v.length == 1)
            v.length = 5
            self.assert_(v == Vec2d(3,4))
            v2 = Vec2d(10, -2)
            self.assert_(v.get_distance(v2) == (v - v2).get_length())

        def testAngles(self):
            v = Vec2d(0, 3)
            self.assertEqual(v.angle, 90)
            v2 = Vec2d(v)
            v.rotate(-90)
            self.assertEqual(v.get_angle_between(v2), 90)
            v2.angle -= 90
            self.assertEqual(v.length, v2.length)
            self.assertEqual(v2.angle, 0)
            self.assertEqual(v2, [3, 0])
            self.assertTrue(((v - v2).length > .00001)==False)
            self.assertEqual(v.length, v2.length)
            v2.rotate(300)
            self.assertAlmostEqual(v.get_angle_between(v2), -60)
            v2.rotate(v2.get_angle_between(v))
            angle = v.get_angle_between(v2)
            self.assertAlmostEqual(v.get_angle_between(v2), 0)

        def testHighLevel(self):
            basis0 = Vec2d(5.0, 0)
            basis1 = Vec2d(0, .5)
            v = Vec2d(10, 1)
            self.assert_(v.convert_to_basis(basis0, basis1) == [2, 2])
            self.assert_(v.projection(basis0) == (10, 0))
            self.assert_(basis0.dot(basis1) == 0)

        def testCross(self):
            lhs = Vec2d(1, .5)
            rhs = Vec2d(4,6)
            self.assert_(lhs.cross(rhs) == 4)

        def testComparison(self):
            int_vec = Vec2d(3, -2)
            flt_vec = Vec2d(3.0, -2.0)
            zero_vec = Vec2d(0, 0)
            self.assert_(int_vec == flt_vec)
            self.assert_(int_vec != zero_vec)
            self.assert_((flt_vec == zero_vec) == False)
            self.assert_((flt_vec != int_vec) == False)
            self.assert_(int_vec == (3, -2))
            self.assert_(int_vec != [0, 0])
            self.assert_(int_vec != 5)
            self.assert_(int_vec != [3, -2, -5])

        def testInplace(self):
            inplace_vec = Vec2d(5, 13)
            inplace_ref = inplace_vec
            inplace_src = Vec2d(inplace_vec)
            inplace_vec *= .5
            inplace_vec += .5
            inplace_vec /= (3, 6)
            inplace_vec += Vec2d(-1, -1)
            self.assertEqual(inplace_vec, inplace_ref)

        def testPickle(self):
            testvec = Vec2d(5, .3)
            testvec_str = pickle.dumps(testvec)
            loaded_vec = pickle.loads(testvec_str)
            self.assertEqual(testvec, loaded_vec)

        def testInterpolate(self):
            v1=Vec2d(6,8)
            v2=Vec2d(14,12)
            range=0.1
            v3=v1.interpolate_to(v2,range)
            self.assert_(v3.x==6.8)
            self.assert_(v3.y==8.4)


    ####################################################################


if __name__ == '__main__':
    unittest.main()