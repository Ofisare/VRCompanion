from .environment import environment

# ****************************************
# Class to handle voice command execution
# ****************************************
class VoiceCommand:
    def __init__(self, cmd, action, haptics):
        self.cmd = cmd
        self.action = action
        self.haptics = haptics
        
    def said(self, confidence):
        return ((self.cmd != "") and environment.speech.said(self.cmd, confidence))
     
    def playHaptics(self, currentTime):    
        if environment.hapticPlayer != None and self.haptics != None:
            environment.hapticPlayer.play_registered(currentTime, self.haptics)
        
    def execute(self, currentTime):
        if self.action:
            self.action.enter(currentTime, True)
            
    def update(self, currentTime):
        if self.action:
            self.action.update(currentTime)
    
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
            # update command (hold with duration, multi/auto fire)
            command.update(currentTime)
        
    def reset(self):
        for command in self.commands:
            command.reset()