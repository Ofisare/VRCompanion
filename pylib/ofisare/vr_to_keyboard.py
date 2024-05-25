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
        self.yaw.inertiaSensitivity = 1.25                   # how fast the simulated yaw rotates in radians per second
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
        self.pitch.inertiaSensitivity = 1.25              # how fast the simulated pitch rotates in radians per second
        self.pitch.centerEpsilon = 0.05                   # the arc in which no head tracking happens when looking straight
        self.pitch.current = 0.0
        self.pitch.center = 0.0
        self.pitch.direction = None
        self.pitch.negativeKey = None                     # the key to press when the pitch is decreasing (down)
        self.pitch.positiveKey = None                     # the key to press when the pitch is increasing (up)
        self.pitch.centerKey = None                       # the key to press to center the pitch (if available)
        
        self.horizontal = type('horizontal',(object,),{})()       # all information regarding the horizontal (room scale movement)
        self.horizontal.mode = Mode()                         # how to map horizontal to keyboard
        self.horizontal.sensitivity = 0.1                   # how fast the simulated horizontal position moves in units per second
        self.horizontal.inertiaSensitivity = 0.2              # how fast the simulated horizontal position moves in units per second
        self.horizontal.centerEpsilon = 0.05
        self.horizontal.current = 0.0
        self.horizontal.center = 0.0
        self.horizontal.direction = None
        self.horizontal.negativeKey = None                     # the key to press when the horizontal position is decreasing (down)
        self.horizontal.positiveKey = None                     # the key to press when the horizontal position is increasing (up)
        self.horizontal.centerKey = None                       # the key to press to center the horizontal position (if available)
        
        self.vertical = type('vertical',(object,),{})()       # all information regarding the vertical (room scale movement)
        self.vertical.mode = Mode()                         # how to map vertical to keyboard
        self.vertical.sensitivity = 0.1                   # how fast the simulated vertical position moves in units per second
        self.vertical.inertiaSensitivity = 0.2              # how fast the simulated vertical position moves in units per second
        self.vertical.centerEpsilon = 0.05
        self.vertical.current = 0.0
        self.vertical.center = 0.0
        self.vertical.direction = None
        self.vertical.negativeKey = None                     # the key to press when the vertical position is decreasing (down)
        self.vertical.positiveKey = None                     # the key to press when the vertical position is increasing (up)
        self.vertical.centerKey = None                       # the key to press to center the vertical position (if available)
        
        self.headOrigin = Vector()

    def update(self, currentTime, deltaTime):
        if self.yaw.mode.current == 0 and self.pitch.mode.current == 0 and self.horizontal.mode.current == 0 or self.vertical.mode.current == 0:
            return;
            
        yawHead, pitchHead = getYawPitch(environment.openVR.headPose)
        # fix yaw > math.pi
        if self.yaw.current < yawHead - math.pi:
            yawHead = yawHead - 2 * math.pi
        elif self.yaw.current > yawHead + math.pi:
            yawHead = yawHead + 2 * math.pi
        
        self.updateCore(currentTime, deltaTime, self.yaw, yawHead)
        self.updateCore(currentTime, deltaTime, self.pitch, -pitchHead)
        
        headOffset = subtract(environment.openVR.headPose.position, self.headOrigin)
        headOffset = rotateYaw(headOffset, -yawHead)
        
        self.updateCore(currentTime, deltaTime, self.horizontal, headOffset.x)
        self.updateCore(currentTime, deltaTime, self.vertical, -headOffset.z)

    def updateCore(self, currentTime, deltaTime, axis, target):
        if axis.mode.current == 0:
            return
        
        if axis.direction == None:
            epsilon = axis.sensitivity * deltaTime
        else:
            epsilon = axis.inertiaSensitivity * deltaTime
        
        if abs(target - axis.current) >= epsilon:
            if axis.centerKey != None and abs(axis.center - target) < axis.centerEpsilon:
                axis.current = axis.center
                self.stopMovement(axis)
                environment.keyboard.setPressed(axis.centerKey)
            elif axis.current < target:
                axis.current = min(target, axis.current + axis.sensitivity * deltaTime)
                if axis.direction == -1:
                    environment.keyboard.setKeyUp(axis.negativeKey)
                if axis.direction != 1:
                    environment.keyboard.setKeyDown(axis.positiveKey)
                    axis.direction = 1
            elif axis.current > target:
                axis.current = max(target, axis.current - axis.sensitivity * deltaTime)
                if axis.direction == 1:
                    environment.keyboard.setKeyUp(axis.negativeKey)
                if axis.direction != -1:
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
        
        if axis.direction == -1:
            environment.keyboard.setKeyUp(axis.negativeKey)
        elif axis.direction == 1:
            environment.keyboard.setKeyUp(axis.positiveKey)
        axis.direction = None

    def reset(self):
        yawHead, pitchHead = getYawPitch(environment.openVR.headPose)
        self.headOrigin = environment.openVR.headPose.position
        
        self.yaw.current = yawHead
        self.yaw.center = yawHead
        
        self.pitch.current = pitchHead
        
        self.horizontal.current = 0
        self.vertical.current = 0
        
        self.stopMovement(self.yaw)
        self.stopMovement(self.pitch)
        self.stopMovement(self.horizontal)
        self.stopMovement(self.vertical)