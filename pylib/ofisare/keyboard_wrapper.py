class KeyboardWrapper:
    def __init__(self, keyboard):
        self.keyboard = keyboard
        self.keys = {}
        
    def setKeyDown(self, key):
        if key not in self.keys or self.keys[key] == 0:
            self.keys[key] = 1
            self.keyboard.setKeyDown(key)
        else:
            self.keys[key] = self.keys[key] + 1
        
    def setKeyUp(self, key):
        if key not in self.keys:
            return
            
        if self.keys[key] > 1:
            self.keys[key] = self.keys[key] - 1
        else:
            self.keys[key] = 0
            self.keyboard.setKeyUp(key)
    
    def setPressed(self, key):
        self.setKeyDown(key)
        self.setKeyUp(key)