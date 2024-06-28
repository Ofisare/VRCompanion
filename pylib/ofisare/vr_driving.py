from .environment import environment
from .mode_based_actions import Mode
from .numerics import *
from .vr_roomscale import VRRoomscaleAxis

import math

#****************************************************************
# Class to handle mouse movement based on headset or controller.
# Use its mode to steer mapping:
# - 0: No mouse output
# - 1: Headset to mouse
# - 2: Left controller to mouse
# - 3: Right controller to mouse
# - 4: right stick only
# Additionally, you can switch between using a controllers
# position or orientation (useControllerOrientation).
#****************************************************************
class VRDriving:
    def __init__(self):
        self.axis = VRRoomscaleAxis()
        self.axis.mode.current = True
        self.axis.sensitivity = 1.0
        
        self.leftControllerActive = Mode()
        self.leftControllerActive.current = False
        self._lastLeftControllerActive = False
        
        self.rightControllerActive = Mode()
        self.rightControllerActive.current = False
        self._lastRightControllerActive = False
        
        self._lastAngle = 0
        
        self._initialLeftVector = Vector()
        self._leftAngleOffset = 0
        self._initialRightVector = Vector()
        self._leftRightOffset = 0

    def update(self, currentTime, deltaTime):
        if self.leftControllerActive.current != True and self.rightControllerActive.current != True:
            self.axis.stopMovement()
            self.axis.current = 0
            
            self._lastLeftControllerActive = False
            self._lastRightControllerActive = False
            self._lastAngle = 0
            
            return
        
        angle = 0
        count = 0
        
        # get angle based on left controller
        if self.leftControllerActive.current:
            vector, forward = self.getVectors(environment.openVR.leftTouchPose)
            if self._lastLeftControllerActive:
                angle += angleBetween(self._initialLeftVector, vector, forward)
            else:
                self._lastLeftControllerActive = True
                self._initialLeftVector = vector
                self._leftAngleOffset = self._lastAngle
            angle += self._leftAngleOffset
            count += 1
        else:
            self._lastLeftControllerActive = False
        
        # get angle based on right controller
        if self.rightControllerActive.current:
            vector, normal = self.getVectors(environment.openVR.rightTouchPose)
            if self._lastRightControllerActive:
                angle += angleBetween(self._initialRightVector, vector, normal)
            else:
                self._lastRightControllerActive = True
                self._initialRightVector = vector
                self._rightAngleOffset = self._lastAngle
            angle += self._rightAngleOffset
            count += 1
        else:
            self._lastRightControllerActive = False
        
        angle /= count
        
        self.axis.update(currentTime, deltaTime, -angle)
        self._lastAngle = angle
        
        environment.watch(angle)
        
    def getVectors(self, pose):
        return pose.left, pose.up
    
    def reset(self):
        self.axis.stopMovement()
        self.axis.current = 0
        self._lastLeftControllerActive = False
        self._lastRightControllerActive = False
        self._lastAngle = 0