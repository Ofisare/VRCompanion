from .environment import environment

class HeadJoystickDirection:
    
    def __init__(self, isInverted, minDegrees, maxDegrees, minValue , maxValue, curve = None):
        # type: (int, bool,float, float, float, float, CurveGlobal) -> None
        """
        Initializes the VRHeadJoy object. (Note: All arguments should be positive values, for negative values use the bInverted flag)
        Args:
            isInverted (bool, optional): Inverts the output value. Defaults to False.   
            minDegrees (int): Minimum degrees of head rotation to produce output.
            maxDegrees (int): Maximum degrees of head rotation to produce output.
            minValue (float): Minimum value for axis output. (0-1). **Set to value greater than 0 to create an anti-deadzone.
            maxValue (float): Maximum value for axis output. (0-1).
            curve (Curve, optional): Curve to apply to the output value. Defaults to None.
        """
        self.isInverted = isInverted
        self.minDegrees = abs(minDegrees)
        self.maxDegrees = abs(maxDegrees)
        self.minValue = abs(minValue)
        self.maxValue = abs(maxValue)
        self.curve = curve

        self.currentDegrees = 0.0
        
    @property
    def value(self):
        # type: () -> float
        retval = 0.0
        #minDegrees = self.maxDegrees * self.deadZone
        if not self.isActive:
            retval = 0
        else:
            retval = environment.filters.ensureMapRange(abs(self.currentDegrees), self.minDegrees, self.maxDegrees, self.minValue, self.maxValue)
        
        if(self.curve is not None):
            #environment.diagnostics.debug("Curve is not None")
            retval = self.curve.getY(retval)

        if self.isInverted:
            retval = -retval

        return retval

    @property
    def isActive(self):
    # type: (float) -> bool
        return abs(self.currentDegrees) > self.minDegrees
    
class HeadJoystick:
    
    def __init__(self):
        #self.bJoyLookEnabled = False
        self.left  = HeadJoystickDirection(True, 0, 40, 0, 1)  
        self.right = HeadJoystickDirection(False,0, 40, 0, 1) 
        self.up    = HeadJoystickDirection(True, 0, 25, 0, 1) 
        self.down  = HeadJoystickDirection(False,0, 25, 0, 1) 
        self._yaw = 0
        self._pitch = 0
        
    def update(self):
        # type: () -> None        
        self.left.currentDegrees = self.right.currentDegrees = self._yaw = environment.vr.headPose.yaw
        self.up.currentDegrees = self.down.currentDegrees = self._pitch = environment.vr.headPose.pitch
        
    
    @property
    def x(self):
        #type: () -> float
        return self.left.value if self._yaw < 0 else self.right.value if self._yaw > 0 else 0
    
    @property
    def y(self):
        #type: () -> float
        return self.up.value if self._pitch < 0 else self.down.value if self._pitch > 0 else 0

    @property
    def isActive(self):
        # type: () -> bool
        return self.left.isActive or self.right.isActive \
            or self.up.isActive or self.down.isActive 