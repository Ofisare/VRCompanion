from .basic_actions import Action

#*********************************************************
# container to map a duration to an action for a sequence
#*********************************************************
class TimedAction:
    def __init__(self, action, duration):
        self.action = action
        self.duration = duration

#****************************************************************************
# an action to executing multiple actions after each for a specific duration
#****************************************************************************
class ActionSequence(Action):
    def __init__(self, actions):
        Action.__init__(self)
        self._actions = actions
        self._index = 0
        self._time = 0
    
    def duration(self):
        return sum(a.duration for a in self._actions)
    
    def getCurrentHaptics(self):
        if self._index < len(self._actions):
            haptics = self._actions[self._index].action.getCurrentHaptics() 
            if haptics != None:
                return haptics
        return self.haptics
        
    def enter(self, currentTime):
        self._index = 0
        self._time = currentTime
        self._actions[self._index].action.enter(currentTime)
    
    def update(self, currentTime):
        if self._index >= len(self._actions):
            return
            
        if self._actions[self._index].duration > currentTime - self._time:
            self._actions[self._index].action.update(currentTime)
        else:
            self._actions[self._index].action.leave()
            self._index = self._index + 1
            self._time = currentTime
            if self._index < len(self._actions):
                self._actions[self._index].action.enter(currentTime)
    
    def leave(self):
        if self._index < len(self._actions):
            self._actions[self._index].action.leave()
            
        self._index = 0
        self._time = 0
    
    def reset(self):
        for action in self._actions:
            action.action.reset()
        
        self._index = 0
        self._time = 0

#************************************
# Action class to repeat an action
#************************************
class ActionRepeat(Action):
    def __init__(self, action, times, actionDuration = 0.05, timeInterval = 0.2):
        Action.__init__(self)
        self._action = action
        self._times = times-1
        self._actionDuration = actionDuration
        self._timeInterval = timeInterval
        
        #internally used variables
        self._timesLeft = 0
        self._active = False
        self._needUpdate = False
        
    def duration(self):
        if self._times > 0:
            return self._times * self._timeInterval
        else:
            return self._timeInterval
    
    def getCurrentHaptics(self):
        haptics = self._action.getCurrentHaptics() 
        if haptics != None:
            return haptics
        return self.haptics
    
    def enter(self, currentTime):
        # activate action
        self._action.enter(currentTime)
        self._active = True
        
        # start the update timer
        self._time = currentTime
        self._needUpdate = True
        
        self._timesLeft = self._times
        
    def update(self, currentTime):
        if self._needUpdate:
            elapsedTime = currentTime - self._time
            
            # update action
            if elapsedTime < self._actionDuration:
            	self._action.update(currentTime)
            # leave action
            else:
                self._action.leave()
                self._active = False
        
                # End the update if the last repetion has been finished
                if (self._timesLeft == 0):
                    self._needUpdate = False
                    
                # check for end of pause
                if (elapsedTime >= self._timeInterval):
                    self._action.enter(currentTime)
                    self._active = True
                    
                    self._time = currentTime
                    if self._timesLeft > 0:
                        self._timesLeft = self._timesLeft - 1
        
    def leave(self):
        if self._active:
            self._action.leave()
            self._active = False
            self._needUpdate = False

    def reset(self):
        self.leave()

#**************************************************************
# Action class to differentiate between a short and long press 
#**************************************************************
class TimeBased(Action):
    def __init__(self, actions, duration = 0.25):
        Action.__init__(self)
        self._actions = actions
        self._duration = duration
        self._inLongAction = False
    
    def getCurrentHaptics(self):
        haptics = None
        if self._inLongAction:
            haptics = self._actions[1].getCurrentHaptics()
        else:
            haptics = self._actions[0].getCurrentHaptics()
            
        if haptics != None:
            return haptics
        return self.haptics
        
    def enter(self, currentTime):
        # start the update timer to be able to distinguish actions
        self._time = currentTime
        self._inLongAction = False
            
    def update(self, currentTime):
        if self._inLongAction:
            self._actions[1].update(currentTime)
        elif currentTime - self._time > self._duration:
            self._inLongAction = True
            self._actions[1].enter(currentTime)
        
    def leave(self):
        if self._inLongAction:
            self._actions[1].leave()
        else:
            self._actions[0].enter(self._time)
            self._actions[0].leave()
        self._inLongAction = False

    def reset(self):
        for action in self._actions:
            action.reset()
        self._inLongAction = False
