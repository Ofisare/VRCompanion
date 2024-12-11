from .environment import environment
from .basic_actions import Action

#**********************************
# Base class for key based actions
#**********************************
class KeyAction(Action):
    def __init__(self, keys):
        Action.__init__(self)
        self._keys = []
        if keys != None:
            # append or extend (both are valid)
            if isinstance(keys, list):
                self._keys.extend(keys)
            else:
                self._keys.append(keys)
        
    def setKeyDown(self):
        for key in self._keys:
            environment.keyboard.setKey(key, True)
        
    def setKeyUp(self):
        for key in self._keys:
            environment.keyboard.setKey(key, False)
    
    def setKeyPressed(self):
        for key in self._keys:
            environment.keyboard.tapKey(key)

#********************************************************
# Action class to press and releases a key when entering
#********************************************************
class KeyQuickPress(KeyAction):
    def __init__(self, keys):
        KeyAction.__init__(self, keys)
        
    def enter(self, currentTime):
        self.setKeyPressed()

#****************************************************************************************
# Action class to handle press a key when entering and holding until it leaves a gesture 
#****************************************************************************************
class KeyPress(KeyAction):
    def __init__(self, keys):
        KeyAction.__init__(self, keys)
        
    def enter(self, currentTime):
        # set the keys down
        self.setKeyDown()
        
    def leave(self):
        self.setKeyUp()
        
    def reset(self):
        self.leave()

#*******************************************************
# Action class to press a key when entering and leaving 
#*******************************************************
class KeyToggle(KeyAction):
    def __init__(self, keys):
        KeyAction.__init__(self, keys)
        
    def enter(self, currentTime, fromVoiceRecognition):
        self.setKeyPressed()
        
    def leave(self):
        self.setKeyPressed()
        
#*********************************************************
# Action class to change the state of a key when entering 
#*********************************************************
class KeySwitchState(KeyAction):
    def __init__(self, keys):
        KeyAction.__init__(self, keys)
        self._down = False
        
    def enter(self, currentTime):
        if self._down:
            self.setKeyUp()
            self._down = False
        else:
            self.setKeyDown()
            self._down = True
    
    def reset(self):
        self.setKeyUp()
        self._down = False
        
#******************************************************
# Action class to set the state of a key when entering 
#******************************************************
class KeySetState(KeyAction):
    def __init__(self, keys, state):
        KeyAction.__init__(self, keys)
        self.stateToSet = state

    def enter(self, currentTime):
        if self.stateToSet:
            self.setKeyDown()
        else:
            self.setKeyUp()