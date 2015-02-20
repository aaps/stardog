import pygame
import os
import random
import math

MISSILE_RADIUS = 50
SOUND_RADIUS = 3000
# 5%
SFX_VOLUME = (5./100)
# 20%
MUSIC_VOLUME = (20./100)


class MusicSystem(object):
    def __init__(self, universe, musicdir, quality=44100):
        # 20% volume
        self.musicvolume = (20./100)
        # get the music files in musicdir
        self.musicdir = musicdir
        self.musicfiles = os.listdir(musicdir)
        try:
            pygame.mixer.init(quality)
        except Exception as e:
            print(e)

    def playMusic(self, volume):
        pass

    def setMusicVolume(self, volume):
        self.musicvolume = volume

    def getMusicVolume(self):
        return self.musicvolume


class SoundSystem(object):
    def __init__(self, universe, quality=44100):
        self.universe = universe
        # 5% volume
        self.sfxvolume = (5./100)
        self.sounds = {}

        try:
            pygame.mixer.init(quality)
        except Exception as e:
            print(e)

        # pygame.mixer.

    def register(self, sound):
        self.sounds[sound] = pygame.mixer.Sound(sound)

    def setSFXVolume(self, volume):
        self.setSFXVolume = volume
        for sound in self.sounds:
            self.sounds[sound].set_volume(self.sfxvolume)

    def getSFXVolume(self):
        return self.sfxvolume

    def play(self, sound, amount=1):
        # self.sounds[sound].set_volume(self.sfxvolume)
        self.sounds[sound].play(amount)
        # self.sounds[sound].


def setMusicVolume(volume):
    global MUSIC_VOLUME
    if not volume:
        MUSIC_VOLUME = float(volume)
        pygame.mixer.music.set_volume(volume)
    else:
        MUSIC_VOLUME = 1./(volume/100.)
        pygame.mixer.music.set_volume(volume)


def setSFXVolume(volume):
    global SFX_VOLUME
    if not volume:
        SFX_VOLUME = float(volume)
        pygame.mixer.Sound.set_volume(volume)
    else:
        SFX_VOLUME = 1./(volume/100.)
        pygame.mixer.Sound.set_volume(volume)


# setup sounds
try:
    pygame.mixer.init(44100)

    gunShootSound = pygame.mixer.Sound("res/sound/gunShot-Duality-edit.ogg")
    shootSound = pygame.mixer.Sound("res/sound/lazer.ogg")
    laserShootSound = pygame.mixer.Sound("res/sound/lazer-duality-edit.ogg")
    hitSound = pygame.mixer.Sound("res/se_sdest.wav")
    explodeSound = pygame.mixer.Sound("res/se_explode03.wav")
    missileSound = pygame.mixer.Sound("res/se_explode02.wav")
    messageSound = pygame.mixer.Sound("res/sound/message pip.ogg")

    # load al ambient music (for now just travel music)
    # might also load fighting music this way.
    # and question music and other kinds of music.
    travelMusicDir = "res/sound/ambientMusic/"
    travelMusicFiles = os.listdir(travelMusicDir)
    travelMusic = []
    # for musicfile in os.listdir(travelMusicDir):
    #     sound = pygame.mixer.Sound(travelMusicDir+str(musicfile))
    #     travelMusic.append(sound)
    # for now choose a random music number to play
    randIndex = random.randint(0, len(travelMusicFiles)-1)
    location = str(travelMusicDir) + str(travelMusicFiles[randIndex])

    pygame.mixer.music.load(location)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(MUSIC_VOLUME)
    # print(os.listdir(travelMusicDir)[randIndex])
    # travelMusic[randIndex].play(-1)
    # travelMusic[randIndex].set_volume(MUSIC_VOLUME)

    soundModule = True
except (ImportError, NotImplementedError):
    soundModule = False
    print("Sound module not found. Sounds disabled.")


def setVolume(channel, floater1, floater2):
    from spaceship import Player
    """sets volume for a channel based on the distance between
     the player and floater."""
    distance = floater2.pos.get_distance(floater1.pos)
    if channel and floater1 and floater2:
        volume = 0.0
        if distance < SOUND_RADIUS and (isinstance(floater1, Player) or
           isinstance(floater2, Player)):
            volume = math.sqrt(((SOUND_RADIUS - distance)**1.8 /
                               (SOUND_RADIUS + .001)**1.8))*SFX_VOLUME
        channel.set_volume(volume)