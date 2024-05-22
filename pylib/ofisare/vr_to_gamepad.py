from .environment import environment
from .mode_based_actions import Mode

#************************************************
# Class to handle controller to gamepad mapping.
# Use its modes to steer mapping:
#  - leftTriggerMode and rightTriggerMode handle mapping from
#    controller to gamepad triggers
#  - leftStickMode and rightStickMode handle mapping from 
#    controller to gamepad sticks
#  - dpadMode handle mapping from controller sticks to dpad
# For all of those:
# - 0: No output
# - 1: Left trigger or stick
# - 2: Right trigger or stick
# For the dpad an additional dpadThreshold can be defined.
#************************************************
class VRToGamepad:
    def __init__(self):
        self.leftTriggerMode = Mode()
        self.rightTriggerMode = Mode()
        self.leftStickMode = Mode()
        self.rightStickMode = Mode()
        self.dpadMode = Mode()
        self.dpadThreshold = 0.3
        self.controller = None

    def setController(self, controllerType):
        self.controller = controllerType
        environment.vigem.CreateController(self.controller)

    def update(self, currentTime, deltaTime):
        # map left trigger to left trigger
        if self.leftTriggerMode == 1:
            environment.vigem.SetTrigger(self.controller, environment.VigemSide.Left, environment.openVR.leftTrigger)
        # map right trigger to left trigger
        elif self.leftTriggerMode == 2:
            environment.vigem.SetTrigger(self.controller, environment.VigemSide.Left, environment.openVR.rightTrigger)
        
        # map right trigger to right trigger
        if self.rightTriggerMode == 1:
            environment.vigem.SetTrigger(self.controller, environment.VigemSide.Right, environment.openVR.leftTrigger)
        # map left trigger to right trigger
        elif self.rightTriggerMode == 2:
            environment.vigem.SetTrigger(self.controller, environment.VigemSide.Right, environment.openVR.rightTrigger)
        
        # map left stick to left stick
        if self.leftStickMode == 1:
            environment.vigem.SetStick(self.controller, environment.VigemSide.Left, environment.openVR.leftStickAxes.x, environment.openVR.leftStickAxes.y)
        # map right stick to left stick
        elif self.leftStickMode == 2:
            environment.vigem.SetStick(self.controller, environment.VigemSide.Left, environment.openVR.rightStickAxes.x, environment.openVR.rightStickAxes.y)
        
        # map right stick to right stick
        if self.rightStickMode == 1:
            environment.vigem.SetStick(self.controller, environment.VigemSide.Right, environment.openVR.leftStickAxes.x, environment.openVR.leftStickAxes.y)
        # map left stick to right stick
        elif self.rightStickMode == 2:
            environment.vigem.SetStick(self.controller, environment.VigemSide.Right, environment.openVR.rightStickAxes.x, environment.openVR.rightStickAxes.y)
            
        # map left stick to dpad
        if self.dpadMode == 1:
            vigem.SetDPad(self.controller, environment.openVR.leftStickAxes.x, environment.openVR.leftStickAxes.y, self.dpadThreshold)
        # map right stick to dpad
        elif self.dpadMode == 2:
            vigem.SetDPad(self.controller, environment.openVR.rightStickAxes.x, environment.openVR.rightStickAxes.y, self.dpadThreshold)

    def reset(self):
        pass
