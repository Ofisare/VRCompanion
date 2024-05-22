from .environment import environment
from .mode_based_actions import Mode
from .numerics import *

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
class VRToKeyboard:
    def __init__(self):
        self.yaw = type('yaw',(object,),{})()           # all information regarding the yaw (horizontal head tracking)
        self.yaw.mode = Mode()                          # how to map yaw to keyboard
        self.yaw.sensitivity = 1.25                   # how fast the simulated yaw rotates in radians per second
        self.yaw.epsilon = self.yaw.sensitivity / 60  # how fast the simulated yaw is in/decreased in one update step
        self.yaw.centerEpsilon = 0.05                   # the arc in which no head tracking happens when looking straight
        self.yaw.current = 0.0
        self.yaw.center = 0.0
        self.yaw.direction = None
        self.yaw.negativeKey = None                     # the key to press when the yaw is decreasing (left)
        self.yaw.positiveKey = None                     # the key to press when the yaw is increasing (right)
        self.yaw.centerKey = None                       # the key to press to center the yaw (if available)        
        
        self.pitch = type('pitch',(object,),{})()       # all information regarding the pitch (vertical head tracking)
        self.pitch.mode = Mode()                         # how to map pitch to keyboard
        self.pitch.sensitivity = 1.25                   # how fast the simulated pitch rotates in radians per second
        self.pitch.epsilon = self.yaw.sensitivity / 60  # how fast the simulated pitch is in/decreased in one update step
        self.pitch.centerEpsilon = 0.05                   # the arc in which no head tracking happens when looking straight
        self.pitch.current = 0.0
        self.pitch.center = 0.0
        self.pitch.direction = None
        self.pitch.negativeKey = None                     # the key to press when the pitch is decreasing (down)
        self.pitch.positiveKey = None                     # the key to press when the pitch is increasing (up)
        self.pitch.centerKey = None                       # the key to press to center the pitch (if available)

    def update(self, currentTime, deltaTime):
        yawHead, pitchHead = getYawPitch(environment.openVR.headPose)
        
        self.updateCore(currentTime, deltaTime, self.yaw, yawHead)
        self.updateCore(currentTime, deltaTime, self.pitch, -pitchHead)

    def updateCore(self, currentTime, deltaTime, axis, target):
        if axis.mode.current == 0:
            return
        
        if abs(target - axis.current) > axis.epsilon:
            if axis.centerKey != None and abs(axis.center - target) < axis.centerEpsilon:
                axis.current = axis.center
                self.stopMovement(axis)
                environment.keyboard.setPressed(axis.centerKey)
            elif axis.current < target:
                axis.current = min(target, axis.current + axis.sensitivity * deltaTime)
                if axis.direction == -1:
                    environment.keyboard.setKeyUp(axis.negativeKey)
                environment.keyboard.setKeyDown(axis.positiveKey)
                axis.direction = 1
            elif axis.current > target:
                axis.current = max(target, axis.current - axis.sensitivity * deltaTime)
                if axis.direction == 1:
                    environment.keyboard.setKeyUp(axis.negativeKey)
                environment.keyboard.setKeyDown(axis.negativeKey)
                axis.direction = -1
            else:
                self.stopMovement(axis)
        else:
            self.stopMovement(axis)
    
    def stopMovement(self, axis):
        if axis.mode.current == 0:
            return
        
        if axis.direction == None:
            return
        
        environment.keyboard.setKeyUp(axis.negativeKey)
        environment.keyboard.setKeyUp(axis.positiveKey)
        axis.direction = None

    def reset(self):
        yawHead, pitchHead = getYawPitch(environment.openVR.headPose)
        
        self.yaw.current = yawHead
        self.yaw.center = yawHead
        
        self.pitch.current = pitchHead
        
        self.stopMovement(self.yaw)
        self.stopMovement(self.pitch)