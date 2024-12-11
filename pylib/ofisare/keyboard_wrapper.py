class KeyboardWrapper:
    def __init__(self, keyboard):
        self.keyboard = keyboard
        self.keys = {}
    
    def getKey(self, key):
        return self.keyboard.getKey(key)
    
    def setKey(self, key, down):
        if down:
            if key not in self.keys or self.keys[key] == 0:
                self.keys[key] = 1
                self.keyboard.setKey(key, True)
            else:
                self.keys[key] = self.keys[key] + 1
        else:
            if key not in self.keys:
                return
                
            if self.keys[key] > 1:
                self.keys[key] = self.keys[key] - 1
            else:
                self.keys[key] = 0
                self.keyboard.setKey(key, False)
    
    def wasTapped(self, key):
        return self.keyboard.wasTapped(key)
    
    def tapKey(self, key):
        self.setKeyDown(key)
        self.setKeyUp(key)