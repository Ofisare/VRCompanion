from .environment import environment

class HeadJoystickDirection:
    

    def __init__(self, degrees , joyValue, deadZones = [0]):
        # type: (int, float, List[float]) -> None
        
        self.degrees = degrees # Maximum degrees of head rotation
        self.value = joyValue   # Maximum value for joystick axis     
        
        
        self._deadZones = deadZones 
        self._currentDeadZone = 0
    
    @property
    def deadZone(self):
        # type: () -> float
        return self._deadZones[self._currentDeadZone]
    
    # add a getter property for currentDeadZone
    @property
    def currentDeadZone(self):
        # type: () -> int
        return self._currentDeadZone
    
    # add a setter property for currentDeadZone
    @currentDeadZone.setter
    def currentDeadZone(self, value):
        #type: (int) -> None    
        if value < 0:
            self._currentDeadZone = 0
        elif value >= len(self._deadZones):
            self._currentDeadZone = len(self._deadZones) - 1
        else:
            self._currentDeadZone = value
    
    def isActive(self, headValue):
    # type: (float) -> bool
        return abs(headValue or 0) > self.deadZone
        
    
class HeadJoystick:
    
    def __init__(self):
        #self.bJoyLookEnabled = False
        self.left  = HeadJoystickDirection(-40,-1)  
        self.right = HeadJoystickDirection( 40, 1) 
        self.up    = HeadJoystickDirection(-25,-1) 
        self.down  = HeadJoystickDirection( 25, 1) 
    
    @property
    def yaw(self):
        #type: () -> float
        return environment.vr.headPose.yaw
    
    @property
    def pitch(self):
        #type: () -> float
        return environment.vr.headPose.pitch

    @property
    def x(self):
        #type: () -> float
        return environment.filters.ensureMapRange(self.yaw, self.left.degrees, self.right.degrees, self.left.value, self.right.value)
    
    @property
    def y(self):
        #type: () -> float
        return environment.filters.ensureMapRange(self.pitch, self.up.degrees, self.down.degrees, self.up.value, self.down.value)

    def isActive(self):
    # type: (float) -> bool
        return self.left.isActive(self.x) or self.right.isActive(self.x) \
                        or self.up.isActive(self.y) or  self.down.isActive(self.y) 