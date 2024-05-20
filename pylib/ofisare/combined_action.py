from .basic_actions import Action

#*******************************************************************************
# classes to require multiple gestures to be active before performing an action
# counter keeps track of active gestures and target count
# combined action takes care of activating counter and action
# only one combined action should manage the final action
#*******************************************************************************
class Counter:
    def __init__(self, count):
        self._target = count
        self._current = 0
        
    def increase(self):
        self._current = self._current + 1
        if self._current > self._target:
            raise Exception("Too many activations of counter, check number of combined actions using this counter.")
            
    def decrease(self):
        self._current = self._current - 1
        if self._current < 0:
            raise Exception("Too many deactivations of counter, check number of combined actions using this counter.")

    def active(self):
        return self._current == self._target

class CombinedAction(Action):
    def __init__(self, counter, action = None):
        Action.__init__(self)
        self._counter = counter
        self._action = action
        self._entered = False
        self._counterActive = False
    
    def enter(self, currentTime, fromVoiceRecognition):
        if fromVoiceRecognition:
            raise Exception("CombinedActions don't support voice commands")
        
        self._entered = True
        self._counter.increase()
        
        self._counterActive = self._counter.active()
        if self._action != None and self._counterActive:
            self._action.enter(currentTime, False)
        
    def update(self, currentTime):
        if self._action != None:
            # check for activation change
            if self._counterActive != self._counter.active():
                if self._counterActive:
                    self._action.leave()
                else:
                    self._action.enter(currentTime, False)
                self._counterActive = self._counter.active()
            elif self._counterActive:
                self._action.update(currentTime)    
            
    def leave(self):
        if self._action != None and self._counterActive:
            self._action.leave()
            
        self._counter.decrease()
        self._entered = False
        self._counterActive = False

    def reset(self):
        if self._entered:
            self.leave()
    
        if self._action != None:
            self._action.reset()