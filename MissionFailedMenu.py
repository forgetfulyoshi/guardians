from direct.showbase import DirectObject
from pandac.PandaModules import *
from direct.gui.DirectGui import *

import sys

class MissionFailedMenu(DirectObject.DirectObject):
    def __init__(self):

        self.menuFont = loader.loadFont("Art/fonts/space_age.ttf")
        self.inGameMenuGeom = loader.loadModel("Art/gamemenu.bam")
        
        
      
        self.frame = DirectFrame(image = "Art/textures/gamemenu_bg.png",
                                    scale = (1, 1, .6),
                                    )
        
        #Set up In Game Menu buttons
        #----------------------------------------------------------------------
        self.tryAgainButton = DirectButton(geom = (self.inGameMenuGeom.find('**/button_normal'),
                                                self.inGameMenuGeom.find('**/button_click'),
                                                self.inGameMenuGeom.find('**/button_over'),
                                                self.inGameMenuGeom.find('**/button_normal')),
                                            command = self.restart,
                                            scale = (.4, 1, .1),
                                            pos = (-.50, 0, -.40),
                                            relief = None
                                            )
        self.tryAgainButton.reparentTo(self.frame)
        
        self.exitToMenuButton = DirectButton(geom = (self.inGameMenuGeom.find('**/button_normal'),
                                                self.inGameMenuGeom.find('**/button_click'),
                                                self.inGameMenuGeom.find('**/button_over'),
                                                self.inGameMenuGeom.find('**/button_normal')),
                                                command = self.exitToMenu,
                                                scale = (.4, 1, .1),
                                                pos = (.50, 0, -.40),
                                                relief = None
                                                )
        self.exitToMenuButton.reparentTo(self.frame)
        #----------------------------------------------------------------------
        
        #Set up In Game Menu text
        #----------------------------------------------------------------------
        self.missionFailedText = OnscreenText(text = "Mission Failed",
                                                pos = (0, .3, 0),
                                                scale = .18,
                                                font = self.menuFont,
                                                fg = (1, 1, 1, 1))
        self.missionFailedText.reparentTo(self.frame)
        self.explanationText = OnscreenText(text = '',
                                            pos = (0, 0, 0),
                                            scale = .12,
                                            font = self.menuFont,
                                            mayChange = 1,
                                            fg = (1, 1, 1, 1))
        self.explanationText.reparentTo(self.frame)
        
        self.resumeText = OnscreenText(text = "Exit To Menu",
                                        pos = (.50, -.40, 0),
                                        font = self.menuFont)
        self.resumeText.reparentTo(self.frame)
        
        self.restartText = OnscreenText(text = "Try Again",
                                        pos = (-.50, -.40, 0),
                                        font = self.menuFont)
        self.restartText.reparentTo(self.frame)
        #----------------------------------------------------------------------
        self.frame.hide()
        
       
    def display(self, text):        
        props = WindowProperties()
        props.setCursorHidden(False)
        base.win.requestProperties(props)
        taskMgr.remove('moveStick')
        self.explanationText['text'] = text
        self.frame.show()
            
    def restart(self):
        self.frame.hide()
        messenger.send('missionfailedrestart')
        
    def exitToMenu(self):
        self.frame.hide()
        messenger.send('missionfailedexittomenu')