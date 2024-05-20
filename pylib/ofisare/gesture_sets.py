from gesture_tracker import GestureTracker
from mode_based_actions import Mode

#**********************************************
# class for handling multiple gesture trackers
#**********************************************
class GestureSets:
    def __init__(self, weaponInventory):
        self.defaultGestureSet = GestureTracker(weaponInventory)
        self.gestureSets = dict()
        self.mode = Mode()
        self._activeMode = None
    
    def createGestureSet(self, mode, weaponInventory):
        gestures = GestureTracker(weaponInventory)
        self.gestureSets[mode] = gestures
        return gestures
    
    def getCurrentGestureSet(self):
        return self.gestureSets.get(self._activeMode, self.defaultGestureSet)
    
    def update(self, currentTime, deltaTime):
        if self.mode.current != self._activeMode:
            gestures = self.getCurrentGestureSet()
            gestures.reset()
            if gestures.leave != None:
                gestures.leave.enter(currentTime, False)
                gestures.leave.leave()
            self._activeMode = self.mode.current
            gestures = self.getCurrentGestureSet()
            if gestures.enter != None:
                gestures.enter.enter(currentTime, False)
                gestures.enter.leave()
        self.getCurrentGestureSet().update(currentTime, deltaTime)
            