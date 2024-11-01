from .environment import environment

class HeadJoystickDirection:
    
    def __init__(self, maxDegrees , maxValue, deadZones = [0], antiDeadZone = 0):
        # type: (int, float, List[float]) -> None
        """
        Initializes the VRHeadJoy object.
        Args:
            maxDegrees (int): Maximum degrees of head rotation.
            antiDeadZone (float): Minimum value for axis output.(0-1). Defaults to 0.
            maxValue (float): Maximum value for axis axis.
            deadZones (List[float], optional): List of dead zone values (0-1). Defaults to [0].        
        """
        
        
        self.currentDegrees = 0      # stores the current degrees of head rotation
        self.maxDegrees = maxDegrees # Maximum degrees of head rotation
        self.antiDeadZone = abs(antiDeadZone)     # Maximum value for joystick axis
        self.maxValue = maxValue     # Maximum value for joystick axis
        self._deadZones = deadZones 
        self._currentDeadZoneIndex = 0 
    
    # get deadZone by index
    @property
    def deadZone(self):
        # type: () -> float
        return self._deadZones[self._currentDeadZoneIndex]
    
    # add a getter property for currentDeadZone
    @property
    def currentDeadZoneIndex(self):
        # type: () -> int
        return self._currentDeadZoneIndex
    
    # add a setter property for currentDeadZone
    @currentDeadZoneIndex.setter
    def currentDeadZoneIndex(self, value):
        #type: (int) -> None    
        if value < 0:
            self._currentDeadZoneIndex = 0
        elif value >= len(self._deadZones):
            self._currentDeadZoneIndex = len(self._deadZones) - 1
        else:
            self._currentDeadZoneIndex = value
    
    @property
    def value(self):
        # type: () -> float
        minDegrees = self.maxDegrees * self.deadZone
        if self.maxDegrees >= 0:
            return environment.filters.ensureMapRange(self.currentDegrees, minDegrees, self.maxDegrees, self.antiDeadZone, self.maxValue)
        else:
            return environment.filters.ensureMapRange(self.currentDegrees, self.maxDegrees, minDegrees, self.maxValue, -self.antiDeadZone)

    @property
    def isActive(self):
    # type: (float) -> bool
        return abs(self.currentDegrees) > (abs(self.maxDegrees) * self.deadZone)
        
    
class HeadJoystick:
    
    def __init__(self):
        #self.bJoyLookEnabled = False
        self.left  = HeadJoystickDirection(-40,-1)  
        self.right = HeadJoystickDirection( 40, 1) 
        self.up    = HeadJoystickDirection(-25,-1) 
        self.down  = HeadJoystickDirection( 25, 1) 
        self._yaw = 0
        self._pitch = 0
        
    def update(self):
        # type: () -> None
        self._yaw = environment.vr.headPose.yaw
        self._pitch = environment.vr.headPose.pitch
        
        self.left.currentDegrees = self._yaw
        self.right.currentDegrees = self._yaw
        self.up.currentDegrees = self._pitch
        self.down.currentDegrees = self._pitch
    
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