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
class VRToMouse:
    def __init__(self):
        self.mode = Mode()
        self.stickMode = Mode()
        self.stickMode.current = 1
        self.mouseSensitivityX = 800
        self.mouseSensitivityY = 800
        self.stickMultiplierX = 1
        self.stickMultiplierY = 1
        self.enableYawPitch = Mode()
        self.enableYawPitch.current = True
        self.enableRoll = Mode()
        self.enableRoll.current = False
        self.useControllerOrientation = True
        self.useRightController = True
        
        self._yaw = 0.0
        self._pitch = 0.0
        
        self._lastMode = 0
        self._yawOffset = 0.0
        self._pitchOffset = 0.0

    def update(self, currentTime, deltaTime):
        if self.mode.current == 0:
            if self._lastMode != 0:
                # reset settings
                self._lastMode = self.mode.current
                self._yawOffset = 0
                self._pitchOffset = 0
                # no mouse mapping
                environment.freePieIO[0].yaw = 0
                environment.freePieIO[0].pitch = 0
                environment.freePieIO[0].roll = 0
            return

        yawTarget = self._yaw
        pitchTarget = self._pitch
        
        # get head orientation
        yawHead, pitchHead, rollHead = getYawPitchRoll(environment.vr.headPose)
        if self.mode.current == 1:
            yawTarget = yawHead
            pitchTarget = pitchHead            
        elif self.mode.current == 2:
            # left controller
            if self.useControllerOrientation:
                yaw, pitch = getYawPitch(environment.vr.leftTouchPose)
                yawTarget = yaw + self._yawOffset
                pitchTarget = pitch + self._pitchOffset
            else:
                dx = environment.vr.leftTouchPose.position.x - environment.vr.headPose.position.x
                dy = environment.vr.leftTouchPose.position.y - environment.vr.headPose.position.y
                dz = environment.vr.leftTouchPose.position.z - environment.vr.headPose.position.z
                dh = math.sqrt(dx*dx + dz*dz)
                yawTarget = math.pi + math.atan2(dz, dx) + self._yawOffset
                pitchTarget = -math.atan2(dy, dh) + self._pitchOffset
        elif self.mode.current == 3:
            # right controller
            if self.useControllerOrientation:
                yaw, pitch = getYawPitch(environment.vr.rightTouchPose)
                yawTarget = yaw + self._yawOffset
                pitchTarget = pitch + self._pitchOffset
            else:
                dx = environment.vr.rightTouchPose.position.x - environment.vr.headPose.position.x
                dy = environment.vr.rightTouchPose.position.y - environment.vr.headPose.position.y
                dz = environment.vr.rightTouchPose.position.z - environment.vr.headPose.position.z
                dh = math.sqrt(dx*dx + dz*dz)
                yawTarget = math.pi + math.atan2(dz, dx) + self._yawOffset
                pitchTarget = -math.atan2(dy, dh) + self._pitchOffset
                
        if self._lastMode != self.mode.current:
            if self.mode.current == 1 and self._lastMode > 1:
                self._yawOffset = 0
                self._pitchOffset = 0
                
                yawChange = yawHead - self._yaw                
                if yawChange > math.pi:
                    yawChange = yawChange - math.pi * 2
                elif yawChange < -math.pi:
                    yawChange = yawChange + math.pi * 2
                    
                pitchChange = pitchHead - self._pitch
                
                self._yaw = yawHead
                self._pitch = pitchHead
            else:
                self._yawOffset = yawHead - yawTarget
                self._pitchOffset = pitchHead - pitchTarget
                yawChange = 0
                pitchChange = 0
                self._yaw = yawHead
                self._pitch = pitchHead
            self._lastMode = self.mode.current
        else:
            # apply offset and changes to view and mouse movement
            yawTarget = yawTarget
            pitchTarget = pitchTarget
            yawChange = yawTarget - self._yaw
            pitchChange = pitchTarget - self._pitch
            
            self._yaw = yawTarget
            self._pitch = pitchTarget
        
        if yawChange > math.pi:
            yawChange = yawChange - math.pi * 2
        elif yawChange < -math.pi:
            yawChange = yawChange + math.pi * 2
        
        deltaX = yawChange * self.mouseSensitivityX
        deltaY = pitchChange * self.mouseSensitivityY
        
        if self.stickMode.current == 1:
            if self.useRightController:
                deltaX = deltaX + environment.vr.rightStickAxes.x * self.mouseSensitivityX * self.stickMultiplierX * deltaTime
                deltaY = deltaY - environment.vr.rightStickAxes.y * self.mouseSensitivityY * self.stickMultiplierY * deltaTime
            else:
                deltaX = deltaX + environment.vr.leftStickAxes.x * self.mouseSensitivityX * self.stickMultiplierX * deltaTime
                deltaY = deltaY - environment.vr.leftStickAxes.y * self.mouseSensitivityY * self.stickMultiplierY * deltaTime
        
        environment.mouse.deltaX = deltaX
        environment.mouse.deltaY = deltaY
        
        # communicate to reshade
        if self.enableYawPitch.current:
            yaw = yawHead - self._yaw            
            if yaw > math.pi:
                yaw = yaw - math.pi * 2
            elif yaw < -math.pi:
                yaw = yaw + math.pi * 2
        
            environment.freePieIO[0].yaw = yaw
            environment.freePieIO[0].pitch = self._pitch - pitchHead
        else:
            environment.freePieIO[0].yaw = 0
            environment.freePieIO[0].pitch = 0
            
        if self.enableRoll.current:
            environment.freePieIO[0].roll = -rollHead
        else:
            environment.freePieIO[0].roll = 0

    def reset(self):
        # clear communication with reshade
        environment.freePieIO[0].yaw = 0
        environment.freePieIO[0].pitch = 0
        environment.freePieIO[0].roll = 0