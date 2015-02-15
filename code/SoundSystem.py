import pygame
import os
import random
import math

MISSILE_RADIUS = 50
SOUND_RADIUS = 3000
# 20%
SFX_VOLUME = 0#(20./100)
# 60%
MUSIC_VOLUME = 0#(5./100)


class SoundSystem(object):
    def __init__(self):
        pass

# setup sounds
try:
    pygame.mixer.init(44100)

    shootSound = pygame.mixer.Sound("res/sound/lazer.ogg")
    hitSound = pygame.mixer.Sound("res/se_sdest.wav")
    explodeSound = pygame.mixer.Sound("res/se_explode03.wav")
    missileSound = pygame.mixer.Sound("res/se_explode02.wav")
    messageSound = pygame.mixer.Sound("res/sound/message pip.ogg")

    # load al ambient music (for now just travel music)
    # might also load fighting music this way.
    # and question music and other kinds of music.
    travelMusicDir = "res/sound/ambientSound/"
    travelMusicFiles = os.listdir(travelMusicDir)
    travelMusic = []
    # for musicfile in os.listdir(travelMusicDir):
    #     sound = pygame.mixer.Sound(travelMusicDir+str(musicfile))
    #     travelMusic.append(sound)
    # for now choose a random music number to play
    randIndex = random.randint(0, len(travelMusicFiles)-1)
    location = str(travelMusicDir) + str(travelMusicFiles[randIndex])
    print location
    pygame.mixer.music.load(location)
    pygame.mixer.music.play(-1)
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