from .vr_headjoy import HeadJoystick
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
        self.headMode = Mode()
        self.dpadMode = Mode()
        self.dpadThreshold = 0.3
        self.controller = None
        
        self.headJoy = HeadJoystick()
        self.beforeUpdate = None

    def setController(self, controllerType):
        self.controller = controllerType
        environment.vigem.CreateController(self.controller)

    def update(self, currentTime, deltaTime):

        if self.beforeUpdate is not None:
            self.beforeUpdate(self)

        # map left trigger to left trigger
        if self.leftTriggerMode.current == 1:
            environment.vigem.SetTrigger(self.controller, environment.VigemSide.Left, environment.vr.leftTrigger)
        # map right trigger to left trigger
        elif self.leftTriggerMode.current == 2:
            environment.vigem.SetTrigger(self.controller, environment.VigemSide.Left, environment.vr.rightTrigger)
        
        # map right trigger to right trigger
        if self.rightTriggerMode.current == 1:
            environment.vigem.SetTrigger(self.controller, environment.VigemSide.Right, environment.vr.leftTrigger)
        # map left trigger to right trigger
        elif self.rightTriggerMode.current == 2:
            environment.vigem.SetTrigger(self.controller, environment.VigemSide.Right, environment.vr.rightTrigger)
        
        # map left stick to left stick
        if self.leftStickMode.current == 1:
            environment.vigem.SetStick(self.controller, environment.VigemSide.Left, environment.vr.leftStickAxes.x, environment.vr.leftStickAxes.y)
        # map right stick to left stick
        elif self.leftStickMode.current == 2:
            environment.vigem.SetStick(self.controller, environment.VigemSide.Left, environment.vr.rightStickAxes.x, environment.vr.rightStickAxes.y)
        
        if self.headMode.current == 1:
            if self.headJoy.isActive():
                environment.vigem.SetStick(self.controller, environment.VigemSide.Right, self.headJoy.x, self.headJoy.y)        
            # else:
            #     environment.vigem.SetStick(self.controller, environment.VigemSide.Right, 0, 0)
        # map right stick to right stick
        if self.rightStickMode.current == 1:
            environment.vigem.SetStick(self.controller, environment.VigemSide.Right, environment.vr.leftStickAxes.x, environment.vr.leftStickAxes.y)
        # map left stick to right stick
        elif self.rightStickMode.current == 2:
            environment.vigem.SetStick(self.controller, environment.VigemSide.Right, environment.vr.rightStickAxes.x, environment.vr.rightStickAxes.y)
            
        # map left stick to dpad
        if self.dpadMode.current == 1:
            environment.vigem.SetDPad(self.controller, environment.vr.leftStickAxes.x, environment.vr.leftStickAxes.y, self.dpadThreshold)
        # map right stick to dpad
        elif self.dpadMode.current == 2:
            environment.vigem.SetDPad(self.controller, environment.vr.rightStickAxes.x, environment.vr.rightStickAxes.y, self.dpadThreshold)

    def reset(self):
        pass
