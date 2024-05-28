from .environment import environment
from .mode_based_actions import Mode
from .numerics import *

import math

class VRRoomscaleAxis:
    def __init__(self):
        self.mode = Mode()              # mode to enable axis
        self.sensitivity = 1.25         # how fast the simulated axis moves/rotates in units/radians per second
        self.centerEpsilon = 0.05       # epsilon around center position to perform center action
        self.current = 0.0              # the simulated current axis value
        self.center = 0.0               # the center position for the center action
        self.centered = True            # whether the axis has been centered
        self.direction = None           # the current movement direction (-1, 1, None)
        self.negativeAction = None      # the action to perform when the axis is decreasing
        self.positiveAction = None      # the action to perform when the axis is increasing
        self.centerAction = None        # the action to perform to center the axis (if available)

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
        
        self.horizontal = VRRoomscaleAxis()
        self.horizontal.sensitivity = 0.1
        
        self.vertical = VRRoomscaleAxis()
        self.vertical.sensitivity = 0.1
    
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
        
        maxChange = axis.sensitivity * deltaTime
        if abs(target - axis.current) >= maxChange:
            if axis.centerAction != None and abs(axis.center - target) < axis.centerEpsilon:
            # reset axis
                if axis.direction == 0:
                    self.stopMovement(axis)
                    axis.centered = True
                elif axis.centered == False:
                    self.stopMovement(axis)
                    axis.current = axis.center
                    axis.centerAction.enter(currentTime, False)
                    axis.direction = 0
            
            elif axis.current < target:
            # update axis
                axis.current = min(target, axis.current + maxChange)
                # perform positive movement
                if axis.direction == 1:
                    axis.positiveAction.update(currentTime)
                else:
                    # stop current movement
                    self.stopMovement(axis)
                    # start positive movement
                    axis.centered = False
                    axis.direction = 1
                    axis.positiveAction.enter(currentTime, False)
                    
            elif axis.current > target:
            # update axis
                axis.current = max(target, axis.current - maxChange)
                # perform negative movement
                if axis.direction == -1:
                    axis.negativeAction.update(currentTime)
                else:
                    # stop current movement
                    self.stopMovement(axis)
                    # start negative movement
                    axis.centered = False
                    axis.direction = -1
                    axis.negativeAction.enter(currentTime, False)
            else:
                self.stopMovement(axis)
        else:
            self.stopMovement(axis)
    
    def stopMovement(self, axis):
        if axis.mode.current == 0:
            return
        
        if axis.direction == None:
            return
        
        if axis.direction == 0:
            axis.centerAction.leave()
        elif axis.direction == -1:
            axis.negativeAction.leave()
        elif axis.direction == 1:
            axis.positiveAction.leave()
        
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