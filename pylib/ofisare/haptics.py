#***************************************************************
# a container to group haptics for different interaction states
#***************************************************************
class HapticsGroup:
    def __init__(self, enter = None, hold = None, leave = None, touchEnter = None, touchHold = None, touchLeave = None):
        self.enter = enter
        self.hold = hold
        self.leave = leave
        
        self.touchEnter = touchEnter
        self.touchHold = touchHold
        self.touchLeave = touchLeave