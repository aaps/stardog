# SoundSystem.py
import pygame
import os
import random

MISSILE_RADIUS = 50
SOUND_RADIUS = 3000

# def setVolume(channel, floater1, floater2):
#     from spaceship import Player
#     """sets volume for a channel based on the distance between
#      the player and floater."""
#     distance = floater2.pos.get_distance(floater1.pos)
#     if channel and floater1 and floater2:
#         volume = 0.0
#         if distance < SOUND_RADIUS and (isinstance(floater1, Player) or
#            isinstance(floater2, Player)):
#             volume = math.sqrt(((SOUND_RADIUS - distance)**1.8 /
#                                (SOUND_RADIUS + .001)**1.8))*SFX_VOLUME
#         channel.set_volume(volume)


class DummyMusicSystem(object):
    """
    a dummy class that has all the functions the Music Class uses.
    for example to disable the Music system on a server or such.
    """
    def __init__(self, musicdir, quality=44100):
        pass

    def getMusicFiles(self):
        return(['Dummy.ogg', 'Dummy2.ogg'])

    def play(self, music, amount=1):
        pass

    def setVolume(self, volume):
        pass

    def getVolume(self, volume):
        return(1.0)

    def getRandomMusic(self):
        return('Dummy.ogg')


class DummySoundSystem(object):
    """
    a dummy class that has all the fucntions the Sound Class uses.
    for example to disable the Sound system on a server or such.
    """
    def __init__(self, sounddir, quality=44100):
        pass

    def register(self, sound):
        pass

    def getSound(self):
        return('Dummy.ogg')

    def setVolume(self, volume):
        pass

    def getVolume(self):
        return(1.0)

    def play(self, sound, scale_f=None, loops=0):
        pass


class MusicSystem(object):
    """
    the MusicSystem class.
    that wraps pygame functions for running music.
    <musicdir>(str) that is the location of the music files.
    <quality>(int) that is the quality the pygame system will be
    initialized to.
    """
    def __init__(self, musicdir, quality=44100):
        try:
            pygame.mixer.init(quality)
        except Exception as e:
            print(e)
        else:
            # 20% volume default
            self.musicvolume = (20./100)
            # get the music files in musicdir
            self.musicdir = musicdir
            self.musicfiles = os.listdir(musicdir)
            pygame.mixer.music.set_volume(self.musicvolume)
    """ returns a list of music files."""
    def getMusicFiles(self):
        return self.musicfiles
    """
        play function that plays <music>(str),
        and the number of loops <loops>(int)
        default unlimited loops (-1)
    """
    def play(self, music, loops=-1):
        index = self.musicfiles.index(music)
        filelocation = str(self.musicdir) + str(self.musicfiles[index])
        pygame.mixer.music.load(filelocation)
        pygame.mixer.music.play(loops)
        pygame.mixer.music.set_volume(self.musicvolume)
    """ function to set the music volume. """
    def setVolume(self, volume):
        self.musicvolume = volume
        pygame.mixer.music.set_volume(volume)
    """ function to get the current music volume """
    def getVolume(self):
        return self.musicvolume
    """ returns a random music file. """
    def getRandomMusic(self):
        return(self.musicfiles[random.randint(0, len(self.musicfiles)-1)])


class SoundSystem(object):
    """
    the SoundSystem class.
    a wrapper around the pygame sound system.
    <soundDir>(str) is the location of the sound files.
    <quality>(int) is the quality the pygame system,
    is initialized to.
    """
    def __init__(self, soundDir, quality=44100):
        try:
            pygame.mixer.init(quality)
        except Exception as e:
            print(e)
        # 5% volume default
        self.sfxvolume = (5./100)
        self.soundDir = soundDir
        self.soundFiles = os.listdir(soundDir)
        self.sounds = {}
    """ function to register a <sound>(str) to the soundsystem """
    def register(self, sound):
        location = str(self.soundDir)+str(sound)
        self.sounds[sound] = pygame.mixer.Sound(location)
        for sound in self.sounds:
            self.sounds[sound].set_volume(self.sfxvolume)
    """ returns the <soundFiles>(list) found at <soundDir> """
    def getSounds(self):
        return self.soundFiles
    """ sets the <volume>(float) for playing sounds """
    def setVolume(self, volume):
        self.sfxvolume = volume
    """ returns the current value for <volume>(float) """
    def getVolume(self):
        return self.sfxvolume
    """ function that plays a <sound>(str)
        with scaled volume returned by <scale_f>(<func>(float))
        default no scaling
        and loop for number of <loops>(int)
        default 0 loops. (played once.)
    """
    def play(self, sound, scale_f=None, loops=0):
        self.sounds[sound].play(loops)
