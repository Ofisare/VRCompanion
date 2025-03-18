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
        
        # define a delegate function called beforeUpdate(sender)
        self.beforeUpdate = None
        # define a delegate function called afterUpdate(sender)
        self.afterUpdate = None

        self._yaw = 0.0
        self._pitch = 0.0
        self.deltaX = 0.0
        self.deltaY = 0.0
        
        self._lastMode = 0
        self._yawOffset = 0.0
        self._pitchOffset = 0.0

    def update(self, currentTime, deltaTime):

        if self.beforeUpdate is not None:
            self.beforeUpdate(self)

        if self.mode.current == 0:
            if self._lastMode != 0:
                # reset settings
                self._lastMode = self.mode.current
                self._yawOffset = 0
                self._pitchOffset = 0
                self.deltaX = 0.0
                self.deltaY = 0.0
                # no mouse mapping
                environment.freePieIO[0].yaw = 0
                environment.freePieIO[0].pitch = 0
                environment.freePieIO[0].roll = 0
            return

        yawTarget = self._yaw
        pitchTarget = self._pitch
        
        # get head orientation
        
        if self.mode.current == 1:
            yawTarget = environment.vr.headPose.yawRaw
            pitchTarget = environment.vr.headPose.pitchRaw
        elif self.mode.current == 2:
            # left controller
            if self.useControllerOrientation:
                yawTarget = environment.vr.leftTouchPose.yawRaw + self._yawOffset
                pitchTarget = environment.vr.leftTouchPose.pitchRaw + self._pitchOffset
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
                yawTarget = environment.vr.rightTouchPose.yawRaw + self._yawOffset
                pitchTarget = environment.vr.rightTouchPose.pitchRaw + self._pitchOffset
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
                
                yawChange = environment.vr.headPose.yawRaw - self._yaw                
                if yawChange > math.pi:
                    yawChange = yawChange - math.pi * 2
                elif yawChange < -math.pi:
                    yawChange = yawChange + math.pi * 2
                    
                pitchChange = environment.vr.headPose.pitchRaw - self._pitch
                
                self._yaw = environment.vr.headPose.yaw
                self._pitch = environment.vr.headPose.pitch
            else:
                self._yawOffset = environment.vr.headPose.yawRaw - yawTarget
                self._pitchOffset = environment.vr.headPose.pitchRaw - pitchTarget
                yawChange = 0
                pitchChange = 0
                self._yaw = environment.vr.headPose.yawRaw
                self._pitch = environment.vr.headPose.pitchRaw
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
                self.deltaX = deltaX + environment.vr.rightStickAxes.x * self.mouseSensitivityX * self.stickMultiplierX * deltaTime
                self.deltaY = deltaY - environment.vr.rightStickAxes.y * self.mouseSensitivityY * self.stickMultiplierY * deltaTime
            else:
                self.deltaX = deltaX + environment.vr.leftStickAxes.x * self.mouseSensitivityX * self.stickMultiplierX * deltaTime
                self.deltaY = deltaY - environment.vr.leftStickAxes.y * self.mouseSensitivityY * self.stickMultiplierY * deltaTime
        
        if self.afterUpdate is not None:
            self.afterUpdate(self)

        environment.mouse.deltaX = self.deltaX
        environment.mouse.deltaY = self.deltaY
        
        # communicate to reshade
        if self.enableYawPitch.current:
            yaw = environment.vr.headPose.yawRaw - self._yaw            
            if yaw > math.pi:
                yaw = yaw - math.pi * 2
            elif yaw < -math.pi:
                yaw = yaw + math.pi * 2
        
            environment.freePieIO[0].yaw = yaw
            environment.freePieIO[0].pitch = self._pitch - environment.vr.headPose.pitchRaw
        else:
            environment.freePieIO[0].yaw = 0
            environment.freePieIO[0].pitch = 0
            
        if self.enableRoll.current:
            environment.freePieIO[0].roll = -environment.vr.headPose.rollRaw
        else:
            environment.freePieIO[0].roll = 0

    def reset(self):
        # clear communication with reshade
        environment.freePieIO[0].yaw = 0
        environment.freePieIO[0].pitch = 0
        environment.freePieIO[0].roll = 0