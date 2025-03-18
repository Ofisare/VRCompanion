from .environment import environment
from .basic_actions import Action

#*********************************************************************
# Special class to dispatch an action from a gesture or voice control
#*********************************************************************
class DispatchAction(Action):
    def __init__(self, action, duration):
        Action.__init__(self)
        self._action = action
        self._duration = duration
        self._time = 0
       
    def getCurrentHaptics(self):
        haptics = self._action.getCurrentHaptics()
        if haptics != None:
            return haptics
        return self.haptics
        
    def enter(self, currentTime):
        if environment.dispatcher == None or self._time > 0:
            return
        self._time = currentTime
        self._action.enter(currentTime)
        environment.dispatcher.addAction(self)
    
    def updateFromDispatcher(self, currentTime):
        if environment.dispatcher == None:
            return False
        if self._duration < currentTime - self._time:
            self._time = 0
            self._action.leave()
            return True
        self._action.update(currentTime)
        return False
        
    def reset(self):
        if environment.dispatcher == None:
            return
        self._time = 0
        self._action.reset()
        environment.dispatcher.removeAction(self)

#********************************************
# Engine to handle asynchronous actions
#********************************************
class Dispatcher:
    def __init__(self):
        self._actions = []
    
    def addAction(self, action):
        self._actions.append(action)
        
    def removeAction(self, action):    
        if action in self._actions:
            self._actions.remove(action)

    def update(self, currentTime):
        finishedActions = []
        for action in self._actions:
            if action.updateFromDispatcher(currentTime):
                finishedActions.append(action)
        if finishedActions:
            self._actions = [action for action in self._actions if action not in finishedActions]
        
    def reset(self):
        actions = self._actions
        self._actions = []
        
        for action in actions:
            action.reset()