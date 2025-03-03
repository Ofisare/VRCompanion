from .environment import environment
from .time_based_actions import ActionSequence, ActionRepeat
from .dispatcher import DispatchAction

# ****************************************
# Class to handle voice command execution
# ****************************************
class VoiceCommand:
    def __init__(self, cmd, action, haptics):
        self.cmd = cmd
        if isinstance(action, ActionSequence) or isinstance(action, ActionRepeat):
            self.action = DispatchAction(action, action.duration)
        elif isinstance(action, DispatchAction):
            self.action = action
        else:
            self.action = DispatchAction(action, 0.035)
        self.haptics = haptics
        
    def said(self, confidence):
        return (self.cmd != "") and environment.speech.said(self.cmd, confidence)
     
    def playHaptics(self, currentTime):    
        if environment.hapticPlayer != None and self.haptics != None:
            environment.hapticPlayer.play_registered(currentTime, self.haptics)
        
    def execute(self, currentTime):
        if self.action:
            self.action.enter(currentTime)
        
    def reset(self):
        if self.action:
            self.action.reset()
                        
#********************************************
# Engine to handle and update voice commands
#********************************************
class VoiceCommands:
    def __init__(self, confidenceLevel = 0.7):
        self.confidenceLevel = confidenceLevel
        self.commands = []

    def addCommand(self, cmd, action = None, haptics = None):
        self.commands.append( VoiceCommand(cmd, action, haptics) )

    def update(self, currentTime):
        for command in self.commands:
            # if said execute action
            if command.said(self.confidenceLevel):
                command.playHaptics(currentTime)
                command.execute(currentTime)

    def reset(self):
        for command in self.commands:
            command.reset()