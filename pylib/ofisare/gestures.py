from .haptics import HapticsGroup
from .environment import environment

#*******************************************************************************************************
# Class to handle trigger or grip based validation of gestures and skip further uses of trigger or grip
#*******************************************************************************************************
class GestureValidation:
    def __init__(self, trigger, grip):
        self.trigger = trigger
        self.grip = grip
        
        self.triggerUsed = False
        self.gripUsed = False

#*****************************************************
# Class handling gesture actions and haptics feedback
#*****************************************************
class Gesture:
    # public members:
    # * action: the action to perform when in the gesture
    # * enabled: whether this gesture is active
    # * hapticsValidating: when hitting the right position but needing some time to confirm this interaction
    # * hapticsEnter: the haptics feedback when entering the gesture -> a one shot
    # * hapticsHold: the haptics when within the gesture -> a continuous feedback -> minigun/chainsaw
    # * hapticsLeave: the haptics when leaving the gesture
    
    def __init__(self, lowerThreshold, upperThreshold):
        self.lowerThreshold = lowerThreshold
        self.upperThreshold = upperThreshold
        
        self.coolDown = 0
        self._lastActionTime = 0
        self._lastTriggerTime = 0
        self._lastGripTime = 0
        
        self.validationMode = 0
        self.validationThreshold = 0.6
        self.validationTime = 0.5
        self._validationStartTime = 0
        
        self.haptics = HapticsGroup()
        self.validating = None
        self.touchValidating = None
        
        self.action = None
        self.triggerAction = None
        self.gripAction = None
        
        self.triggerLowerThreshold = 0.5
        self.triggerUpperThreshold = 0.6
        self.gripLowerThreshold = 0.5
        self.gripUpperThreshold = 0.6
        
        self.enabled = False
        self._inValidation = False
        self.inGesture = False
        self.inTriggerGesture = False
        self.inGripGesture = False
        
    def reset(self):
        if self.action != None:
            self.action.reset()
        if self.triggerAction != None:
            self.triggerAction.reset()
        if self.gripAction != None:
            self.gripAction.reset()
            
        self._inValidation = False
        self.inGesture = False
        self.inTriggerGesture = False
        self.inGripGesture = False
    
    def playHaptics(self, currentTime, haptics, touchHaptics):        
        if environment.hapticPlayer != None and haptics != None:
            environment.hapticPlayer.play_registered(currentTime, haptics)
        
        if environment.touchHaptics != None:
            environment.touchHapticsPlayer.play(touchHaptics)
   
    def _updateBaseGesture(self, currentTime, value, gestureValidation, haptics):
        # use action haptics
        if self.action != None:
            actionHaptics = self.action.getCurrentHaptics()
            if actionHaptics != None:
                haptics = actionHaptics
    
        # gesture entered, check whether to leave or stay in gesture
        if self.inGesture:
            if value > self.upperThreshold:
                self.playHaptics(currentTime, haptics.leave, haptics.touchLeave)
                if self.action != None:
                    self.action.leave()
                self.inGesture = False
                self._lastActionTime = currentTime
            else:
                self.playHaptics(currentTime, haptics.hold, haptics.touchHold)
                if self.action != None:
                    self.action.update(currentTime)
        # check whether to enter gesture
        else:
            if currentTime - self._lastActionTime > self.coolDown and value < self.lowerThreshold:
                valid = False
                # no validation required
                if self.validationMode == 0:
                    valid = True
                # delayed/time based validation
                elif self.validationMode == 1:
                    if self._inValidation:
                        valid = currentTime - self._validationStartTime > self.validationTime
                # trigger validation
                elif self.validationMode == 2:
                    valid = gestureValidation.triggerUsed == False and gestureValidation.trigger > self.validationThreshold
                # grip validation
                elif self.validationMode == 3:
                    valid = gestureValidation.gripUsed == False and gestureValidation.grip > self.validationThreshold
                
                # fially enter gesture if eveything is fine
                if valid:
                    self.playHaptics(currentTime, haptics.enter, haptics.touchEnter)
                    if self.action != None:
                        self.action.enter(currentTime, False)
                    self.inGesture = True
                
        # block other gestures from using trigger or grip
        if self.inGesture:
            # trigger validation
            if self.validationMode == 2:
                gestureValidation.triggerUsed = True
            # grip validation
            elif self.validationMode == 3:
                gestureValidation.gripUsed = True
    
    def _updateTriggerGesture(self, currentTime, value, gestureValidation, haptics):
        # use action haptics
        actionHaptics = self.triggerAction.getCurrentHaptics()
        if actionHaptics != None:
            haptics = actionHaptics
        
        # gesture entered, check whether to leave or stay in gesture
        if self.inTriggerGesture:
            if gestureValidation.triggerUsed == True or value > self.upperThreshold or gestureValidation.trigger < self.triggerLowerThreshold:
                self.playHaptics(currentTime, haptics.leave, haptics.touchLeave)    
                if self.triggerAction != None:
                    self.triggerAction.leave()
                self.inTriggerGesture = False
                self._lastTriggerTime = currentTime
            else:
                self.playHaptics(currentTime, haptics.hold, haptics.touchHold)
                if self.triggerAction != None:
                    self.triggerAction.update(currentTime)
        # check whether to enter gesture
        else:
            if currentTime - self._lastTriggerTime > self.coolDown and gestureValidation.triggerUsed == False and value < self.lowerThreshold and gestureValidation.trigger > self.triggerUpperThreshold:
                # enter gesture if eveything is fine
                self.playHaptics(currentTime, haptics.enter, haptics.touchEnter)
                if self.triggerAction != None:
                    self.triggerAction.enter(currentTime, False)
                self.inTriggerGesture = True
                
        # block other gestures from using trigger
        if self.inTriggerGesture:
            gestureValidation.triggerUsed = True
                    
    def _updateGripGesture(self, currentTime, value, gestureValidation, haptics):
        # use action haptics
        actionHaptics = self.gripAction.getCurrentHaptics()
        if actionHaptics != None:
            haptics = actionHaptics
        
        # gesture entered, check whether to leave or stay in gesture
        if self.inGripGesture:
            if gestureValidation.gripUsed == True or value > self.upperThreshold or gestureValidation.grip < self.gripLowerThreshold:
                self.playHaptics(currentTime, haptics.leave, haptics.touchLeave)
                if self.gripAction != None:
                    self.gripAction.leave()
                self.inGripGesture = False
                self._lastGripTime = currentTime 
            else:
                self.playHaptics(currentTime, haptics.hold, haptics.touchHold)
                if self.gripAction != None:
                    self.gripAction.update(currentTime)
        # check whether to enter gesture
        else:
            if currentTime - self._lastGripTime > self.coolDown and gestureValidation.gripUsed == False and value < self.lowerThreshold and gestureValidation.grip > self.gripUpperThreshold:
                # enter gesture if eveything is fine
                self.playHaptics(currentTime, haptics.enter, haptics.touchEnter)
                if self.gripAction != None:
                    self.gripAction.enter(currentTime, False)
                self.inGripGesture = True
                
        # block other gestures from using trigger
        if self.inGripGesture:
            gestureValidation.gripUsed = True
    
    def _updateCore(self, currentTime, value, gestureValidation, haptics):
        # check gestures
        if self.action != None:
            self._updateBaseGesture(currentTime, value, gestureValidation, haptics)
        if self.triggerAction != None:
            self._updateTriggerGesture(currentTime, value, gestureValidation, haptics)
        if self.gripAction != None:
            self._updateGripGesture(currentTime, value, gestureValidation, haptics)
        
        # check for validation
        if self.inGesture or self.inTriggerGesture or self.inGripGesture:
            self._inValidation = False
        elif value < self.lowerThreshold:
            if not self._inValidation:
                self.playHaptics(currentTime, self.validating, self.touchValidating)
                self._inValidation = True
                self._validationStartTime = currentTime
        else:
            self._inValidation = False
        
    def update(self, currentTime, value, gestureValidation):
        self._updateCore(currentTime, value, gestureValidation, self.haptics)

#***************************************************************
# Special class using item feedback instead of gesture feedback
#***************************************************************
class InventoryGesture(Gesture):
    def __init__(self, lowerThreshold, upperThreshold, inventory):
        Gesture.__init__(self, lowerThreshold, upperThreshold)
        self._inventory = inventory

    def update(self, currentTime, value, gestureValidation):
        # use item feedback if available
        item = self._inventory.get()
        if item == None:
            self._updateCore(currentTime, value, gestureValidation, self.haptics)
        else:
            self._updateCore(currentTime, value, gestureValidation, item.haptics)
            
#********************************************************************
# Special class for gestures based on an offset to the head position 
#********************************************************************
class LocationBasedGesture(Gesture):
    def __init__(self, lowerThreshold, upperThreshold, offset):
        Gesture.__init__(self, lowerThreshold, upperThreshold)
        self.offset = offset