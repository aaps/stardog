import pygame
import os
import random
import math

MISSILE_RADIUS = 50
SOUND_RADIUS = 3000


class DummyMusicSystem(object):
    def __init__(self, universe, musicdir, quality=44100):
        pass

    def getMusicFiles(self):
        pass

    def play(self, music, amount=1):
        pass

    def setVolume(self, volume):
        pass

    def getVolume(self, volume):
        pass

    def getRandomMusic(self):
        pass


class MusicSystem(object):
    def __init__(self, musicdir, quality=44100):
        try:
            pygame.mixer.init(quality)
        except Exception as e:
            print(e)
        else:
            # 20% volume
            self.musicvolume = (20./100)
            # get the music files in musicdir
            self.musicdir = musicdir
            self.musicfiles = os.listdir(musicdir)
            pygame.mixer.music.set_volume(self.musicvolume)

    def getMusicFiles(self):
        return self.musicfiles

    def play(self, music, loops=-1):
        index = self.musicfiles.index(music)
        filelocation = str(self.musicdir) + str(self.musicfiles[index])
        pygame.mixer.music.load(filelocation)
        pygame.mixer.music.play(loops)
        pygame.mixer.music.set_volume(self.musicvolume)

    def setVolume(self, volume):
        self.musicvolume = volume
        pygame.mixer.music.set_volume(volume)

    def getVolume(self):
        return self.musicvolume

    def getRandomMusic(self):
        return(self.musicfiles[random.randint(0, len(self.musicfiles)-1)])


class SoundSystem(object):
    def __init__(self, soundDir, quality=44100):
        try:
            pygame.mixer.init(quality)
        except Exception as e:
            print(e)
        # 5% volume
        self.sfxvolume = (5./100)
        self.soundDir = soundDir
        self.soundFiles = os.listdir(soundDir)
        self.sounds = {}

    def register(self, sound):
        location = str(self.soundDir)+str(sound)
        self.sounds[sound] = pygame.mixer.Sound(location)
        for sound in self.sounds:
            self.sounds[sound].set_volume(self.sfxvolume)

    def getSounds(self):
        return self.soundFiles

    def setVolume(self, volume):
        self.sfxvolume = volume

    def getVolume(self):
        return self.sfxvolume

    def play(self, sound, loops=0):
        print(sound)
        self.sounds[sound].play(loops)
