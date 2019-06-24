from direct.showbase import DirectObject
from pandac.PandaModules import *
from direct.fsm import FSM
from direct.task import Task
from direct.gui.OnscreenImage import OnscreenImage
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from SoundHandler import *

import random

class CutScene(DirectObject.DirectObject):
    def __init__(self):
        
        x = SoundHandler()
        
        self.cutSceneNode = render.attachNewNode("cutSceneNode")
        self.cutSceneNode.reparentTo(render)
        self.cutSceneNode.setPos(0,0,0)
        self.cutSceneNode.setScale(1)
        
        self.scene = loader.loadModel("Art/jailcell.bam")
        self.scene.reparentTo(self.cutSceneNode)
        
        #base.camera.lookAt(Point3(0,0,0))
        
        self.lightNode = self.scene.find("**/light")
        
        self.alight = AmbientLight('alight')
        self.alight.setColor(VBase4(0.09, 0.09, 0.09, 1))
        self.alnp = render.attachNewNode(self.alight)
        render.setLight(self.alnp)
        self.door = self.scene.find("**/pCube3")
        #
        #self.plight = PointLight('plight')
        #self.plight.setColor(VBase4(0.02, 0.02, 0.02, 1))
        #self.plnp = self.scene.find("**/lightLocator1").attachNewNode(self.plight)
        #self.plnp.setPos(self.plnp, Point3(0,0,-8))
        #render.setLight(self.plnp)
        
        self.lamplist = []
        self.lamplist.append(self.scene.find("**/lamp"))
        self.lamplist.append(self.scene.find("**/lamp1"))
        self.lamplist.append(self.scene.find("**/lamp2"))
        self.lamplist.append(self.scene.find("**/lamp4"))
        self.lamplist.append(self.scene.find("**/lamp6"))
        

        self.dlight = DirectionalLight('dlight')
        self.dlight.setColor(VBase4(.8, .8, .8, 1))
        self.dlnp = render.attachNewNode(self.dlight)
        self.dlnp.setP(90)
        for y in self.lamplist:
            y.setLight(self.dlnp)
            
        self.tempLightNode = render.attachNewNode("tempLightNode")    
        
        self.slightList = []
        self.slnpList = []
        for x in range(1,6):
            #print x
            slight = Spotlight('slight2')
            slight.setColor(VBase4(.8, .8, .8, 1))
            lens = PerspectiveLens()
            lens.setFov(90)
            slight.setLens(lens)
            lightstring = "**/lightLocator" + str(x)
            lightNode = self.scene.find(lightstring)
            #lightNode.setColor(1,1,1,.5)
            slnp = render.attachNewNode(slight)
            slnp.setPos(lightNode.getPos(render))
            slnp.setP(-90)
            #slnp.lookAt(Point3(0,0,0))
            render.setLight(slnp)
            #slnp.setColor(1,0,0,0)
            
            self.slightList.append(slight)
            self.slnpList.append(slnp)
        
        #self.slightList[0].setColor(Vec4(1,0,0,1))
        self.scene.find("**/grime1").setColor(1,1,1,.45)
        self.scene.find("**/grime1").setAttrib(CullFaceAttrib.make(CullFaceAttrib.MCullNone))
        self.scene.find("**/blood3").setDepthWrite(False)
        #base.camera.setPos()

        
        #self.plight.setAttenuation(Point3(.7, .7, 0.7))

        
        self.scene.setShaderAuto()

        base.disableMouse()

        #render.ls()
        self.endImage = OnscreenImage(image = 'Art/textures/mission3_plane.png',
                                        scale = 2,
                                        color = (0, 0, 0, 1))
        self.endImage.reparentTo(aspect2d)
        self.endImage.setTransparency(TransparencyAttrib.MAlpha)
        self.endImage.hide()
        
        #-----Load Audio-----#
        messenger.send("addVoice", [ "john-1","Art/audio/cutscene/John - 01.mp3"])
        messenger.send("addVoice", [ "john-2","Art/audio/cutscene/John - 02.mp3"])
        messenger.send("addVoice", [ "john-3","Art/audio/cutscene/John - 03.mp3"])
        messenger.send("addVoice", [ "john-4","Art/audio/cutscene/John - 04.mp3"])
        messenger.send("addVoice", [ "john-5","Art/audio/cutscene/John - 05.mp3"])
        messenger.send("addVoice", [ "john-6","Art/audio/cutscene/John - 06.mp3"])
        messenger.send("addVoice", [ "john-7","Art/audio/cutscene/John - 07.mp3"])
        messenger.send("addVoice", [ "john-8","Art/audio/cutscene/John - 08.mp3"])
        messenger.send("addVoice", [ "john-9","Art/audio/cutscene/John - 09.mp3"])
        messenger.send("addVoice", [ "john-10","Art/audio/cutscene/John - 10.mp3"])
        messenger.send("addVoice", [ "john-11","Art/audio/cutscene/John - 11.mp3"])
        messenger.send("addVoice", [ "john-12","Art/audio/cutscene/John - 12.mp3"])
        messenger.send("addVoice", [ "john-13","Art/audio/cutscene/John - 13.mp3"])
        
        messenger.send("addVoice", [ "steve-1","Art/audio/cutscene/Steve - 01.mp3"])
        messenger.send("addVoice", [ "steve-2","Art/audio/cutscene/Steve - 02.mp3"])
        messenger.send("addVoice", [ "steve-3","Art/audio/cutscene/Steve - 03.mp3"])
        messenger.send("addVoice", [ "steve-4","Art/audio/cutscene/Steve - 04.mp3"])
        messenger.send("addVoice", [ "steve-5","Art/audio/cutscene/Steve - 05.mp3"])
        messenger.send("addVoice", [ "steve-6","Art/audio/cutscene/Steve - 06.mp3"])
        messenger.send("addVoice", [ "steve-7","Art/audio/cutscene/Steve - 07.mp3"])
        messenger.send("addVoice", [ "steve-8","Art/audio/cutscene/Steve - 08.mp3"])
        messenger.send("addVoice", [ "steve-9","Art/audio/cutscene/Steve - 09.mp3"])
        messenger.send("addVoice", [ "steve-10","Art/audio/cutscene/Steve - 10.mp3"])
        messenger.send("addVoice", [ "steve-11","Art/audio/cutscene/Steve - 11.mp3"])
        messenger.send("addVoice", [ "steve-12","Art/audio/cutscene/Steve - 12.mp3"])
        messenger.send("addVoice", [ "steve-13","Art/audio/cutscene/Steve - 13.mp3"])
        messenger.send("addVoice", [ "steve-14","Art/audio/cutscene/Steve - 14.mp3"])
        messenger.send("addVoice", [ "steve-15","Art/audio/cutscene/Steve - 15.mp3"])
        messenger.send("addVoice", [ "steve-16","Art/audio/cutscene/Steve - 16.mp3"])
        
        messenger.send("addSfx", ["cutscene-1","Art/audio/cutscene/Water Drips.mp3"])
        messenger.send("addSfx", ["cutscene-2","Art/audio/cutscene/Rattling Vent.mp3"])
        messenger.send("addSfx", ["cutscene-3","Art/audio/cutscene/Explosion Sequence.mp3"])
        messenger.send("addSfx", ["cutscene-4","Art/audio/cutscene/Death & Pain.mp3"])
        messenger.send("addSfx", ["cutscene-5","Art/audio/cutscene/Construction Bangs.mp3"])
        
        self.setupIntervals()
    def escape(self):
        #for x in self.slightList:
        #    render.clearLight(x)
        #for x in self.slnpList:
        #    x.removeNode()
        #
        #self.slightList = []
        #self.slnpList = []
        #self.dlight.setSpecularColor(Vec4(1,0,0,1))
        #for x in self.slightList:
            #x.setSpecularColor(Vec4(1,0,0,1))
        #pCube3
        for x in self.slightList:
            x.setColor(Vec4(1,0,0,1))
        self.dlight.setColor(Vec4(1,0,0,1))
        
        
    def setupIntervals(self):
        
        messenger.send("loopSfx", ["cutscene-1"])
        messenger.send("loopSfx", ["cutscene-2"])
        messenger.send("playSfx", ["cutscene-1"])
        messenger.send("playSfx", ["cutscene-2"])
        #messenger.send("loopSfx", ["cutscene-1"])
        
        #render.clearLight(self.slnpList[0])
        base.camera.setPos(self.scene.find("**/start").getPos(render))
        base.camera.setHpr(0,-90,90)
        base.camLens.setFov(100)
        self.sequence = Sequence()
        self.sequence.append(Func(self.endImage.show))
        self.sequence.append(Wait(2.0))
        self.sequence.append(LerpColorInterval(self.endImage,
                                6,
                                Vec4(0, 0, 0, 0),
                                Vec4(0, 0, 0, 1)))
        self.sequence.append(Func(self.endImage.hide))
        self.sequence.append(Func(messenger.send, 'playVoice', ['john-1']))
        self.sequence.append(Wait(1.5))
        self.sequence.append(Parallel(LerpPosInterval(base.camera, 6,
                                                      self.scene.find("**/pos1").getPos(render),
                                                      base.camera.getPos(render)),
                                      LerpHprInterval(base.camera, 3.5,
                                                      Vec3(0,0,0),
                                                      Vec3(0,-90,90))))
        self.sequence.append(LerpHprInterval(base.camera, 1.5,
                                             Vec3(55,0,0),
                                             Vec3(0,0,0)))
        self.sequence.append(Wait(.35))
        self.sequence.append(LerpHprInterval(base.camera, 1.5,
                                             Vec3(0,0,0),
                                             Vec3(55,0,0)))
        self.sequence.append(LerpHprInterval(base.camera, 1.5,
                                             Vec3(-50,-20,0),
                                             Vec3(0,0,0)))
        self.sequence.append(Wait(1.5))
        self.sequence.append(Func(messenger.send, 'playVoice', ['john-2']))
        self.sequence.append(Parallel(LerpPosInterval(base.camera, 3,
                                            self.scene.find("**/pos2").getPos(render) + Point3(4,7,0),
                                            self.scene.find("**/pos1").getPos(render)),
                                      LerpHprInterval(base.camera, 1,
                                             Vec3(0,0,0),
                                             Vec3(-50,-20,0))))
        self.sequence.append(LerpHprInterval(base.camera, .75,
                                             Vec3(55,-25,0),
                                             Vec3(0,0,0)))
        self.sequence.append(LerpHprInterval(base.camera, .5,
                                             Vec3(0,0,0),
                                             Vec3(55,-25,0)))
        #self.sequence.append(LerpHprInterval(base.camera, .75,
        #                                     Vec3(-55,0,0),
        #                                     Vec3(0,0,0)))
        #self.sequence.append(LerpHprInterval(base.camera, .75,
        #                                     Vec3(0,0,0),
        #                                     Vec3(-55,0,0)))
        #self.sequence.append(LerpHprInterval(base.camera, .75,
        #                                     Vec3(55,0,0),
        #                                     Vec3(0,0,0)))
        #self.sequence.append(LerpHprInterval(base.camera, .75,
        #                                     Vec3(0,0,0),
        #                                     Vec3(55,0,0)))
        self.sequence.append(LerpHprInterval(base.camera, 4,
                                             Vec3(-70,-20,0),
                                             Vec3(0,0,0)))
        self.sequence.append(LerpHprInterval(base.camera, 2.5,
                                             Vec3(-55,0,0),
                                             Vec3(-70,-20,0)))
        #self.sequence.append(Wait(.3))
        self.sequence.append(Func(messenger.send, 'playVoice', ['steve-1']))
        self.sequence.append(LerpHprInterval(base.camera, 3,
                                             Vec3(-70,-10,0),
                                             Vec3(-55,0,0)))
        #self.sequence.append(LerpHprInterval(base.camera, 1.5,
        #                                     Vec3(-70,20,0),
        #                                     Vec3(-70,-10,0)))
        #self.sequence.append(LerpHprInterval(base.camera, 1.5,
        #                                     Vec3(-70,0,0),
        #                                     Vec3(-70,20,0)))
        self.sequence.append(LerpHprInterval(base.camera, 2.3,
                                             Vec3(-60,0,0),
                                             Vec3(-70,-10,0)))
        self.sequence.append(Func(messenger.send, 'playVoice', ['john-3']))
        self.sequence.append(Wait(2))
        self.sequence.append(Func(messenger.send, 'playVoice', ['steve-2']))
        self.sequence.append(Wait(4))
        self.sequence.append(Parallel(LerpHprInterval(base.camera, 5,
                                             Vec3(-60,-40,0),
                                             Vec3(-60,0,0)),
                                      Func(messenger.send, 'playVoice', ['john-4'])))
        self.sequence.append(Func(messenger.send, 'playVoice', ['john-5']))
        self.sequence.append(LerpHprInterval(base.camera, 2,
                                             Vec3(-60,0,0),
                                             Vec3(-60,-40,0)))
        self.sequence.append(Wait(2))
        self.sequence.append(Func(messenger.send, 'playVoice', ['steve-3']))
        self.sequence.append(LerpHprInterval(base.camera, 5,
                                             Vec3(-70,0,0),
                                             Vec3(-60,0,0)))
        self.sequence.append(LerpHprInterval(base.camera, 4,
                                             Vec3(-60,-10,0),
                                             Vec3(-70,0,0)))
        self.sequence.append(Func(messenger.send, 'playVoice', ['steve-4']))
        self.sequence.append(Parallel(LerpPosInterval(base.camera, 5,
                                             self.scene.find("**/pos3").getPos(render),
                                             self.scene.find("**/pos2").getPos(render) + Point3(4,7,0)),
                                      LerpHprInterval(base.camera, 2,
                                            Vec3(-200,-15,0),
                                            Vec3(-60,-10,0))))
        self.sequence.append(Func(messenger.send, 'playVoice', ['john-6']))
        self.sequence.append(LerpHprInterval(base.camera, 2,
                                             Vec3(-50,0,0),
                                             Vec3(-200,-15,0)))
        #self.sequence.append(LerpHprInterval(base.camera, 3,
        #                                     Vec3(0,-30,0),
        #                                     Vec3(0,-50,0)))
        self.sequence.append(Wait(4))
        self.sequence.append(Func(messenger.send, 'playVoice', ['steve-5']))
        self.sequence.append(LerpHprInterval(base.camera, 4.6,
                                             Vec3(-50,-20,0),
                                             Vec3(-50,0,0)))
        #self.sequence.append(Wait(1.5))
        self.sequence.append(Func(messenger.send, 'playVoice', ['steve-6']))
        self.sequence.append(Wait(4))
        #self.sequence.append(LerpHprInterval(base.camera, 4,
        #                                     Vec3(0,-30,0),
        #                                     Vec3(-50,-20,0)))
        self.sequence.append(Func(messenger.send, 'playVoice', ['steve-7']))
        #self.sequence.append(LerpHprInterval(base.camera, 5,
        #                                     Vec3(-55,-30,0),
        #                                     Vec3(0,-30,0)))
        self.sequence.append(Wait(10))
        self.sequence.append(Func(messenger.send, 'playVoice', ['steve-8']))
        self.sequence.append(Wait(2))
        self.sequence.append(LerpHprInterval(base.camera, 2.2,
                                             Vec3(-50,0,0),
                                             Vec3(-50,-20,0)))
        self.sequence.append(Func(messenger.send, 'playVoice', ['john-7']))
        self.sequence.append(Wait(2.7))
        self.sequence.append(Func(messenger.send, 'playVoice', ['steve-9']))
        self.sequence.append(Wait(13))
        self.sequence.append(Func(messenger.send, 'playVoice', ['john-8']))
        self.sequence.append(Wait(3))
        self.sequence.append(Func(messenger.send, 'playVoice', ['steve-10']))
        self.sequence.append(LerpHprInterval(base.camera, 2,
                                             Vec3(-55,-10,0),
                                             Vec3(-50,0,0)))
        self.sequence.append(Wait(6))
        self.sequence.append(Func(messenger.send, 'playVoice', ['steve-11']))
        self.sequence.append(Wait(3))
        self.sequence.append(Func(messenger.send, 'playVoice', ['john-9']))
        self.sequence.append(Wait(4.4))
        self.sequence.append(Parallel(Func(messenger.send, 'playVoice', ['steve-12']),
                                      LerpHprInterval(base.camera, 6,
                                             Vec3(-50,5,0),
                                             Vec3(-55,-10,0))))
        self.sequence.append(Wait(11))
        self.sequence.append(Func(messenger.send, 'playVoice', ['john-10']))
        self.sequence.append(Wait(3))
        self.sequence.append(Func(messenger.send, 'playVoice', ['steve-13']))
        self.sequence.append(Wait(9))
        self.sequence.append(Func(messenger.send, 'playVoice', ['john-11']))
        self.sequence.append(Wait(3))
        self.sequence.append(Func(messenger.send, 'playVoice', ['steve-14']))
        self.sequence.append(LerpHprInterval(base.camera, 3.5,
                                             Vec3(-40,10,0),
                                             Vec3(-50,5,0)))
        self.sequence.append(Wait(3))
        self.sequence.append(Func(messenger.send, 'playSfx', ['cutscene-3']))
        self.sequence.append(Func(self.escape))
        self.sequence.append(Wait(1.5))
        self.sequence.append(Parallel(Func(messenger.send, 'playVoice', ['steve-15']),
                                      LerpPosInterval(self.door, 2,
                                                      self.door.getPos(render) + Vec3(5,0,0),
                                                      self.door.getPos(render))))
        self.sequence.append(Func(self.endImage.show))
        #self.sequence.append(Wait(1.0))
        self.sequence.append(Parallel(LerpColorInterval(self.endImage,
                                                    3,
                                                    Vec4(0, 0, 0, 1),
                                                    Vec4(0, 0, 0, 0)),
                                      LerpPosInterval(base.camera, 3,
                                                      self.scene.find("**/pos4").getPos(render),
                                                      self.scene.find("**/pos3").getPos(render)),
                                      LerpHprInterval(base.camera, 3,
                                                      Vec3(-30,0,0),
                                                      Vec3(-40,10,0))))
        self.sequence.append(Func(self.preCleanUp))
                                                       

        self.sequence.start()
        #self.sequence.append()
    def preCleanUp(self):
        render.clearLight(self.dlnp)
        render.clearLight(self.alnp)
        for x in self.slnpList:
            render.clearLight(x)
        self.dlnp.removeNode()
        self.alnp.removeNode()
        del self.slightList
        for x in self.slnpList:
            del x
        del self.slnpList
        self.cutSceneNode.removeNode()
            
        