from .environment import environment
from .mode_based_actions import Mode
from .numerics import *

import math

class VRRoomscaleAxis:
    def __init__(self):
        self.mode = Mode()              # mode to enable axis (0: off, 1: action duration + hold, 10: direct mouse, 20: direct gamepad)
        self._lastMode = 0              
        self.sensitivity = 1.25         # how fast the simulated axis moves/rotates in units/radians per second, or for mapping the target value to mouse or gamepad axis
        self.centerEpsilon = 0.05       # epsilon around center position to perform center action
        self.holdThreshold = 100000     # a threshold to hold negative or positive when target exceeds this value
        self.current = 0.0              # the simulated current axis value
        self.center = 0.0               # the center position for the center action
        self.centered = True            # whether the axis has been centered
        self.direction = None           # the current movement direction (-1, 1, None)
        self.negativeAction = None      # the action to perform when the axis is decreasing
        self.positiveAction = None      # the action to perform when the axis is increasing
        self.centerAction = None        # the action to perform to center the axis (if available)
        self.gamepadSide = None         # the side of the gamepad stick
        self.gamepadAxis = None         # the gamepad stick axis
        self.mouseAxis = None           # the mouse axis
        
    def update(self, currentTime, deltaTime, target):
        # mapped to action by duration
        if self.mode.current == 1:
            maxChange = self.sensitivity * deltaTime
            if abs(target - self.current) >= maxChange or abs(target - self.center) > self.holdThreshold:
                if self.centerAction != None and abs(self.center - target) < self.centerEpsilon:
                # reset axis
                    if self.direction == 0:
                        self.stopMovement()
                        self.centered = True
                    elif self.centered == False:
                        self.stopMovement()
                        self.current = self.center
                        self.centerAction.enter(currentTime, False)
                        self.direction = 0
                
                elif self.current < target or target > self.center + self.holdThreshold:
                # update axis
                    self.current = min(target, self.current + maxChange)
                    # perform positive movement
                    if self.direction == 1:
                        self.positiveAction.update(currentTime)
                    else:
                        # stop current movement
                        self.stopMovement()
                        # start positive movement
                        self.centered = False
                        self.direction = 1
                        self.positiveAction.enter(currentTime, False)
                        
                elif self.current > target or target < self.center - self.holdThreshold:
                # update axis
                    self.current = max(target, self.current - maxChange)
                    # perform negative movement
                    if self.direction == -1:
                        self.negativeAction.update(currentTime)
                    else:
                        # stop current movement
                        self.stopMovement()
                        # start negative movement
                        self.centered = False
                        self.direction = -1
                        self.negativeAction.enter(currentTime, False)
                else:
                    self.stopMovement()
            else:
                self.stopMovement()
        # mapped to mouse axis
        elif self.mode.current == 10:
            value = (target - self.center) / self.sensitivity
            if self.mouseAxis != 1:
                environment.mouse.deltaX = value
            else:
                environment.mouse.deltaY = value
        # mapped to gamepad
        elif self.mode.current == 20:
            value = (target - self.center) / self.sensitivity
            environment.vigem.SetStick(environment.vrToGamepad.controller, self.gamepadSide, self.gamepadAxis, value)
        # no movement 
        else:
            self.stopMovement()
                
        self._lastMode = self.mode.current
    
    def stopMovement(self):
        if self._lastMode == 1:        
            if self.direction == None:
                return
            
            if self.direction == 0:
                self.centerAction.leave()
            elif self.direction == -1:
                self.negativeAction.leave()
            elif self.direction == 1:
                self.positiveAction.leave()
            
            self.direction = None
        elif self._lastMode == 20:
            environment.vigem.SetStick(environment.vrToGamepad.controller, self.gamepadSide, self.gamepadAxis, 0)

#******************************************************************
# Class to handle headset rotaion and movement to discrete actions
# for a duration to reflect that change.
# Use case 1: games with rotation mapped solely to keyboard
# Use case 2: roomscale movement, reflect own movement in game
#******************************************************************
class VRRoomscale:
    def __init__(self):
        self.yaw = VRRoomscaleAxis()
        self.pitch = VRRoomscaleAxis()
        self.roll = VRRoomscaleAxis()
        
        self.horizontal = VRRoomscaleAxis()
        self.horizontal.sensitivity = 0.1
        
        self.vertical = VRRoomscaleAxis()
        self.vertical.sensitivity = 0.1
    
        self.headOrigin = Vector()

    def update(self, currentTime, deltaTime):
        if self.yaw.mode.current == 0 and self.pitch.mode.current == 0 and self.roll.mode.current == 0 and self.horizontal.mode.current == 0 or self.vertical.mode.current == 0:
            return;
            
        # fix yaw > math.pi
        yawHead = environment.vr.headPose
        if self.yaw.current < yawHead - math.pi:
            yawHead = yawHead - 2 * math.pi
        elif self.yaw.current > yawHead + math.pi:
            yawHead = yawHead + 2 * math.pi
        
        self.updateCore(currentTime, deltaTime, self.yaw, yawHead)
        self.updateCore(currentTime, deltaTime, self.pitch, -environment.vr.headPose.pitch)
        self.updateCore(currentTime, deltaTime, self.roll, environment.vr.headPose.roll)
        
        headOffset = subtract(environment.vr.headPose.position, self.headOrigin)
        headOffset = rotateYaw(headOffset, -yawHead)
        
        self.updateCore(currentTime, deltaTime, self.horizontal, headOffset.x)
        self.updateCore(currentTime, deltaTime, self.vertical, -headOffset.z)
    
    def reset(self):
        self.headOrigin = environment.vr.headPose.position
        
        self.yaw.current = environment.vr.headPose.yaw
        self.yaw.center = environment.vr.headPose.yaw
        self.pitch.current = environment.vr.headPose.pitch
        self.roll.current = environment.vr.headPose.roll
        self.horizontal.current = 0
        self.vertical.current = 0
        
        self.yaw.stopMovement()
        self.pitch.stopMovement()
        self.roll.stopMovement()
        self.horizontal.stopMovement()
        self.vertical.stopMovement()