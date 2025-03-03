#*******************************************
# Base class to handle gesture/voice action
#*******************************************
class Action:
    def __init__(self):        
        self.haptics = None

    def getCurrentHaptics(self):
        return self.haptics

    def enter(self, currentTime):
        pass
    
    def update(self, currentTime):
        pass
    
    def leave(self):
        pass
    
    def reset(self):
        pass

#*****************************************************
# Special class to combine multiple different actions
#*****************************************************
class MultiAction(Action):
    def __init__(self, actions):
        Action.__init__(self)
        self._actions = actions
       
    def getCurrentHaptics(self):
        for action in self._actions:
            haptics = action.getCurrentHaptics()
            if haptics != None:
                return haptics                
        return self.haptics
        
    def enter(self, currentTime):
        for action in self._actions:
            action.enter(currentTime)
    
    def update(self, currentTime):
        for action in self._actions:
            action.update(currentTime)
    
    def leave(self):
        for action in self._actions:
            action.leave()
    
    def reset(self):
        for action in self._actions:
            action.reset()

#**************************************************************************************************************
# Action class to separate enter and leave to assign individual actions (from which enter and leave is called)
#**************************************************************************************************************
class ActionSplit(Action):
    def __init__(self, actions):
        Action.__init__(self)
        self._actions = actions
        self._inAction = False
        self._lastTime = 0
    
    def getCurrentHaptics(self):
        haptics = None
        if self._inAction:
            haptics = self._actions[1].getCurrentHaptics()
        else:
            haptics = self._actions[0].getCurrentHaptics()
            
        if haptics != None:
            return haptics
        return self.haptics
        
    def enter(self, currentTime):
        self._actions[0].enter(currentTime)
        self._actions[0].leave()
        self._inAction = True
        self._lastTime = currentTime
        
    def update(self, currentTime):
        self._lastTime = currentTime
            
    def leave(self):
        self._actions[1].enter(self._lastTime)
        self._actions[1].leave()
        self._inAction = False

    def reset(self):
        for action in self._actions:
            action.reset()
        self._inAction = False