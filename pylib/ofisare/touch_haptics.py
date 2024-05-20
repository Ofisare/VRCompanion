from .environment import environment

#*********************************************************
# class to describe a sample for the controller vibration
#*********************************************************
class TouchHapticsSample:
    def __init__(self, frequency, amplitude):
        self.frequency = frequency
        self.amplitude = amplitude
        
#*****************************************************************
# class to describe a vibration pattern for a specific controller
#*****************************************************************
class TouchHaptics:
    def __init__(self, left, samples):
        self.left = left
        self.samples = samples

#*******************************************************************************************
# class to play vibration patterns, for each controller only one pattern can play at a time
#*******************************************************************************************
class TouchHapticsPlayer:
    def __init__(self):
        self._left = []
        self._right = []
    
    def play(self, haptics):
        if haptics.left:
            if len(self._left) == 0:
                self._left.extend(haptics.samples)
                # add an empty final event in case oculus is working again
                self._left.append(TouchHapticsSample(0, 0))
        else:
            if len(self._right) == 0:
                self._right.extend(haptics.samples)
                # add an empty final event in case oculus is working again
                self._right.append(TouchHapticsSample(0, 0))
    
    def update(self, deltaTime):
        if len(self._left) > 0:            
            left = self._left.pop(0)
            environment.openVR.triggerHapticPulse(0, deltaTime, left.frequency, left.amplitude)
            
        if len(self._right) > 0:
            right = self._right.pop(0)
            environment.openVR.triggerHapticPulse(1, deltaTime, right.frequency, right.amplitude)

    # some patterns
    def pulse(self, length, intensity):               
        count = (int)(length / (5 * environment.updateFrequency))
        haptics = []
        for x in range(count):
            haptics.append(TouchHapticsSample(1, intensity * x / count))
        
        for x in range(3*count):
            haptics.append(TouchHapticsSample(1, intensity))
            
        for x in range(count):
            haptics.append(TouchHapticsSample(1, intensity * (1 - x / count)))
        
        return haptics
        
    def pulseWithPause(self, length, intensity, pauseLength):
        global UpdateFrequency
        
        count = (int)(length / environment.updateFrequency)
        haptics = self.pulse(length, intensity)
        for x in range(count):
            haptics.append(TouchHapticsSample(1, 0))
        
        return haptics