from .environment import environment
from .basic_actions import Action

#************************************
# Base class for mouse based actions
#************************************
class MouseAction(Action):
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
        pass
        for key in self._keys:
            if key == -1:
                environment.mouse.wheelDown = True
            elif key == -2:
                environment.mouse.wheelUp = True
            else:
                environment.mouse.setButton(key, True)
        
    def setKeyUp(self):
        pass
        for key in self._keys:
            if key == -1:
                pass
                #environment.mouse.wheelDown = False
            elif key == -2:
                pass
                #environment.mouse.wheelUp = False
            else:
                environment.mouse.setButton(key, False)
    
    def setKeyPressed(self):
        for key in self._keys:
            if key == -1:
                environment.mouse.wheelDown = True
            elif key == -2:
                environment.mouse.wheelUp = True
            else:
                environment.mouse.setButton(key, True)
                environment.mouse.setButton(key, False)

#****************************************************************
# Action class to press and release a mouse button when entering 
#****************************************************************
class MouseQuickPress(MouseAction):
    def __init__(self, keys):
        MouseAction.__init__(self, keys)
        
    def enter(self, currentTime, fromVoiceRecognition):
        self.setKeyPressed()

#**************************************************
# Action class to handle single mouse button press 
#**************************************************
class MousePress(MouseAction):
    def __init__(self, keys):
        MouseAction.__init__(self, keys)
        
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

#****************************************************************
# Action class to press a mouse button when entering and leaving 
#****************************************************************
class MouseToggle(MouseAction):
    def __init__(self, keys):
        MouseAction.__init__(self, keys)
        
    def enter(self, currentTime, fromVoiceRecognition):
        self.setKeyPressed()
            
    def leave(self):
        self.setKeyPressed()

#******************************************************************
# Action class to change the state of a mouse button when entering 
#******************************************************************
class MouseSwitchState(MouseAction):
    def __init__(self, keys):
        MouseAction.__init__(self, keys)
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
class MouseSetState(MouseAction):
    def __init__(self, keys, state):
        MouseAction.__init__(self, keys)
        self.stateToSet = state

    def enter(self, currentTime, fromVoiceRecognition):
        if self.stateToSet:
            self.setKeyDown()
        else:
            self.setKeyUp()