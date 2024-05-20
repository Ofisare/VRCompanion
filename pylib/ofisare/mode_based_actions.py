from .basic_actions import Action

#******************************
# Mode switching functionality
#******************************
class Mode:
    def __init__(self):
        self.current = 0

class ModeBasedAction(Action):
    def __init__(self, mode, actions, defaultAction = None):
        Action.__init__(self)
        self._mode = mode
        # append or extend (both are valid)
        if isinstance(actions, list):
            self._actions = dict()
            for i, action in enumerate(actions):
                self._actions[i] = action
        else:
            self._actions = actions
        self._defaultAction = defaultAction
        self._activeMode = mode.current
        self._needUpdate = False
        
    def getCurrentAction(self):
    	return self._actions.get(self._activeMode, self._defaultAction)

    def getCurrentHaptics(self):
        action = self.getCurrentAction()
        if action != None:
            haptics = action.getCurrentHaptics()
            if haptics != None:
                return haptics
        return self.haptics

    def enter(self, currentTime, fromVoiceRecognition):
        self._activeMode = self._mode.current
        action = self.getCurrentAction()
        if action != None:
            action.enter(currentTime, fromVoiceRecognition)            
        self._needUpdate = fromVoiceRecognition == False
    
    def update(self, currentTime):
        if self._needUpdate:
            return
    
        if self._mode.current == self._activeMode:
            action = self.getCurrentAction()
            if action != None:
                action.update(currentTime)
        else:
            action = self.getCurrentAction()
            if action != None:
                action.leave()
            self._activeMode = self._mode.current
            action = self.getCurrentAction()
            if action != None:
                action.enter(currentTime, False)
    
    def leave(self):
        action = self.getCurrentAction()
        if action != None:
            action.leave()
    
    def reset(self):
        for key, action in self._actions.iteritems():
            action.reset()

class ModeSwitch(Action):
    def __init__(self, mode, selectedMode):
        Action.__init__(self)
        self._mode = mode
        self._selectedMode = selectedMode
        
    def enter(self, currentTime, fromVoiceRecognition):
        if fromVoiceRecognition:
            self.leave()
        
    def leave(self):
        self._mode.current = self._selectedMode

class ModeCopy(Action):
    def __init__(self, mode, targetMode):
        Action.__init__(self)
        self._mode = mode
        self._targetMode = targetMode
    
    def leave(self):
        self._mode.current = self._targetMode.current

#---------------------------------------------------------------------
# Action to set the mode when entering and resetting it when leaving.
# An exit mode can also be set instead of using the one which was
# active when entering.
# Does not work in combination with mode based action.
#---------------------------------------------------------------------
class ModeSwitchWithReset(Action):
    def __init__(self, mode, selectedMode, resetMode = None):
        Action.__init__(self)
        self._mode = mode
        self._selectedMode = selectedMode
        self._resetMode = resetMode
        self._lastMode = mode.current
        
    def enter(self, currentTime, fromVoiceRecognition):
        self._lastMode = self._mode.current # remember last mode to reset
        self._mode.current = self._selectedMode
    
    def leave(self):
        if self._resetMode == None:
            self._mode.current = self._lastMode
        else:
            self._mode.current = self._resetMode
