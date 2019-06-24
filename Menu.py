from direct.showbase import DirectObject
from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.fsm import FSM
import config

import pickle
import sys


class MainMenu(DirectObject.DirectObject, FSM.FSM):
    def __init__(self, soundHandler):
        self.difficulty = 0
        FSM.FSM.__init__(self,'menuFSM')
        self.defaultTransitions = {
            'Main' : [ 'NewGame', 'LoadGame', 'Options' ],
            'NewGame' : [ 'Main' ],
            'LoadGame' : [ 'Main' ],
            'Options' : [ 'Main' ],
            }

        self.menuFont = loader.loadFont("Art/fonts/space_age.ttf")
        self.soundHandler = soundHandler

        self.setupBackgroundScene()
        self.request('Main')
        self.requestedZone = 0

        #Set up Options
        #----------------------------------------------------------------------
        #this value must be higher than the possible value
        #in the radio buttons or the command for the respective value will be called
        #messenger.send("setVoiceVolume", [100])
        #messender.send("setSfxVolume", [100])
        #----------------------------------------------------------------------

        #Open saved info
        #----------------------------------------------------------------------
        slotOne = open('./saveInfo/slotOne', 'r')
        self.slotOneList = pickle.load(slotOne)
        slotOne.close()
        slotTwo = open('./saveInfo/slotTwo', 'r')
        self.slotTwoList = pickle.load(slotTwo)
        slotTwo.close()
        slotThree = open('./saveInfo/slotThree', 'r')
        self.slotThreeList = pickle.load(slotThree)
        slotThree.close()
        optionsFile = open('./saveInfo/options', 'r')
        self.optionsList = pickle.load(optionsFile)
        print self.optionsList
        optionsFile.close()
        #----------------------------------------------------------------------


    def setupBackgroundScene(self):
        #props = base.win.getProperties()
        #props = WindowProperties(base.win.getProperties())
        #props.setFullscreen(True)
        alight = AmbientLight('alight')
        alight.setColor(VBase4(1,1,1,1))

        self.capitalShip = loader.loadModel("Art/cap1.bam")
        self.menu = loader.loadModel("Art/mainmenu_buttons.egg")
        self.skybox = loader.loadModel("Art/backbox.bam")
        self.solarsystem = loader.loadModel("Art/solarsystem.bam")

        self.soundHandler.addMusic("menuBackgroundMusic", "Art/audio/DJ Quicksilver - Aebisc Song.mp3")
        self.soundHandler.setMusicVolume(0.7)
        self.soundHandler.playMusic("menuBackgroundMusic")

        ###
        #Set up the Solar System and background stuffs
        ###
        self.solarsystem.reparentTo(render)
        planetlist = self.solarsystem.find("**/system")
        planetlist = planetlist.getChildrenAsList()
        for x in planetlist:
            x.hide()

        self.earth = self.solarsystem.find("**/earth*")
        self.earth.show()
        self.earth.setPos(self.earth, -1.4,2,.4) #Due to the offset in the mayaModel
        self.earth.setScale(1)
        self.earth.getChild(0).setP(180)
        self.earth.getChild(1).reparentTo(self.earth.getChild(0))
        self.earth.getChild(0).getChild(1).setScale(.5)

        tex2 = loader.loadTexture('Art/textures/earthlights1k.jpg')
        ts = TextureStage('ts')
        self.earth.setTexture(ts, tex2)
        self.earth.setScale(1.33)

        #self.earth.ls()

        self.rotationSeq = Sequence()
        self.rotationSeq.append(LerpHprInterval(self.earth.getChild(0), 130, Vec3(360,0,0), Vec3(0,0,0)))

        self.rotationSeq.loop()

        #Debug, Will put you back so you can view everything
        #base.camera.setPos(20,0,0)
        #base.camera.setHpr(90,0,0)

        base.camera.setPos(4,0,0)
        base.camera.setHpr(80,10,0)
        #####End of Background movement######


        self.menu.setAttrib(CullFaceAttrib.make(CullFaceAttrib.MCullNone))
        self.skybox.setAttrib(CullFaceAttrib.make(CullFaceAttrib.MCullNone))
        alnp = self.skybox.attachNewNode(alight)
        self.skybox.setLight(alnp)

        self.skybox.reparentTo(render)
        self.skybox.setScale(100)
        self.skybox.setHpr(20,2,20)


    def enterMain(self):
        self.buttonsNode = NodePath('buttonsNode')
        self.buttonsNode.reparentTo(aspect2d)
        self.buttonsNode.setX(-.2)
        self.resolutionSelect = [5]

        # Set up Main Menu Buttons
        #-------------------------------------------------------------------------------
        self.buttonOne = DirectButton(geom = (self.menu.find('**/one_normal'),
                                                  self.menu.find('**/one_clicked'),
                                                  self.menu.find('**/one_over'),
                                                  self.menu.find('**/one_normal')),
                                        scale = (1, 1, .2),
                                        pos = (-1, 0, 0),
                                        relief = None,
                                        command = self.request,
                                        extraArgs = ['NewGame'],
                                        #text = "New",
                                        #text_scale = 0.25,
                                        #text_pos = (.08, 0)
                                        )
        self.buttonOne.reparentTo(self.buttonsNode)

        self.buttonTwo = DirectButton(geom = (self.menu.find('**/two_normal'),
                                                 self.menu.find('**/two_clicked'),
                                                 self.menu.find('**/two_over'),
                                                 self.menu.find('**/two_normal')),
                                         scale = (1.1, 1, .2),
                                         pos = (-.79, 0, -.19),
                                         relief = None,
                                         command = self.request,
                                         extraArgs = ['LoadGame'],
                                        #text = "Load Game",
                                        #text_scale = 0.25,
                                        #text_pos = (.08, 0)
                                         )
        self.buttonTwo.reparentTo(self.buttonsNode)

        self.buttonThree = DirectButton(geom = (self.menu.find('**/three_normal'),
                                                   self.menu.find('**/three_clicked'),
                                                   self.menu.find('**/three_over'),
                                                   self.menu.find('**/three_normal')),
                                           scale = (1.35, 1, .2),
                                           pos = (-.66, 0, -.38),
                                           relief = None,
                                           command = self.request,
                                           extraArgs = ['Options'],
                                        #text = "Options",
                                        #text_scale = 0.25,
                                        #text_pos = (.08, 0)
                                           )
        self.buttonThree.reparentTo(self.buttonsNode)

        self.buttonFour = DirectButton(geom = (self.menu.find('**/four_normal'),
                                               self.menu.find('**/four_clicked'),
                                               self.menu.find('**/four_over'),
                                               self.menu.find('**/four_normal')),
                                       scale = (1.55, 1, .2),
                                       pos = (-.52, 0, -.57),
                                       relief = None,
                                       command = exit,
                                    #text = "Quit",
                                    #text_scale = 0.25,
                                    #text_pos = (.08, 0)
                                       )
        self.buttonFour.reparentTo(self.buttonsNode)
        #-----------------------------------------------------------------------------

        #Set up text for Main menu (also used in New Game and Loading Menus)
        #------------------------------------------------------------------------------
        self.buttonText = NodePath('buttonText')
        self.buttonText.reparentTo(self.buttonsNode)
        self.buttonText.setX(-0.85)
        self.buttonText.setZ(-0.02)

        self.buttonOneText = OnscreenText(text = "New",
                                         pos = (0,0,0),
                                         mayChange = True,
                                         font = self.menuFont,
                                         )
        self.buttonOneText.reparentTo(self.buttonText)

        self.buttonTwoText = OnscreenText(text = "Load",
                                         pos = (0,-0.19,0),
                                         mayChange = True,
                                         font = self.menuFont
                                         )
        self.buttonTwoText.reparentTo(self.buttonText)

        self.buttonThreeText = OnscreenText(text = "Options",
                                         pos = (0,-0.38,0),
                                         mayChange = True,
                                         font = self.menuFont,
                                         )
        self.buttonThreeText.reparentTo(self.buttonText)

        self.buttonFourText = OnscreenText(text = "Quit",
                                         pos = (0,-0.57,0),
                                         mayChange = True,
                                         font = self.menuFont,
                                         )
        self.buttonFourText.reparentTo(self.buttonText)

        #------------------------------------------------------------------------------
        #------------------------------------------------------------------------------

    def exitMain(self):
        print "Exited Menu"


    def enterNewGame(self):
        print "Enter New Game"

        if self.slotOneList[0] != '0':
            self.buttonOneText['text'] = "Chapter " + self.slotOneList[0]
            self.buttonOneText.setScale(.065)
            self.buttonOneText['pos'] = (-.05,0,0)
        else:
            self.buttonOneText['text'] = "Empty"
        self.buttonOne['command'] = self.newButtonClicked
        self.buttonOne['extraArgs'] = ['slotOne']

        if self.slotTwoList[0] != '0':
            self.buttonTwoText['text'] = "Chapter " + self.slotTwoList[0]
        else:
            self.buttonTwoText['text'] = "Empty"
        self.buttonTwo['command'] = self.newButtonClicked
        self.buttonTwo['extraArgs'] = ['slotTwo']

        if self.slotThreeList[0] != '0':
            self.buttonThreeText['text'] = "Chapter " + self.slotThreeList[0]
        else:
            self.buttonThreeText['text'] = "Empty"
        self.buttonThree['command'] = self.newButtonClicked
        self.buttonThree['extraArgs'] = ['slotThree']

        self.buttonFourText['text'] = "Main Menu"
        self.buttonFour['command'] = self.request
        self.buttonFour['extraArgs'] = ['Main']

    def exitNewGame(self):
        self.buttonsNode.removeNode()
        print "Exit New Game"

    def enterLoadGame(self):
        print "Enter Load Game"

        if not self.slotOneList[0] == '0':
            self.buttonOneText['text'] = "Chapter " + self.slotOneList[0]
            self.buttonOneText.setScale(.065)
            self.buttonOneText['pos'] = (-.05,0,0)
        else:
            self.buttonOne['state'] = DGG.DISABLED
            self.buttonOneText['text'] = "Empty"
        self.buttonOne['command'] = self.loadGame
        self.buttonOne['extraArgs'] = ['slotOne', self.slotOneList]

        if not self.slotTwoList[0] == '0':
            self.buttonTwoText['text'] = "Chapter " + self.slotTwoList[0]
        else:
            self.buttonTwo['state'] = DGG.DISABLED
            self.buttonTwoText['text'] = "Empty"
        self.buttonTwo['command'] = self.loadGame
        self.buttonTwo['extraArgs'] = ['slotTwo', self.slotTwoList]

        if not self.slotThreeList[0] == '0':
            self.buttonThreeText['text'] = "Chapter " + self.slotThreeList[0]
        else:
            self.buttonThree['state'] = DGG.DISABLED
            self.buttonThreeText['text'] = "Empty"
        self.buttonThree['command'] = self.loadGame
        self.buttonThree['extraArgs'] = ['slotThree', self.slotThreeList]

        self.buttonFourText['text'] = "Main Menu"
        self.buttonFour['command'] = self.request
        self.buttonFour['extraArgs'] = ['Main']

    def exitLoadGame(self):
        self.buttonsNode.removeNode()
        print "Exit Load Game"

    def enterOptions(self):
        print "Enter Options Menu"

        self.buttonsNode.removeNode()

        self.optionsButtons = NodePath('optionsButtons') #Used to group and delete ALL buttons on Options Screen
        self.resolutionButtons = NodePath('radioButtons') #Used to group all labels and buttons pertaining to resolution
        self.volumeButtons = NodePath('volumeButtons') #Used to group all labels and buttons pertainting to volume

        self.optionsButtons.reparentTo(aspect2d)
        self.resolutionButtons.reparentTo(self.optionsButtons)
        self.volumeButtons.reparentTo(self.optionsButtons)

        #Set up resolution modifiers
        #-------------------------------------------------------------------------------------
        self.resolutionButtons.setX(-0.75)
        self.resolutionButtons.setZ(0.4)



        self.resolutionLabel = OnscreenText(text = "Resolution",
                                            pos = (.1,.2,0),
                                            scale = .15,
                                            style = 3,
                                            font = self.menuFont,
                                            )
        self.resolutionLabel.reparentTo(self.resolutionButtons)

        self.resolutionChangeLowest = DirectRadioButton(
                                                    #boxGeom = self.menu.find('**/radio_fg'),
                                                    #boxImage = self.menu.find('**/radio_bg'),
                                                    variable = self.resolutionSelect,
                                                    value = [0],
                                                    relief = None,
                                                    scale = 0.1,
                                                    text = '640 x 480',
                                                    pos = (0,0,0),
                                                    command = self.changeResolution,
                                                    extraArgs = ['640', '480', 0],
                                                    text_font = self.menuFont,
                                                    )
        self.resolutionChangeLowest.reparentTo(self.resolutionButtons)

        self.resolutionChangeLow = DirectRadioButton(
                                                    #boxGeom = self.menu.find('**/radio_fg'),
                                                    #boxImage = self.menu.find('**/radio_bg'),
                                                    variable = self.resolutionSelect,
                                                    value = [1],
                                                    relief = None,
                                                    scale = 0.1,
                                                    text = '800 x 600',
                                                    pos = (0,0,-.15),
                                                    command = self.changeResolution,
                                                    extraArgs = ['800', '600', 1],
                                                    text_font = self.menuFont,
                                                    )
        self.resolutionChangeLow.reparentTo(self.resolutionButtons)

        self.resolutionChangeMed = DirectRadioButton(
                                                    #boxGeom = self.menu.find('**/radio_fg'),
                                                    #boxImage = self.menu.find('**/radio_bg'),
                                                    #indicatorValue = 1,
                                                    variable = self.resolutionSelect,
                                                    value = [2],
                                                    relief = None,
                                                    scale = 0.1,
                                                    text = '1024 x 768',
                                                    pos = (.02,0,-.3),
                                                    command = self.changeResolution,
                                                    extraArgs = ['1024', '768', 2],
                                                    text_font = self.menuFont,
                                                    )
        self.resolutionChangeMed.reparentTo(self.resolutionButtons)

        self.resolutionChangeHigh = DirectRadioButton(
                                                    #boxGeom = self.menu.find('**/radio_fg'),
                                                    #boxImage = self.menu.find('**/radio_bg'),
                                                    variable = self.resolutionSelect,
                                                    value = [3],
                                                    relief = None,
                                                    scale = 0.1,
                                                    text = '1280 x 1024',
                                                    pos = (.04,0,-.45),
                                                    command = self.changeResolution,
                                                    extraArgs = ['1280', '1024', 3],
                                                    text_font = self.menuFont,
                                                    )
        self.resolutionChangeHigh.reparentTo(self.resolutionButtons)

        self.resolutionChangeHighest = DirectRadioButton(
                                                    #boxGeom = self.menu.find('**/radio_fg'),
                                                    #boxImage = self.menu.find('**/radio_bg'),
                                                    variable = self.resolutionSelect,
                                                    value = [4],
                                                    relief = None,
                                                    scale = 0.1,
                                                    text = '1600 x 1200',
                                                    pos = (.04,0,-.6),
                                                    command = self.changeResolution,
                                                    extraArgs = ['1600', '1200', 4],
                                                    text_font = self.menuFont,
                                                    )
        self.resolutionChangeHighest.reparentTo(self.resolutionButtons)

        resolutionButtonsList = [self.resolutionChangeLowest,
                                 self.resolutionChangeLow,
                                 self.resolutionChangeMed,
                                 self.resolutionChangeHigh,
                                 self.resolutionChangeHighest]

        for button in resolutionButtonsList:
            button.setOthers(resolutionButtonsList)

        ###Set the right radio button to be true upon initialization
        if self.optionsList[2] == 0:
            self.resolutionChangeLowest['indicatorValue'] = 1
        elif self.optionsList[2] == 1:
            self.resolutionChangeLow['indicatorValue'] = 1
        elif self.optionsList[2] == 2:
            self.resolutionChangeMed['indicatorValue'] = 1
        elif self.optionsList[2] == 3:
            self.resolutionChangeHigh['indicatorValue'] = 1
        elif self.optionsList[2] == 4:
            self.resolutionChangeHighest['indicatorValue'] = 1

        #----------------------------------------------------------------------------------------------

        #Set up volume controls
        #----------------------------------------------------------------------------------------------
        #----------------------------------------------------------------------------------------------
        self.volumeButtons.setX(0.9)
        self.volumeButtons.setZ(0.4)
        self.volumeLabel = OnscreenText(text = "Volume",
                                       pos = (-0.2,.2,0),
                                       scale = 0.15,
                                       style = 3,
                                       font = self.menuFont,
                                      )
        self.volumeLabel.reparentTo(self.volumeButtons)

        #Music Volume
        #----------------------------------------------------------------------------------------------
        self.musicVolumeDown = DirectButton(geom = (self.menu.find('**/arrowleft_normal'),
                                                    self.menu.find('**/arrowleft_clicked'),
                                                    self.menu.find('**/arrowleft_over'),
                                                    self.menu.find('**/arrowleft_normal')),
                                            pos = (-0.2, 0, 0),
                                            scale = 0.15,
                                            relief = None,
                                            command = self.changeMusicVolume,
                                            extraArgs = [-.1],
                                            )
        self.musicVolumeDown.reparentTo(self.volumeButtons)

        self.musicVolumeUp = DirectButton(geom = (self.menu.find('**/arrowright_normal'),
                                                    self.menu.find('**/arrowright_clicked'),
                                                    self.menu.find('**/arrowright_over'),
                                                    self.menu.find('**/arrowright_normal')),
                                          pos = (0.2, 0, 0),
                                          scale = 0.15,
                                          relief = None,
                                          command = self.changeMusicVolume,
                                          extraArgs = [.1]
                                            )
        self.musicVolumeUp.reparentTo(self.volumeButtons)

        self.musicVolumeLabel = OnscreenText(text = str(int(self.soundHandler.getMusicVolume() * 100)),
                                             pos = (0,0,0),
                                             fg = (0,1,0,1),
                                             font = self.menuFont,
                                             mayChange = True,
                                             )
        self.musicVolumeLabel.reparentTo(self.volumeButtons)

        self.musicLabel = OnscreenText(text = "Music",
                                        pos = (-0.5,0,0),
                                        fg = (0,1,0,1),
                                        font = self.menuFont,
                                        )
        self.musicLabel.reparentTo(self.volumeButtons)

        #Voice Volume
        #------------------------------------------------------------------------------------------
        self.voiceVolumeDown = DirectButton(geom = (self.menu.find('**/arrowleft_normal'),
                                                    self.menu.find('**/arrowleft_clicked'),
                                                    self.menu.find('**/arrowleft_over'),
                                                    self.menu.find('**/arrowleft_normal')),
                                            pos = (-0.2, 0, -.2),
                                            scale = 0.15,
                                            relief = None,
                                            command = self.changeVoiceVolume,
                                            extraArgs = [-.1]
                                            )
        self.voiceVolumeDown.reparentTo(self.volumeButtons)

        self.voiceVolumeUp = DirectButton(geom = (self.menu.find('**/arrowright_normal'),
                                                    self.menu.find('**/arrowright_clicked'),
                                                    self.menu.find('**/arrowright_over'),
                                                    self.menu.find('**/arrowright_normal')),
                                          pos = (0.2, 0, -.2),
                                          scale = 0.15,
                                          relief = None,
                                          command = self.changeVoiceVolume,
                                          extraArgs = [.1]
                                            )
        self.voiceVolumeUp.reparentTo(self.volumeButtons)

        self.voiceVolumeLabel = OnscreenText(text = str(int(self.soundHandler.getVoiceVolume() * 100)),
                                             pos = (0,-.2,0),
                                             fg = (0,1,0,1),
                                             font = self.menuFont,
                                             mayChange = True,
                                             )
        self.voiceVolumeLabel.reparentTo(self.volumeButtons)

        self.voiceLabel = OnscreenText(text = "Voice",
                                             pos = (-0.5,-.2,0),
                                             fg = (0,1,0,1),
                                             font = self.menuFont,
                                             )
        self.voiceLabel.reparentTo(self.volumeButtons)


        #Sfx Volume
        #----------------------------------------------------------------------------------------------
        self.sfxVolumeDown = DirectButton(geom = (self.menu.find('**/arrowleft_normal'),
                                                    self.menu.find('**/arrowleft_clicked'),
                                                    self.menu.find('**/arrowleft_over'),
                                                    self.menu.find('**/arrowleft_normal')),
                                            pos = (-0.2, 0, -.4),
                                            scale = 0.15,
                                            relief = None,
                                            command = self.changeSfxVolume,
                                            extraArgs = [-.1]
                                            )
        self.sfxVolumeDown.reparentTo(self.volumeButtons)

        self.sfxVolumeUp = DirectButton(geom = (self.menu.find('**/arrowright_normal'),
                                                    self.menu.find('**/arrowright_clicked'),
                                                    self.menu.find('**/arrowright_over'),
                                                    self.menu.find('**/arrowright_normal')),
                                          pos = (0.2, 0, -.4),
                                          scale = 0.15,
                                          relief = None,
                                          command = self.changeSfxVolume,
                                          extraArgs = [.1]
                                            )
        self.sfxVolumeUp.reparentTo(self.volumeButtons)

        self.sfxVolumeLabel = OnscreenText(text = str(int(self.soundHandler.getSfxVolume() * 100)),
                                             pos = (0,-.4,0),
                                             fg = (0,1,0,1),
                                             font = self.menuFont,
                                            mayChange = True,
                                             )
        self.sfxVolumeLabel.reparentTo(self.volumeButtons)

        self.sfxLabel = OnscreenText(text = "SFX",
                                             pos = (-0.5,-.4,0),
                                             fg = (0,1,0,1),
                                             font = self.menuFont,
                                             )
        self.sfxLabel.reparentTo(self.volumeButtons)

        #-----------------------------------------------------------------------------------------------
        #-----------------------------------------------------------------------------------------------

        #Main Menu Button
        self.menuButton = DirectButton(geom = (self.menu.find('**/four_normal'),
                                               self.menu.find('**/four_clicked'),
                                               self.menu.find('**/four_over'),
                                               self.menu.find('**/four_normal')),
                                        scale = (1.55, 1, .2),
                                        pos = (-.72, 0, -.57),
                                        relief = None,
                                        command = self.request,
                                        extraArgs = ['Main'],
                                        #text = "Main",
                                        #text_scale = 0.25,
                                        #text_pos = (.08, 0)
                                       )
        self.menuButton.reparentTo(self.optionsButtons)

        self.menuButtonText = OnscreenText(text = "Main Menu",
                                         pos = (-.85,-0.59,0),
                                         mayChange = True,
                                         font = self.menuFont,
                                         )
        self.menuButtonText.reparentTo(self.optionsButtons)



        inGameMenuGeom = loader.loadModel("Art/gamemenu.bam")
        self.shaderLabel = OnscreenText(text = "",
                                       pos = (.75,-.25,0),
                                       scale = 0.1,
                                       style = 3,
                                       #fg = (1,1,0,1),
                                       font = self.menuFont,
                                       mayChange = True
                                      )
        if config.wantShaders:
            self.shaderLabel["text"] = "Shaders\n are ON"
        else:
            self.shaderLabel["text"] = "Shaders\n are OFF"
        self.shaderToggle = DirectButton(geom = (inGameMenuGeom.find('**/button_normal'),
                                                inGameMenuGeom.find('**/button_click'),
                                                inGameMenuGeom.find('**/button_over'),
                                                inGameMenuGeom.find('**/button_normal')),
                                            pos = (.75, 0, -.285),
                                            color = (1,1,1,.7),
                                            relief = None,
                                            scale = (.37,.2,.13),
                                            command = self.toggleShaders,
                                            #text = "Toggle Shaders"
                                            )
        self.shaderLabel.reparentTo(aspect2d)
    def toggleShaders(self):
        config.wantShaders = not config.wantShaders
        if config.wantShaders:
            self.shaderLabel["text"] = "Shaders\n are ON"
        else:
            self.shaderLabel["text"] = "Shaders\n are OFF"
        
    def exitOptions(self):
        print "Exit Options Menu"
        self.optionsList[3] = self.soundHandler.getMusicVolume()
        self.optionsList[4] = self.soundHandler.getVoiceVolume()
        self.optionsList[5] = self.soundHandler.getSfxVolume()
        optionsFile = open('./saveInfo/options', 'w')
        pickle.dump(self.optionsList, optionsFile)
        optionsFile.close()
        self.optionsButtons.removeNode()
        self.shaderToggle.removeNode()
        self.shaderLabel.removeNode()

    def changeMusicVolume(self, change):
        #right now this is working for self.backgroundMusic
        print self.soundHandler.getMusicVolume()
        if change == -.1:
            if (self.soundHandler.getMusicVolume()) > 0:
                self.soundHandler.setMusicVolume(self.soundHandler.getMusicVolume() + change)
                self.musicVolumeLabel['text'] = str(int(self.soundHandler.getMusicVolume() * 100))
            else:
                print "CANNOT CHANGE" + str(self.soundHandler.getMusicVolume())
        elif change == .1:
            if (self.soundHandler.getMusicVolume()) < 1:
                self.soundHandler.setMusicVolume(self.soundHandler.getMusicVolume() + change)
                self.musicVolumeLabel['text'] = str(int(self.soundHandler.getMusicVolume() * 100))
            else:
                print "CANNOT CHANGE" + str(self.soundHandler.getMusicVolume())

    def changeVoiceVolume(self, change):
        print self.soundHandler.getVoiceVolume()
        if change == -.1:
            if (self.soundHandler.getVoiceVolume()) > 0:
                self.soundHandler.setVoiceVolume(self.soundHandler.getVoiceVolume() + change)
                self.voiceVolumeLabel['text'] = str(int(self.soundHandler.getVoiceVolume() * 100))
            else:
                print "CANNOT CHANGE" + str(self.soundHandler.getVoiceVolume())
        elif change == .1:
            if (self.soundHandler.getVoiceVolume()) < 1:
                self.soundHandler.setVoiceVolume(self.soundHandler.getVoiceVolume() + change)
                self.voiceVolumeLabel['text'] = str(int(self.soundHandler.getVoiceVolume() * 100))
            else:
                print "CANNOT CHANGE" + str(self.soundHandler.getVoiceVolume())

    def changeSfxVolume(self, change):
        print self.soundHandler.getSfxVolume()
        if change == -.1:
            if (self.soundHandler.getSfxVolume()) > 0:
                self.soundHandler.setSfxVolume(self.soundHandler.getSfxVolume() + change)
                self.sfxVolumeLabel['text'] = str(int(self.soundHandler.getSfxVolume() * 100))
            else:
                print "CANNOT CHANGE" + str(self.soundHandler.getSfxVolume())
        elif change == .1:
            if (self.soundHandler.getSfxVolume()) < 1:
                self.soundHandler.setSfxVolume(self.soundHandler.getSfxVolume() + change)
                self.sfxVolumeLabel['text'] = str(int(self.soundHandler.getSfxVolume() * 100))
            else:
                print "CANNOT CHANGE" + str(self.soundHandler.getSfxVolume())


    def changeResolution(self, HACK, width, height, resSelect):
        #Change Options File to include the new resolution
        #----------------------------------------------------------------------
        print "CHANGE RESOULTION TO: ", width, "x", height
        self.optionsList[0] = width
        self.optionsList[1] = height
        self.optionsList[2] = resSelect
        #----------------------------------------------------------------------

        #Tell user to restart
        #----------------------------------------------------------------------
        optionsWarning = NodePath('Options Warning')
        optionsWarning.reparentTo(self.optionsButtons)
        optionsWarning.setPos(0, 0, -.3)
        optionsWarning1 = OnscreenText(text = "You must restart the game for",
                                   font = self.menuFont,
                                   fg = (1,0,0,1))
        optionsWarning1.reparentTo(optionsWarning)
        optionsWarning2 = OnscreenText(text = "resolution changes to take effect",
                                    font = self.menuFont,
                                    fg = (1,0,0,1),
                                    pos = (0, -.1))
        optionsWarning2.reparentTo(optionsWarning)
        #----------------------------------------------------------------------

    def newButtonClicked(self, slotName):
        messenger.send('setCurrentSlot', [slotName])
        messenger.send('modifySlot', [['0']])
        self.requestedZone = "IntroMovie"
        self.cleanUp()

    def loadGame(self, slotName, slotData):
        messenger.send('setCurrentSlot', [slotName])

        if slotData[0] == '1': self.requestedZone = "ZoneOne"
        if slotData[0] == '2': self.requestedZone = "ZoneTwo"
        if slotData[0] == '3': self.requestedZone = "ZoneThree"
        if slotData[0] == '4': self.requestedZone = "ZoneFour"
        if slotData[0] == '5': self.requestedZone = "ZoneFive"

        self.cleanUp()


    def cleanUp(self):

        self.soundHandler.stopMusic("menuBackgroundMusic")

        #self.shipSequence.finish()
        self.rotationSeq.finish()

        self.buttonsNode.removeNode()

        del self.soundHandler

        self.capitalShip.removeNode()
        self.menu.removeNode()
        self.skybox.removeNode()
        self.solarsystem.removeNode()
        #self.shipNode.removeNode()
        self.earth.removeNode()

        messenger.send("startgame", [self.requestedZone])
