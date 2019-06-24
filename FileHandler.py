from direct.showbase import DirectObject

import pickle
import sys

class FileHandler(DirectObject.DirectObject):
    def __init__(self, currentSlot = "slotOne"):
        self.currentSlot = currentSlot

        self.accept("modifySlot", self.modifyCurrentSlot)
        self.accept("setCurrentSlot", self.setCurrentSlot)

    def setCurrentSlot(self, slotName):
        assert(slotName == "slotOne" or slotName == "slotTwo" or slotName == "slotThree")
        self.currentSlot = slotName

    def modifyCurrentSlot(self, data): #data is a list
        assert(type(data) == list)
        if self.currentSlot == "slotOne":
            slotOne = open('./saveInfo/slotOne', 'w')
            pickle.dump(data, slotOne)
            slotOne.close()

        elif self.currentSlot == "slotTwo":
            slotTwo = open('./saveInfo/slotTwo', 'w')
            pickle.dump(data, slotTwo)
            slotTwo.close()

        elif self.currentSlot == "slotThree":
            slotThree = open('./saveInfo/slotThree', 'w')
            pickle.dump(data, slotThree)
            slotThree.close()

        else:
            pass

    def getSlotData(self): #Get data from current slot
        slot = open('./saveInfo/' + self.currentSlot, 'r')
        slotData = pickle.load(slot)
        slot.close()
        return slotData

    def cleanUp(self):
        self.ignoreAll()
