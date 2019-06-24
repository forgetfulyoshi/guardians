#FSM.py
# Created - 9/12/2008
# Programmer - Eric Ranaldi
# FSM - Finite State Machine. 
# A FSM to be used with the next-gen games clients and servers. The aim is to
# make it simple yet with expandability as we need it.

class FSM : 
    
    def default() : pass
    def list() : pass
    currentState = 'default'
    stateList = [default() , list()]
    stateMap = {'default' : stateList }
    #func to add a state to the FSM
    def add(self, stateName, funcList) :
        FSM.stateMap[stateName] = funcList
    #Func to change state to a new state
    def changeState(self, stateName, args = []) :
        #if FSM has not been set yet then enter the requested state 
        #immedietly
        if FSM.currentState == 'default' : 
            FSM.currentState = stateName
            self.temp = FSM.stateMap[FSM.currentState]
            self.temp[0](args)
            
        #if FSM is currently in requested state then simply return    
        elif FSM.currentState == stateName :
            return
       #If FSM is not in the requested state. Then exit current state and
       #enter requested state    
        elif self.currentState != stateName :
            self.temp = FSM.stateMap[FSM.currentState]
            self.temp[1](args)
            FSM.currentState = stateName
            self.temp = FSM.stateMap[FSM.currentState]
            self.temp[0](args)
        
    #for testing purprose to be removed upon completion of testing
    #Prints the complete dict for the FSM
    def showStateMap( self ) :
        print FSM.stateMap


"""
class TestClass : 
    testClassFSM = FSM()
    def EnterPlay(self) : 
        print 'do game stuff'
        print 1+2
        self.testClassFSM.changeState('Menu')
    def ExitPlay(self) : 
        print 'Do CleanupCode - Play'
    def EnterMenu(self) :
        print 'do menu stuff'
        #self.testClassFSM.changeState('Play')
    def ExitMenu(self) : 
        print 'do CleanupCode - Menu'
    def CreateStateList(self) : 
        self.tempFuncList = [self.EnterPlay, self.ExitPlay]
        self.testClassFSM.add('Play', self.tempFuncList)
        self.tempFuncList = [self.EnterMenu, self.ExitMenu]
        self.testClassFSM.add('Menu', self.tempFuncList)
    def startup(self) :
        self.testClassFSM.changeState('Play')

a = TestClass()
a.CreateStateList()
a.startup()
"""