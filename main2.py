#!/usr/bin/env python
from pandac.PandaModules import *
from pandac.PandaModules import loadPrcFileData
from direct.gui.OnscreenImage import OnscreenImage
from direct.interval.IntervalGlobal import *

from CutScene import *

loadPrcFileData("", "show-frame-rate-meter #t")


import direct.directbase.DirectStart

x = CutScene()
run()

