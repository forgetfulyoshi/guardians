from direct.showbase import DirectObject
from pandac.PandaModules import *
import sys

class SoundHandler(DirectObject.DirectObject):
    def __init__(self):
        self.accept("playSfx", self.playSfx)
        self.accept("playMusic", self.playMusic)
        self.accept("playVoice", self.playVoice)

        self.accept("stopSfx", self.stopSfx)
        self.accept("stopMusic", self.stopMusic)
        self.accept("stopVoice", self.stopVoice)

        self.accept("setSfxVolume", self.setSfxVolume)
        self.accept("setMusicVolume", self.setMusicVolume)
        self.accept("setVoiceVolume", self.setVoiceVolume)

        self.accept("addSfx", self.addSfx)
        self.accept("addMusic", self.addMusic)
        self.accept("addVoice", self.addVoice)
        
        self.accept("loopSfx", self.loopSfx)
        self.accept("loopMusic", self.loopMusic)

        self.accept("fireGun", self.playSfx, ["primaryGun"])
        self.accept("fireMissile", self.playSfx, ["secondaryGun"])
        self.accept("shipDestroyed", self.playSfx, ["shipDestroyed"])
        self.accept("toggleShipAmbient", self.toggleShipAmbient)
        self.accept("toggleWarning", self.toggleWarning)

        self.sfxVolume = 1
        self.musicVolume = 1
        self.voiceVolume = 1

        self.sfxList = {}
        self.musicList = {}
        self.voiceList = {}


        #Common Sounds
        #-------------------------------------------------------------------
        self.primaryGun = loader.loadSfx("Art/audio/laser1.wav")
        self.primaryGun.setVolume(self.sfxVolume)
        self.sfxList["primaryGun"] = self.primaryGun

        self.secondaryGun = loader.loadSfx("Art/audio/missileLaunch.wav")
        self.secondaryGun.setVolume(self.sfxVolume)
        self.sfxList["secondaryGun"] = self.secondaryGun

        self.shipDestroyed = loader.loadSfx("Art/audio/otherShipExploding.wav")
        self.shipDestroyed.setVolume(self.sfxVolume)
        self.sfxList["shipDestroyed"] = self.shipDestroyed

        self.shipAmbient = loader.loadSfx("Art/audio/shipAmbient.wav")

        self.shipWarning = loader.loadSfx("Art/audio/shipWarning.wav")
        #-------------------------------------------------------------------


    def playSfx(self, soundName):
        if self.sfxList.has_key(soundName):
            self.sfxList[soundName].play()

    def playMusic(self, musicName):
        if self.musicList.has_key(musicName):
            self.musicList[musicName].play()

    def playVoice(self, voiceName):
        if self.voiceList.has_key(voiceName):
            self.voiceList[voiceName].play()


    def stopSfx(self, soundName = ""):
        if soundName == "":
            for sound in self.sfxList:
                self.sfxList[sound].stop()

        elif self.sfxList.has_key(soundName):
            self.sfxList[soundName].stop()

    def stopMusic(self, musicName = ""):
        if musicName == "":
            for sound in self.musicList:
                self.musicList[sound].stop()

        elif self.musicList.has_key(musicName):
            self.musicList[musicName].stop()

    def stopVoice(self, voiceName = ""):
        if voiceName == "":
            for sound in self.voiceList:
                self.voiceList[sound].stop()

        elif self.voiceList.has_key(voiceName):
            self.voiceList[voiceName].stop()

    def addSfx(self, soundName, soundPath):
        sound = loader.loadSfx(soundPath)
        sound.setVolume(self.sfxVolume)
        self.sfxList[soundName] = sound

    def addMusic(self, soundName, soundPath):
        sound = loader.loadSfx(soundPath)
        sound.setVolume(self.musicVolume)
        self.musicList[soundName] = sound

    def addVoice(self, soundName, soundPath):
        sound = loader.loadSfx(soundPath)
        sound.setVolume(self.voiceVolume)
        self.voiceList[soundName] = sound

    def setSfxVolume(self, volume):
        if 0.0 <= volume and volume <= 1.0:
            self.sfxVolume = volume
            for sound in self.sfxList:
                self.sfxList[sound].setVolume(self.sfxVolume)

    def setMusicVolume(self, volume):
        if 0.0 <= volume and volume <= 1.0:
            self.musicVolume = volume
            for sound in self.musicList:
                self.musicList[sound].setVolume(self.musicVolume)

    def setVoiceVolume(self, volume):
        if 0.0 <= volume and volume <= 1.0:
            self.voiceVolume = volume
            for sound in self.voiceList:
                self.voiceList[sound].setVolume(self.voiceVolume)
                
    #Looping for SFX and Music, must restart the music to take effect
    #-------------------------------------------------------------------
    def loopSfx(self, soundName = ""):
        if soundName == "":
            for sound in self.sfxList:
                sound.setLoop(True)
                sound.setLoopCount(0)
        else:
            self.sfxList[soundName].setLoop(True)
            self.sfxList[soundName].setLoopCount(0)
            
    
    def loopMusic(self, musicName = ""):
        if musicName == "":
            for music in self.musicList:
                music.setLoop(True)
                music.setLoopCount(0)
        else:
            self.musicList[musicName].setLoop(True)
            self.musicList[musicName].setLoopCount(0)
    #-------------------------------------------------------------------

    def getSfxVolume(self):
        return self.sfxVolume

    def getMusicVolume(self):
        return self.musicVolume

    def getVoiceVolume(self):
        return self.voiceVolume

    def toggleShipAmbient(self):
        if self.shipAmbient.status():
            self.shipAmbient.setVolume(0.5)
            self.shipAmbient.setLoop(True)
            self.shipAmbient.play()
        else:
            self.shipAmbient.stop()

    def toggleWarning(self):
        if self.shipWarning.status() == 1:
            self.shipWarning.setVolume(0.3)
            self.shipWarning.setLoop(True)
            self.shipWarning.play()
        elif self.shipWarning.status() == 2:
            self.shipWarning.setLoop(False)
            self.shipWarning.stop()

    def cleanUp(self):
        self.ignoreAll()

        del self.sfxVolume
        del self.musicVolume
        del self.voiceVolume

        del self.sfxList
        del self.musicList
        del self.voiceList
