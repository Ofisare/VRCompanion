from .haptics import HapticsGroup
from .mode_based_actions import Mode
from .basic_actions import Action
from .key_actions import KeyAction

#******************************************
# an item to be placed inside an inventory
# with optional custom haptic feedback
#******************************************
class Item:
    def __init__(self, trackFireWeapon = True, trackMeleeRight = False, haptics = None, name = None):
        self.trackFireWeapon = trackFireWeapon
        self.trackMeleeRight = trackMeleeRight
        
        if haptics == None:
            self.haptics = HapticsGroup()
        else:
            self.haptics = haptics
        
        self.name = name

#**********************************************************************************
# the current loadout of items, a map to access them by name and the selected item
#**********************************************************************************
class Inventory(Mode):
    def __init__(self):
        Mode.__init__(self)
        self._items = dict()
        self._keys = dict()
        self.current = 0
        
    def get(self):
        return self._items.get(self.current)
    
    def getKeys(self):
        return self._keys.get(self.current)
    
    def getKey(self, itemName):
        for k, item in self._items.iteritems():
            if item != None and item.name == itemName:
                return k
                
        return None
    
    def set(self, key, item):
        self._items[key] = item
        
    def setKeys(self, key, keys):
        self._keys[key] = keys


#***************************************************
# Action to select a specific inventory item/weapon
#***************************************************
class InventorySelect(Action):
    def __init__(self, inventory, item):
        Action.__init__(self)
        self._inventory = inventory
        self._item = item
        
    def enter(self, currentTime, fromVoiceRecognition):
        self._inventory.current = self._item

#***********************************************************
# Action to select a specific inventory item/weapon by name
# and then press the according button if provided
#***********************************************************
class InventoryByNameSelect(KeyAction):
    def __init__(self, inventory, itemName):
        KeyAction.__init__(self, None)
        self._inventory = inventory
        self._itemName = itemName
        
    def enter(self, currentTime, fromVoiceRecognition):    
        self._inventory.current = self._inventory.getKey(self._itemName)
        
        keys = self._inventory.getKeys()
        if keys != None:
            self._keys = []
            # append or extend (both are valid)
            if isinstance(keys, list):
                self._keys.extend(keys)
            else:
                self._keys.append(keys)
            self.setKeyPressed()

#******************************************************************************
# An action to replace the feedback for the current item.
# This can be used in more dynamic games, where weapons/items can be replaced.
#******************************************************************************
class InventoryReplace(Action):
    def __init__(self, inventory, feedback):
        Action.__init__(self)
        self._inventory = inventory
        self._feedback = feedback
        
    def enter(self, currentTime, fromVoiceRecognition):
        self._inventory.set(self._inventory.current, self._feedback)
