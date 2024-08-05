from .environment import environment
from .basic_actions import Action

#**************************************
# Base class for gamepad based actions
#**************************************
class GamepadAction(Action):
    def __init__(self, keys):
        Action.__init__(self)
        self._keys = []
        if keys != None:
            # append or extend (both are valid)
            if isinstance(keys, list):
                self._keys.extend(keys)
            else:
                self._keys.append(keys)
        self._duration = 0.035
        self._time = 0
        self._needUpdate = False
    
    def setKeyDown(self):
        global vrToGamepad
        for key in self._keys:
            environment.vigem.SetButtonState(environment.vrToGamepad.controller, key, True)
        
    def setKeyUp(self):
        global vrToGamepad
        for key in self._keys:
            environment.vigem.SetButtonState(environment.vrToGamepad.controller, key, False) 

#**********************************************************
# Action class to press and releases a key when "entering"
# vigem has no pressed state, so it has to be active for a
# short duration instead.
#**********************************************************
class GamepadQuickPress(GamepadAction):
    def __init__(self, keys):
        GamepadAction.__init__(self, keys)
        
    def enter(self, currentTime, fromVoiceRecognition):
        # set the keys down
        self.setKeyDown()
        # start the update timer to auto release when from voice activation
        self._time = currentTime
        self._needUpdate = True
            
    def update(self, currentTime):
        if self._needUpdate:
            # determine if we should stop pressing the keys
            if (currentTime - self._time) >= self._duration:
                self.leave()

    def leave(self):
        self.setKeyUp()
        self._needUpdate = False

    def reset(self):
        self.leave()

#****************************************************************************************
# Action class to handle press a key when entering and holding until it leaves a gesture 
#****************************************************************************************
class GamepadPress(GamepadAction):
    def __init__(self, keys):
        GamepadAction.__init__(self, keys)
        
    def enter(self, currentTime, fromVoiceRecognition):
        # set the keys down
        self.setKeyDown()
        # start the update timer to auto release when from voice activation
        self._time = currentTime
        self._needUpdate = fromVoiceRecognition
            
    def update(self, currentTime):
        if self._needUpdate:
            # determine if we should stop pressing the keys
            if (currentTime - self._time) >= self._duration:
                self.leave()

    def leave(self):
        self.setKeyUp()
        self._needUpdate = False

    def reset(self):
        self.leave()

#*******************************************************
# Action class to press a key when entering and leaving 
#*******************************************************
class GamepadToggle(GamepadAction):
    def __init__(self, keys):
        GamepadAction.__init__(self, keys)
        
    def enter(self, currentTime, fromVoiceRecognition):
        self.setKeyPressed()
            
    def leave(self):
        self.setKeyPressed()

#*********************************************************
# Action class to change the state of a key when entering 
#*********************************************************
class GamepadSwitchState(GamepadAction):
    def __init__(self, keys):
        GamepadAction.__init__(self, keys)
        self._down = False
        
    def enter(self, currentTime, fromVoiceRecognition):
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
class GamepadSetState(GamepadAction):
    def __init__(self, keys, state):
        GamepadAction.__init__(self, keys)
        self.stateToSet = state

    def enter(self, currentTime, fromVoiceRecognition):
        if self.stateToSet:
            self.setKeyDown()
        else:
            self.setKeyUp()