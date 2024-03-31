# This scripts adds additional buttons (keyboard, mouse and gamepad) by natural gestures and voice commands.
# Furthermore, all controller inputs can be mapped directly as well.
# Additionally, interactions can be enhanced by bhaptics and controller feedback.
# While no feedback of the game logic is possible (like being hit), weapon recoil etc. might be simulated
# by observing the corresponding actions (track controller movement for melee swings, the trigger press
# for gun recoil etc.).
# Configurations are done using profile files, see scripts/profiles/#How to define a profile.txt
#
# After starting, a small launcher will be shown to select a game profile.
# The last settings are remembered in scripts/vr_companion.json
# Using the console version, you can then create shortcuts to instantly start a specific profile without the launcher.
# I.e.: FreePIE.Console.exe .\scripts\vr_companion.py TerminatorResistance
#
# Under "Settings > Plugins > Open VR" you can switch the vr engine to be used:
# - OpenVR: most compatible
# - Oculus: only for Oculus Rift (s) and Meta Quest connected via Cable and possibly Air Link (controller haptics might not be working)
#
#
# Feature Overview:
####################
#
# Gestures
# --------
# There are 3 gun poses (pistol: both hands close together, rifle: left or right hand in front of the other hand).
# The gun poses can press certain buttons to activate for instance ingame aiming for higher accuracy or toggle modes
# to allow adding multiple functions to the same button in a context aware scenario.
# Additional poses:
# - leaning of the head (left and right)
# - two use gestures (left and right hand): rotate the palm of the hand facing down
# - two "light" gestures (left and right hand): move the hand close to the side of the head
# - melee gesture for left and right: fast hand movement
# - alternate left melee gestures: fast hand movement while pointing up separated into push (hand palm pointing away from head), pull (hand palm pointing towards head) and everything else
# - 8 inventory/weapon gestures (left and right): move hand close to left/right shoulder or hip
# - 6 controller buttons (a,b,x,y,left and right stick), left/right trigger and grip are also available as "gestures" to allow usage of the same functionality
# - 2 location based gestures for mode shifting (left and right): move hands up zo enter location, good for differentiating between melee (low) and grenade throw (high)
#
# Validation: all gestures can activate when entering it or with an additional validation step, such as a short delay to not accidentally activating a gesture
# or the requirement to press the grip or trigger (more immersive for inventory gestures).
#
# Voice commands
# --------------
# They work on detecting phrases to execute a timely limited action whereas gesture based action
# might be executed as long as you are within the gesture.
#
# VR to Mouse/Gamepad
# -------------------
# Headset or controller movement can be mapped directly to mouse movement.
# Controller sticks and trigger can be directly mapped to gamepad sticks, dpads and triggers.
# All these mapping use the mode functionality, so they can be switched easily during gameplay
# with matching gesture interactions or button presses.
#
# Bhaptics and Controller Haptics Feedback
# -----------------------------------------
# With each gesture or voice command a bhaptics/controller feedback can be associated (currently only provide files for the vest as I can't test more).
# Interaction/weapon feedback is also possible, without actually triggering an ingame action.
#
# Inventory Management
# --------------------
# To have the correct weapon sounds. There is a limited inventory system to keep track of
# the selected and available weapons to have the right bhaptics feedbacks.
# For this it is best to use voice commands to select the correct weapon.
# Next and previous button presses often skip unavailable weapons, which this script cannot track.
#
#
# Poor Mans VR:
# -------------
# This script also enables head aiming for non vr games by mapping head rotation to mouse movement.
# If you use a compatible Reshade version (latest tested 6.0.1 with installed freepie addon)
# you can also enable controller based aiming. In this case this script communicates the difference
# in yaw and pitch between head and controller to the DetachedAiming* reshade shader. This shader
# then rotates the view so the crosshair "follows" the controller. Larger rotations will lead to black
# spaces as only what is rendered can be used.
# It also supports stereo output such as Super Depth 3D, just put the DetachedAiming_pixel at the end, so it can rotate
# the two individual images.
# Depending on the DirectX Version you might have to check flip pitch and or roll to get the
# correct movement of the image according to controller movement
#
# acknoweledgements:
# - voice recognitation adapted from https://github.com/NoxWings/FreePie-Scripts
# - vr support based on special build from https://github.com/Ofisare/FreePIE/releases/tag/OpenVR_v0.2
# - bhaptics integration based on https://github.com/bhaptics/tact-python
#
#
# Further reading of this script should not be required, but feel free to explore the magic.
#

import time
import math
import sys

try:
    from bhaptics import HapticPlayer
    skipBhaptics = False
except ImportError:
    skipBhaptics = True
    pass

#*********************
# geometry operations 
#*********************
class Vector:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z

def getYawPitch(pose):
    yaw = math.atan2(pose.forward.z, pose.forward.x)
    pitch = math.asin(pose.forward.y)
    
    return yaw, pitch

def getYawPitchRoll(pose):
    yaw = math.atan2(pose.forward.z, pose.forward.x)
    pitch = math.asin(pose.forward.y)    
    planeRightX = math.sin(yaw);
    planeRightZ = -math.cos(yaw);
    roll = math.asin(max(-1, min(1, pose.up.x * planeRightX + pose.up.z * planeRightZ)))    
    return yaw, pitch, roll

def getRoll(pose):
    yaw = math.atan2(pose.forward.z, pose.forward.x)
    planeRightX = math.sin(yaw);
    planeRightZ = -math.cos(yaw);
    return math.asin(max(-1, min(1, pose.up.x * planeRightX + pose.up.z * planeRightZ)))
    
def dotProduct(vector1, vector2):
    return vector1.x*vector2.x + vector1.y*vector2.y + vector1.z*vector2.z

#**********************
# Inventory managament
#**********************
class HapticsGroup:
    def __init__(self, enter = None, hold = None, leave = None, touchEnter = None, touchHold = None, touchLeave = None):
        self.enter = enter
        self.hold = hold
        self.leave = leave
        
        self.touchEnter = touchEnter
        self.touchHold = touchHold
        self.touchLeave = touchLeave

class Item:
    def __init__(self, trackFireWeapon = True, trackMeleeRight = False, haptics = None, name = None):
        self.trackFireWeapon = trackFireWeapon
        self.trackMeleeRight = trackMeleeRight
        
        if haptics == None:
            self.haptics = HapticsGroup()
        else:
            self.haptics = haptics
        
        self.name = name

class Inventory:
    def __init__(self):    
        self._items = [None] * 20
        self._keys = [None] * 20
        self.currentItem = 0
        
    def get(self):
        if self.currentItem < 0:
            return None
        if self.currentItem >= len(self._items):
            return None
        return self._items[self.currentItem]
    
    def getKeys(self):
        if self.currentItem < 0:
            return None
        if self.currentItem >= len(self._keys):
            return None
        return self._keys[self.currentItem]
    
    def indexOf(self, itemName):
        for i, item in enumerate(self._items):
            if item != None and item.name == itemName:
                return i
        return 0 # empty item
    
    def set(self, index, item):
        if index < 0:
            return
        if index >= len(self._items):
            return
        self._items[index] = item
        
    def setKeys(self, index, keys):
        if index < 0:
            return
        if index >= len(self._keys):
            return
        self._keys[index] = keys

#*******************************************
# Base class to handle gesture/voice action
#*******************************************
class Action:
    def __init__(self):        
        self.haptics = None

    def getCurrentHaptics(self):
        return self.haptics

    def enter(self, currentTime, fromVoiceRecognition):
        pass
    
    def update(self, currentTime):
        pass
    
    def leave(self):
        pass
    
    def reset(self):
        pass

#*****************************************************
# Special class to combine multiple different actions
#*****************************************************
class MultiAction(Action):
    def __init__(self, actions):
        Action.__init__(self)
        self._actions = actions
       
    def getCurrentHaptics(self):
        for action in self._actions:
            haptics = action.getCurrentHaptics()
            if haptics != None:
                return haptics                
        return self.haptics
        
    def enter(self, currentTime, fromVoiceRecognition):
        for action in self._actions:
            action.enter(currentTime, fromVoiceRecognition)
    
    def update(self, currentTime):
        for action in self._actions:
            action.update(currentTime)
    
    def leave(self):
        for action in self._actions:
            action.leave()
    
    def reset(self):
        for action in self._actions:
            action.reset()

#***********************************************
# Action classes to handle sequences of actions
#***********************************************
class TimedAction:
    def __init__(self, action, duration):
        self.action = action
        self.duration = duration
        
class ActionSequence(Action):
    def __init__(self, actions):
        Action.__init__(self)
        self._actions = actions
        self._index = 0
        self._time = 0
        
    def getCurrentHaptics(self):
        if self._index < len(self._actions):
            haptics = self._actions[self._index].action.getCurrentHaptics() 
            if haptics != None:
                return haptics
        return self.haptics
        
    def enter(self, currentTime, fromVoiceRecognition):
        self._index = 0
        self._time = currentTime
        self._actions[self._index].action.enter(currentTime, False)
    
    def update(self, currentTime):
        if self._index >= len(self._actions):
            return
            
        if self._actions[self._index].duration > currentTime - self._time:
            self._actions[self._index].action.update(currentTime)
        else:
            self._actions[self._index].action.leave()
            self._index = self._index + 1
            self._time = currentTime
            if self._index < len(self._actions):
                self._actions[self._index].action.enter(currentTime, False)                
    
    def leave(self):
        if self._index < len(self._actions):
            self._actions[self._index].action.leave()
            
        self._index = 0
        self._time = 0
    
    def reset(self):
        for action in self._actions:
            action.action.reset()
        
        self._index = 0
        self._time = 0


#************************************
# Action class to repeat an action
#************************************
class ActionRepeat(Action):
    def __init__(self, action, times, actionDuration = 0.05, timeInterval = 0.2):
        Action.__init__(self)
        self._action = action
        self._times = times-1
        self._actionDuration = actionDuration        
        self._timeInterval = timeInterval
        
        #internally used variables
        self._timesLeft = 0
        self._active = False
        self._needUpdate = False
        
    def getCurrentHaptics(self):
        haptics = self._action.getCurrentHaptics() 
        if haptics != None:
            return haptics
        return self.haptics
    
    def enter(self, currentTime, fromVoiceRecognition):
        # activate action
        self._action.enter(currentTime, False)
        self._active = True
        
        # start the update timer
        self._time = currentTime
        self._needUpdate = True
        
        if fromVoiceRecognition and self._times == -1:
            self._timesLeft = 0
        else:
            self._timesLeft = self._times
            
    def update(self, currentTime):
        if self._needUpdate:
            elapsedTime = currentTime - self._time
            
            # update action
            if elapsedTime < self._actionDuration:
            	self._action.update(currentTime)
            # leave action
            else:
                self._action.leave()
                self._active = False
        
                # End the update if the last key has been released
                if (self._timesLeft == 0):
                    self._needUpdate = False
                    
                # check for end of pause
                if (elapsedTime >= self._timeInterval):
                    self._action.enter(currentTime, False)
                    self._active = True
                    
                    self._time = currentTime
                    if self._timesLeft > 0:
                        self._timesLeft = self._timesLeft - 1
        
    def leave(self):
        if self._active:
            self._action.leave()
            self._active = False
            self._needUpdate = False

    def reset(self):
        self.leave()

#**************************************************************
# Action class to differentiate between a short and long press 
#**************************************************************
class TimeBased(Action):
    def __init__(self, actions, duration = 0.25):
        Action.__init__(self)
        self._actions = actions
        self._duration = duration
        self._inLongAction = False
    
    def getCurrentHaptics(self):
        haptics = None
        if self._inLongAction:
            haptics = self._actions[1].getCurrentHaptics()
        else:
            haptics = self._actions[0].getCurrentHaptics()
            
        if haptics != None:
            return haptics
        return self.haptics
        
    def enter(self, currentTime, fromVoiceRecognition):
        if fromVoiceRecognition:
            raise Exception("Time based actions don't support voice commands")
    
        # start the update timer to be able to distinguish actions
        self._time = currentTime
        self._inLongAction = False
            
    def update(self, currentTime):
        if self._inLongAction:
            self._actions[1].update(currentTime)
        elif currentTime - self._time > self._duration:
            self._inLongAction = True
            self._actions[1].enter(currentTime, False)
        
    def leave(self):
        if self._inLongAction:
            self._actions[1].leave()
        else:
            self._actions[0].enter(self._time, False)
            self._actions[0].leave()
        self._inLongAction = False

    def reset(self):
        for action in self._actions:
            action.reset()
        self._inLongAction = False

#******************************
# Mode switching functionality
#******************************
class Mode:
    def __init__(self):
        self.current = 0

class ModeBasedAction(Action):
    def __init__(self, mode, actions):
        Action.__init__(self)
        self._mode = mode
        self._actions = actions
        self._activeMode = mode.current
        self._fromVoiceRecognition = False

    def getCurrentHaptics(self):
        haptics = self._actions[self._mode.current].getCurrentHaptics()            
        if haptics != None:
            return haptics            
        return self.haptics

    def enter(self, currentTime, fromVoiceRecognition):
        self._actions[self._mode.current].enter(currentTime, fromVoiceRecognition)
        self._activeMode = self._mode.current
        self._fromVoiceRecognition = fromVoiceRecognition
    
    def update(self, currentTime):
        if self._mode.current == self._activeMode:
            self._actions[self._mode.current].update(currentTime)
        else:
            self._actions[self._activeMode].leave()
            self._activeMode = self._mode.current
            self._actions[self._mode.current].enter(currentTime, self._fromVoiceRecognition)
    
    def leave(self):
        if self._mode.current != self._activeMode:
            self._actions[self._activeMode].leave()            
        self._actions[self._mode.current].leave()
    
    def reset(self):
        for action in self._actions:
            action.reset()

class ModeSwitch(Action):
    def __init__(self, mode, selectedMode):
        Action.__init__(self)
        self._mode = mode
        self._selectedMode = selectedMode
        
    def enter(self, currentTime, fromVoiceRecognition):
        self._mode.current = self._selectedMode

#---------------------------------------------------------------------
# Action to set the mode when entering and resetting it when leaving.
# An exit mode can also be set instead of using the one which was
# active when entering.
#---------------------------------------------------------------------
class ModeSwitchWithReset(Action):
    def __init__(self, mode, selectedMode, resetMode = -1):
        Action.__init__(self)
        self._mode = mode
        self._selectedMode = selectedMode
        self._resetMode = resetMode
        self._lastMode = mode.current
        
    def enter(self, currentTime, fromVoiceRecognition):
        self._lastMode = self._mode.current # remember last mode to reset
        self._mode.current = self._selectedMode
    
    def leave(self):
        if self._resetMode == -1:
            self._mode.current = self._lastMode
        else:
            self._mode.current = self._resetMode

#************************************
# Base class for mouse based actions
#************************************
class MouseAction(Action):
    def __init__(self, keys):
        Action.__init__(self)
        self._keys = []
        if keys != None:
            # append or extend (both are valid)
            if isinstance(keys, list):
                self._keys.extend(keys)
            else:
                self._keys.append(keys)
        self._duration = 0.035
        self._time = time.time()
        self._needUpdate = False
    
    def setKeyDown(self):
        for key in self._keys:
            if key == -1:
                mouse.wheelDown = True
            elif key == -2:
                mouse.wheelUp = True
            else:
                mouse.setButton(key, True)
        
    def setKeyUp(self):
        for key in self._keys:
            if key == -1:
                mouse.wheelDown = False
            elif key == -2:
                mouse.wheelUp = False
            else:
                mouse.setButton(key, False)
    
    def setKeyPressed(self):
        for key in self._keys:
            if key == -1:
                mouse.wheelDown = True
                mouse.wheelDown = False
            elif key == -2:
                mouse.wheelUp = True
                mouse.wheelUp = False
            else:
                mouse.setButton(key, True)
                mouse.setButton(key, False)

#****************************************************************
# Action class to press and release a mouse button when entering 
#****************************************************************
class MouseQuickPress(MouseAction):
    def __init__(self, keys):
        MouseAction.__init__(self, keys)
        
    def enter(self, currentTime, fromVoiceRecognition):
        self.setKeyPressed()

#**************************************************
# Action class to handle single mouse button press 
#**************************************************
class MousePress(MouseAction):
    def __init__(self, keys):
        MouseAction.__init__(self, keys)
        
    def enter(self, currentTime, fromVoiceRecognition):
        # set the keys down
        self.setKeyDown()
        # start the update timer to auto release when from voice activation
        self._time = currentTime
        self._needUpdate = fromVoiceRecognition
            
    def update(self, currentTime):
        if self._needUpdate:
            # determine if we should stop pressing the keys
            if (currentTime - self._time) >= self._duration:
                self.leave()

    def leave(self):
        self.setKeyUp()
        self._needUpdate = False

    def reset(self):
        self.leave()

#****************************************************************
# Action class to press a mouse button when entering and leaving 
#****************************************************************
class MouseToggle(MouseAction):
    def __init__(self, keys):
        MouseAction.__init__(self, keys)
        
    def enter(self, currentTime, fromVoiceRecognition):
        self.setKeyPressed()
            
    def leave(self):
        self.setKeyPressed()

#******************************************************************
# Action class to change the state of a mouse button when entering 
#******************************************************************
class MouseSwitchState(MouseAction):
    def __init__(self, keys):
        MouseAction.__init__(self, keys)
        self._down = False
        
    def enter(self, currentTime, fromVoiceRecognition):
        if self._down:
            self.setKeyUp()
            self._down = False
        else:
            self.setKeyDown()
            self._down = True
    
    def reset(self):
        self.setKeyUp()
        self._down = False

#**********************************
# Base class for key based actions
#**********************************
class KeyAction(Action):
    def __init__(self, keys):
        Action.__init__(self)
        self._keys = []
        if keys != None:
            # append or extend (both are valid)
            if isinstance(keys, list):
                self._keys.extend(keys)
            else:
                self._keys.append(keys)
        self._duration = 0.035
        self._time = time.time()
        self._needUpdate = False
    
    def setKeyDown(self):
        for key in self._keys:
            keyboard.setKeyDown(key)    
        
    def setKeyUp(self):
        for key in self._keys:
            keyboard.setKeyUp(key)    
    
    def setKeyPressed(self):
        for key in self._keys:
            keyboard.setPressed(key)

#********************************************************
# Action class to press and releases a key when entering
#********************************************************
class KeyQuickPress(KeyAction):
    def __init__(self, keys):
        KeyAction.__init__(self, keys)
        
    def enter(self, currentTime, fromVoiceRecognition):
        self.setKeyPressed()

#****************************************************************************************
# Action class to handle press a key when entering and holding until it leaves a gesture 
#****************************************************************************************
class KeyPress(KeyAction):
    def __init__(self, keys):
        KeyAction.__init__(self, keys)
        
    def enter(self, currentTime, fromVoiceRecognition):
        # set the keys down
        self.setKeyDown()
        # start the update timer to auto release when from voice activation
        self._time = currentTime
        self._needUpdate = fromVoiceRecognition
            
    def update(self, currentTime):
        if self._needUpdate:
            # determine if we should stop pressing the keys
            if (currentTime - self._time) >= self._duration:
                self.leave()

    def leave(self):
        self.setKeyUp()
        self._needUpdate = False

    def reset(self):
        self.leave()

#*******************************************************
# Action class to press a key when entering and leaving 
#*******************************************************
class KeyToggle(KeyAction):
    def __init__(self, keys):
        KeyAction.__init__(self, keys)
        
    def enter(self, currentTime, fromVoiceRecognition):
        self.setKeyPressed()
            
    def leave(self):
        self.setKeyPressed()
        
#*********************************************************
# Action class to change the state of a key when entering 
#*********************************************************
class KeySwitchState(KeyAction):
    def __init__(self, keys):
        KeyAction.__init__(self, keys)
        self._down = False
        
    def enter(self, currentTime, fromVoiceRecognition):
        if self._down:
            self.setKeyUp()
            self._down = False
        else:
            self.setKeyDown()
            self._down = True
    
    def reset(self):
        self.setKeyUp()
        self._down = False
        
#**************************************
# Base class for gamepad based actions
#**************************************
class GamepadAction(Action):
    def __init__(self, keys):
        Action.__init__(self)
        self._keys = []
        if keys != None:
            # append or extend (both are valid)
            if isinstance(keys, list):
                self._keys.extend(keys)
            else:
                self._keys.append(keys)
        self._duration = 0.035
        self._time = time.time()
        self._needUpdate = False
    
    def setKeyDown(self):
        global vrToGamepad
        for key in self._keys:
            vigem.SetButtonState(vrToGamepad.controller, key, True)
        
    def setKeyUp(self):
        global vrToGamepad
        for key in self._keys:
            vigem.SetButtonState(vrToGamepad.controller, key, False) 

#**********************************************************
# Action class to press and releases a key when "entering"
# vigem has no pressed state, so it has to be active for a
# short duration instead.
#**********************************************************
class GamepadQuickPress(GamepadAction):
    def __init__(self, keys):
        GamepadAction.__init__(self, keys)
        
    def enter(self, currentTime, fromVoiceRecognition):
        # set the keys down
        self.setKeyDown()
        # start the update timer to auto release when from voice activation
        self._time = currentTime
        self._needUpdate = True
            
    def update(self, currentTime):
        if self._needUpdate:
            # determine if we should stop pressing the keys
            if (currentTime - self._time) >= self._duration:
                self.leave()

    def leave(self):
        self.setKeyUp()
        self._needUpdate = False

    def reset(self):
        self.leave()

#****************************************************************************************
# Action class to handle press a key when entering and holding until it leaves a gesture 
#****************************************************************************************
class GamepadPress(GamepadAction):
    def __init__(self, keys):
        GamepadAction.__init__(self, keys)
        
    def enter(self, currentTime, fromVoiceRecognition):
        # set the keys down
        self.setKeyDown()
        # start the update timer to auto release when from voice activation
        self._time = currentTime
        self._needUpdate = fromVoiceRecognition
            
    def update(self, currentTime):
        if self._needUpdate:
            # determine if we should stop pressing the keys
            if (currentTime - self._time) >= self._duration:
                self.leave()

    def leave(self):
        self.setKeyUp()
        self._needUpdate = False

    def reset(self):
        self.leave()

#*******************************************************
# Action class to press a key when entering and leaving 
#*******************************************************
class GamepadToggle(GamepadAction):
    def __init__(self, keys):
        GamepadAction.__init__(self, keys)
        
    def enter(self, currentTime, fromVoiceRecognition):
        self.setKeyPressed()
            
    def leave(self):
        self.setKeyPressed()
        
#*********************************************************
# Action class to change the state of a key when entering 
#*********************************************************
class GamepadSwitchState(GamepadAction):
    def __init__(self, keys):
        GamepadAction.__init__(self, keys)
        self._down = False
        
    def enter(self, currentTime, fromVoiceRecognition):
        if self._down:
            self.setKeyUp()
            self._down = False
        else:
            self.setKeyDown()
            self._down = True
    
    def reset(self):
        self.setKeyUp()
        self._down = False

#***************************************************
# Action to select a specific inventory item/weapon
#***************************************************
class InventorySelect(Action):
    def __init__(self, inventory, item):
        Action.__init__(self)
        self._inventory = inventory
        self._item = item
        
    def enter(self, currentTime, fromVoiceRecognition):
        self._inventory.currentItem = self._item

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
        self._inventory.currentItem = self._inventory.indexOf(self._itemName)
        
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
        self._inventory.set(self._inventory.currentItem, self._feedback)


# ****************************************
# Class to handle voice command execution
# ****************************************
class VoiceCommand:
    def __init__(self, cmd, action, haptics):
        self.cmd = cmd
        self.action = action
        self.haptics = haptics
        
    def said(self, confidence):
        return ((self.cmd != "") and speech.said(self.cmd, confidence))
     
    def playHaptics(self, currentTime):
        global hapticPlayer
    
        if hapticPlayer != None and self.haptics != None:
            hapticPlayer.play_registered(currentTime, self.haptics)
        
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
class VoiceToKeyboard:
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

#****************************************************************
# Class to handle mouse movement based on headset or controller.
# Use its mode to steer mapping:
# - 0: No mouse output
# - 1: Headset to mouse
# - 2: Left controller to mouse
# - 3: Right controller to mouse
# - 4: right stick only
# Additionally, you can switch between using a controllers
# position or orientation (useControllerOrientation).
#****************************************************************
class VRToMouse:
    def __init__(self):
        self.mode = Mode()
        self.mouseSensitivityX = 800
        self.mouseSensitivityY = 800
        self.stickMultiplierX = 1
        self.stickMultiplierY = 1
        self.enableYawPitch = True
        self.enableRoll = False
        self.useControllerOrientation = True
        self.useRightController = True
        
        self._yaw = 0.0
        self._pitch = 0.0
        
        self._lastMode = 0
        self._yawOffset = 0.0
        self._pitchOffset = 0.0
        
    def update(self, currentTime, deltaTime):
        if self.mode.current == 0:
            if self._lastMode != 0:
                # reset settings
                self._lastMode = self.mode.current
                self._yawOffset = 0
                self._pitchOffset = 0
                # no mouse mapping
                freePieIO[0].yaw = 0
                freePieIO[0].pitch = 0
                freePieIO[0].roll = 0
            return

        yawTarget = self._yaw
        pitchTarget = self._pitch
        
        # get head orientation
        yawHead, pitchHead, rollHead = getYawPitchRoll(openVR.headPose)
        if self.mode.current == 1:
            yawTarget = yawHead
            pitchTarget = pitchHead            
        elif self.mode.current == 2:
            # left controller
            if self.useControllerOrientation:
                yaw, pitch = getYawPitch(openVR.leftTouchPose)
                yawTarget = yaw + self._yawOffset
                pitchTarget = pitch + self._pitchOffset
            else:
                dx = openVR.leftTouchPose.position.x - openVR.headPose.position.x
                dy = openVR.leftTouchPose.position.y - openVR.headPose.position.y
                dz = openVR.leftTouchPose.position.z - openVR.headPose.position.z
                dh = math.sqrt(dx*dx + dz*dz)
                yawTarget = math.pi + math.atan2(dz, dx) + self._yawOffset
                pitchTarget = -math.atan2(dy, dh) + self._pitchOffset
        elif self.mode.current == 3:
            # right controller
            if self.useControllerOrientation:
                yaw, pitch = getYawPitch(openVR.rightTouchPose)
                yawTarget = yaw + self._yawOffset
                pitchTarget = pitch + self._pitchOffset
            else:
                dx = openVR.rightTouchPose.position.x - openVR.headPose.position.x
                dy = openVR.rightTouchPose.position.y - openVR.headPose.position.y
                dz = openVR.rightTouchPose.position.z - openVR.headPose.position.z
                dh = math.sqrt(dx*dx + dz*dz)
                yawTarget = math.pi + math.atan2(dz, dx) + self._yawOffset
                pitchTarget = -math.atan2(dy, dh) + self._pitchOffset
                
        if self._lastMode != self.mode.current:
            if self.mode.current == 1 and self._lastMode > 1:
                self._yawOffset = 0
                self._pitchOffset = 0
                yawChange = (yawHead - self._yaw) / 2
                pitchChange = (pitchHead - self._pitch) / 2
                self._yaw = yawHead
                self._pitch = pitchHead
            else:
                self._yawOffset = yawHead - yawTarget
                self._pitchOffset = pitchHead - pitchTarget
                yawChange = 0
                pitchChange = 0
                self._yaw = yawHead
                self._pitch = pitchHead
            self._lastMode = self.mode.current
        else:
            # apply offset and changes to view and mouse movement
            yawTarget = yawTarget
            pitchTarget = pitchTarget
            yawChange = yawTarget - self._yaw
            pitchChange = pitchTarget - self._pitch
            
            self._yaw = yawTarget
            self._pitch = pitchTarget
        
        if yawChange > math.pi:
            yawChange = yawChange - math.pi * 2
        elif yawChange < -math.pi:
            yawChange = yawChange + math.pi * 2
        
        diagnostics.watch(yawChange)
        
        deltaX = yawChange * self.mouseSensitivityX
        deltaY = pitchChange * self.mouseSensitivityY
        
        if self.useRightController:
        	deltaX = deltaX + openVR.rightStickAxes.x * self.mouseSensitivityX * self.stickMultiplierX * deltaTime
        	deltaY = deltaY - openVR.rightStickAxes.y * self.mouseSensitivityY * self.stickMultiplierY * deltaTime
        else:        
        	deltaX = deltaX + openVR.leftStickAxes.x * self.mouseSensitivityX * self.stickMultiplierX * deltaTime
        	deltaY = deltaY - openVR.leftStickAxes.y * self.mouseSensitivityY * self.stickMultiplierY * deltaTime
        	
        mouse.deltaX = deltaX
        mouse.deltaY = deltaY
        
        # communicate to reshade
        if self.enableYawPitch:
            freePieIO[0].yaw = yawHead - self._yaw
            freePieIO[0].pitch = pitchHead - self._pitch
        if self.enableRoll:
            freePieIO[0].roll = rollHead
        else:
            freePieIO[0].roll = 0

    def reset(self):
        # clear communication with reshade
        freePieIO[0].yaw = 0
        freePieIO[0].pitch = 0
        freePieIO[0].roll = 0

#************************************************
# Class to handle controller to gamepad mapping.
# Use its modes to steer mapping:
#  - leftTriggerMode and rightTriggerMode handle mapping from
#    controller to gamepad triggers
#  - leftStickMode and rightStickMode handle mapping from 
#    controller to gamepad sticks
#  - dpadMode handle mapping from controller sticks to dpad
# For all of those:
# - 0: No output
# - 1: Left trigger or stick
# - 2: Right trigger or stick
# For the dpad an additional dpadThreshold can be defined.
#************************************************
class VRToGamepad:
    def __init__(self):
        self.leftTriggerMode = Mode()
        self.rightTriggerMode = Mode()
        self.leftStickMode = Mode()
        self.rightStickMode = Mode()
        self.dpadMode = Mode()
        self.dpadThreshold = 0.3
        self.controller = None
    
    def setController(self, controllerType):
        self.controller = controllerType
        vigem.CreateController(self.controller)
        
    def update(self, currentTime):
        # map left trigger to left trigger
        if self.leftTriggerMode == 1:
            vigem.SetTrigger(self.controller, VigemSide.Left, openVR.leftTrigger)
        # map right trigger to left trigger
        elif self.leftTriggerMode == 2:
            vigem.SetTrigger(self.controller, VigemSide.Left, openVR.rightTrigger)
        
        # map right trigger to right trigger
        if self.rightTriggerMode == 1:
            vigem.SetTrigger(self.controller, VigemSide.Right, openVR.leftTrigger)
        # map left trigger to right trigger
        elif self.rightTriggerMode == 2:
            vigem.SetTrigger(self.controller, VigemSide.Right, openVR.rightTrigger)
        
        # map left stick to left stick
        if self.leftStickMode == 1:
            vigem.SetStick(self.controller, VigemSide.Left, openVR.leftStickAxes.x, openVR.leftStickAxes.y)
        # map right stick to left stick
        elif self.leftStickMode == 2:
            vigem.SetStick(self.controller, VigemSide.Left, openVR.rightStickAxes.x, openVR.rightStickAxes.y)
        
        # map right stick to right stick
        if self.rightStickMode == 1:
            vigem.SetStick(self.controller, VigemSide.Right, openVR.leftStickAxes.x, openVR.leftStickAxes.y)
        # map left stick to right stick
        elif self.rightStickMode == 2:
            vigem.SetStick(self.controller, VigemSide.Right, openVR.rightStickAxes.x, openVR.rightStickAxes.y)
            
        # map left stick to dpad
        if self.dpadMode == 1:
            vigem.SetDPad(self.controller, openVR.leftStickAxes.x, openVR.leftStickAxes.y, self.dpadThreshold)
        # map right stick to dpad
        elif self.dpadMode == 2:
            vigem.SetDPad(self.controller, openVR.rightStickAxes.x, openVR.rightStickAxes.y, self.dpadThreshold)
        
    def reset(self):
        pass
        
#*******************************************************************************************************
# Class to handle trigger or grip based validation of gestures and skip further uses of trigger or grip
#*******************************************************************************************************
class GestureValidation:
    def __init__(self, trigger, grip):
        self.trigger = trigger
        self.grip = grip
        
        self.triggerUsed = False
        self.gripUsed = False

#*****************************************************
# Class handling gesture actions and haptics feedback
#*****************************************************
class Gesture:
    # public members:
    # * action: the action to perform when in the gesture
    # * enabled: whether this gesture is active
    # * hapticsValidating: when hitting the right position but needing some time to confirm this interaction
    # * hapticsEnter: the haptics feedback when entering the gesture -> a one shot
    # * hapticsHold: the haptics when within the gesture -> a continuous feedback -> minigun/chainsaw
    # * hapticsLeave: the haptics when leaving the gesture
    
    def __init__(self, lowerThreshold, upperThreshold):
        self.lowerThreshold = lowerThreshold
        self.upperThreshold = upperThreshold
    
        self.validationMode = 0
        self.validationThreshold = 0.6
        self.validationTime = 0.5
        self._validationStartTime = 0
        
        self.haptics = HapticsGroup()
        self.validating = None
        self.touchValidating = None
        
        self.action = None
        self.triggerAction = None
        self.gripAction = None
        
        self.triggerLowerThreshold = 0.5
        self.triggerUpperThreshold = 0.6
        self.gripLowerThreshold = 0.5
        self.gripUpperThreshold = 0.6
        
        self.enabled = False
        self._inValidation = False
        self.inGesture = False
        self.inTriggerGesture = False
        self.inGripGesture = False
        
    def reset(self):
        if self.action != None:
            self.action.reset()
        if self.triggerAction != None:
            self.triggerAction.reset()
        if self.gripAction != None:
            self.gripAction.reset()
            
        self._inValidation = False
        self.inGesture = False
        self.inTriggerGesture = False
        self.inGripGesture = False
    
    def playHaptics(self, currentTime, haptics, touchHaptics):
        global hapticPlayer
        global touchHapticsPlayer
        
        if hapticPlayer != None and haptics != None:
            hapticPlayer.play_registered(currentTime, haptics)
        
        if touchHaptics != None:
            touchHapticsPlayer.play(touchHaptics)
   
    def _updateBaseGesture(self, currentTime, value, gestureValidation, haptics):
        # use action haptics
        if self.action != None:
            actionHaptics = self.action.getCurrentHaptics()
            if actionHaptics != None:
                haptics = actionHaptics
    
        # gesture entered, check whether to leave or stay in gesture
        if self.inGesture:
            if value > self.upperThreshold:
                self.playHaptics(currentTime, haptics.leave, haptics.touchLeave)
                if self.action != None:
                    self.action.leave()
                self.inGesture = False
            else:
                self.playHaptics(currentTime, haptics.hold, haptics.touchHold)
                if self.action != None:
                    self.action.update(currentTime)
        # check whether to enter gesture
        else:
            if value < self.lowerThreshold:
                valid = False
                # no validation required
                if self.validationMode == 0:
                    valid = True
                # delayed/time based validation
                elif self.validationMode == 1:
                    if self._inValidation:
                        valid = currentTime - self._validationStartTime > self.validationTime
                # trigger validation
                elif self.validationMode == 2:
                    valid = gestureValidation.triggerUsed == False and gestureValidation.trigger > self.validationThreshold
                # grip validation
                elif self.validationMode == 3:
                    valid = gestureValidation.gripUsed == False and gestureValidation.grip > self.validationThreshold
                
                # fially enter gesture if eveything is fine
                if valid:
                    self.playHaptics(currentTime, haptics.enter, haptics.touchEnter)
                    if self.action != None:
                        self.action.enter(currentTime, False)
                    self.inGesture = True
                
        # block other gestures from using trigger or grip
        if self.inGesture:
            # trigger validation
            if self.validationMode == 2:
                gestureValidation.triggerUsed = True
            # grip validation
            elif self.validationMode == 3:
                gestureValidation.gripUsed = True
    
    def _updateTriggerGesture(self, currentTime, value, gestureValidation, haptics):
        # use action haptics
        actionHaptics = self.triggerAction.getCurrentHaptics()
        if actionHaptics != None:
            haptics = actionHaptics
        
        # gesture entered, check whether to leave or stay in gesture
        if self.inTriggerGesture:
            if gestureValidation.triggerUsed == True or value > self.upperThreshold or gestureValidation.trigger < self.triggerLowerThreshold:
                self.playHaptics(currentTime, haptics.leave, haptics.touchLeave)    
                if self.triggerAction != None:
                    self.triggerAction.leave()
                self.inTriggerGesture = False
            else:
                self.playHaptics(currentTime, haptics.hold, haptics.touchHold)
                if self.triggerAction != None:
                    self.triggerAction.update(currentTime)
        # check whether to enter gesture
        else:
            if gestureValidation.triggerUsed == False and value < self.lowerThreshold and gestureValidation.trigger > self.triggerUpperThreshold:
                # enter gesture if eveything is fine
                self.playHaptics(currentTime, haptics.enter, haptics.touchEnter)
                if self.triggerAction != None:
                    self.triggerAction.enter(currentTime, False)
                self.inTriggerGesture = True
                
        # block other gestures from using trigger
        if self.inTriggerGesture:
            gestureValidation.triggerUsed = True
                    
    def _updateGripGesture(self, currentTime, value, gestureValidation, haptics):
        # use action haptics
        actionHaptics = self.gripAction.getCurrentHaptics()
        if actionHaptics != None:
            haptics = actionHaptics
        
        # gesture entered, check whether to leave or stay in gesture
        if self.inGripGesture:
            if gestureValidation.gripUsed == True or value > self.upperThreshold or gestureValidation.grip < self.gripLowerThreshold:
                self.playHaptics(currentTime, haptics.leave, haptics.touchLeave)
                if self.gripAction != None:
                    self.gripAction.leave()
                self.inGripGesture = False
            else:
                self.playHaptics(currentTime, haptics.hold, haptics.touchHold)
                if self.gripAction != None:
                    self.gripAction.update(currentTime)
        # check whether to enter gesture
        else:
            if gestureValidation.gripUsed == False and value < self.lowerThreshold and gestureValidation.grip > self.gripUpperThreshold:
                # enter gesture if eveything is fine
                self.playHaptics(currentTime, haptics.enter, haptics.touchEnter)
                if self.gripAction != None:
                    self.gripAction.enter(currentTime, False)
                self.inGripGesture = True
                
        # block other gestures from using trigger
        if self.inGripGesture:
            gestureValidation.gripUsed = True
    
    def _updateCore(self, currentTime, value, gestureValidation, haptics):
        # check gestures
        if self.action != None:
            self._updateBaseGesture(currentTime, value, gestureValidation, haptics)
        if self.triggerAction != None:
            self._updateTriggerGesture(currentTime, value, gestureValidation, haptics)
        if self.gripAction != None:
            self._updateGripGesture(currentTime, value, gestureValidation, haptics)
        
        # check for validation
        if self.inGesture or self.inTriggerGesture or self.inGripGesture:
            self._inValidation = False
        elif value < self.lowerThreshold:
            if not self._inValidation:
                self.playHaptics(currentTime, self.validating, self.touchValidating)
                self._inValidation = True
                self._validationStartTime = currentTime
        else:
            self._inValidation = False
        
    def update(self, currentTime, value, gestureValidation):
        self._updateCore(currentTime, value, gestureValidation, self.haptics)

#***************************************************************
# Special class using item feedback instead of gesture feedback
#***************************************************************
class InventoryGesture(Gesture):
    def __init__(self, lowerThreshold, upperThreshold, inventory):
        Gesture.__init__(self, lowerThreshold, upperThreshold)
        self._inventory = inventory

    def update(self, currentTime, value, gestureValidation):
        # use item feedback if available
        item = self._inventory.get()
        if item == None:
            self._updateCore(currentTime, value, gestureValidation, self.haptics)
        else:
            self._updateCore(currentTime, value, gestureValidation, item.haptics)


#***************************************
# Class tracking and executing gestures
#***************************************       
class GestureTracker:
    def __init__(self, inventory):
        self.aimPistol = Gesture(0.02, 0.03)                            # distance between both controllers
        self.aimRifleLeft = Gesture(-0.2, -0.1)                         # negative distance between left controller and head in xz plane
        self.aimRifleRight = Gesture(-0.2, -0.1)                        # negative distance between right controller and head in xz plane
        self.buttonA = Gesture(-0.8, -0.7)                              # negative press value of button a
        self.buttonB = Gesture(-0.8, -0.7)                              # negative press value of button b
        self.buttonX = Gesture(-0.8, -0.7)                              # negative press value of button x
        self.buttonY = Gesture(-0.8, -0.7)                              # negative press value of button y
        self.buttonLeftStick = Gesture(-0.8, -0.7)                      # negative press value of button left
        self.buttonLeftStickUp = Gesture(-0.2, -0.05)                   # negative left stick up
        self.buttonLeftStickDown = Gesture(-0.2, -0.1)                  # left stick up
        self.buttonLeftStickLeft = Gesture(-0.2, -0.1)                  # negative left stick right
        self.buttonLeftStickRight = Gesture(-0.2, -0.1)                 # left stick right
        self.buttonLeftStickInnerRing = Gesture(0.5, 0.5)               # left stick in center
        self.buttonLeftStickOuterRing = Gesture(-0.9, -0.9)             # negative left stick in outer area
        self.buttonRightStick = Gesture(-0.8, -0.7)                     # negative press value of button right
        self.buttonRightStickUp = Gesture(-0.2, -0.05)                  # negative right stick up
        self.buttonRightStickDown = Gesture(-0.2, -0.1)                 # right stick up
        self.buttonRightStickLeft = Gesture(-0.2, -0.1)                 # negative right stick right
        self.buttonRightStickRight = Gesture(-0.2, -0.1)                # right stick right
        self.buttonRightStickInnerRing = Gesture(0.5, 0.5)              # left stick in center
        self.buttonRightStickOuterRing = Gesture(-0.9, -0.9)            # negative left stick in outer area
        self.triggerLeft = Gesture(-0.6, -0.4)                          # negative left trigger press
        self.triggerRight = InventoryGesture(-0.6, -0.4, inventory)     # negative right trigger press
        self.gripLeft = Gesture(-0.6, -0.4)                             # negative left grip press
        self.gripRight = Gesture(-0.6, -0.4)                            # negative right grip press
        self.holsterInventoryLeft = Gesture(0.2, 0.3)                   # distance between left controller and left hip holster
        self.holsterInventoryRight = Gesture(0.2, 0.3)                  # distance between left controller and right hip holster
        self.holsterWeaponLeft = Gesture(0.2, 0.3)                      # distance between right controller and left hip holster
        self.holsterWeaponRight = Gesture(0.2, 0.3)                     # distance between right controller and right hip holster
        self.leanLeft = Gesture(-0.125, -0.1)                           # negative difference to normal head roll
        self.leanRight = Gesture(-0.125, -0.1)                          # negative difference to normal head roll
        self.lightLeft = Gesture(0.03, 0.05)                            # distance between left controller and head
        self.lightRight = Gesture(0.03, 0.05)                           # distance between right controller and head
        self.meleeLeft = Gesture(-5.0, -2.0)                            # negative speed from left controller
        self.meleeLeftAlt = Gesture(-5, -2.0)                           # negative speed from left controller, pointing upwards
        self.meleeLeftAltPull = Gesture(-5, -2.0)                       # negative speed from left controller, pointing upwards and away from head
        self.meleeLeftAltPush = Gesture(-5, -2.0)                       # negative speed from left controller, pointing upwards and towards head
        self.meleeRight = InventoryGesture(-5.0, -2.0, inventory)       # negative speed from right controller
        self.meleeRightAlt = InventoryGesture(-5, -2.0, inventory)      # negative speed from right controller, pointing upwards
        self.meleeRightAltPull = InventoryGesture(-5, -2.0, inventory)  # negative speed from right controller, pointing upwards and away from head
        self.meleeRightAltPush = InventoryGesture(-5, -2.0, inventory)  # negative speed from right controller, pointing upwards and towards head
        self.shoulderInventoryLeft = Gesture(0.1, 0.2)                  # distance between left controller and left shoulder
        self.shoulderInventoryRight = Gesture(0.1, 0.2)                 # distance between left controller and right shoulder
        self.shoulderWeaponLeft = Gesture(0.1, 0.2)                     # distance between right controller and left shoulder
        self.shoulderWeaponRight = Gesture(0.1, 0.2)                    # distance between right controller and right shoulder
        self.upperAreaLeft = Gesture(0.1, 0.2)                          # difference between head y - left controller y
        self.upperAreaRight = Gesture(0.1, 0.2)                         # difference between head y - right controller y
        self.useLeft = Gesture(-0.7, -0.5)                              # openVR.leftTouchPose.left.y, basically checking whether the left palm is facing down
        self.useRight = Gesture(-0.7, -0.5)                             # -openVR.rightTouchPose.left.y, basically checking whether the right palm is facing down
        
        self.holsterOffset = Vector(0.5, -0.6, -0.1)    # the offset from head to holster
        self.shoulderOffset = Vector(0.4, 0, -0.1)      # the offset from head to shoulder
        self.leftMeleeAltThreshold = -0.7               # the threshold for the forward vector y coordinate
        self.rightMeleeAltThreshold = -0.7              # the threshold for the forward vector y coordinate
                
        # aliases      
        self.fireWeaponLeft = self.triggerLeft
        self.fireWeaponRight = self.triggerRight        
        self.grabLeft = self.gripLeft
        self.grabRight = self.gripRight
        
        self._gestures = [
            self.aimPistol,
            self.aimRifleLeft,
            self.aimRifleRight,
            self.buttonA,
            self.buttonB,
            self.buttonX,
            self.buttonY,
            self.buttonLeftStick,
            self.buttonLeftStickUp,
            self.buttonLeftStickDown,
            self.buttonLeftStickLeft,
            self.buttonLeftStickRight,
            self.buttonLeftStickInnerRing,
            self.buttonLeftStickOuterRing,
            self.buttonRightStick,
            self.buttonRightStickUp,
            self.buttonRightStickDown,
            self.buttonRightStickLeft,
            self.buttonRightStickRight,
            self.buttonRightStickInnerRing,
            self.buttonRightStickOuterRing,
            self.triggerLeft,
            self.triggerRight,
            self.gripLeft,
            self.gripRight,
            self.holsterInventoryLeft,
            self.holsterInventoryRight,
            self.holsterWeaponLeft,
            self.holsterWeaponRight,
            self.leanLeft,
            self.leanRight,
            self.lightLeft,
            self.lightRight,
            self.meleeLeft,
            self.meleeLeftAlt,
            self.meleeLeftAltPull,
            self.meleeLeftAltPush,
            self.meleeRight,
            self.meleeRightAlt,
            self.meleeRightAltPull,
            self.meleeRightAltPush,
            self.shoulderInventoryLeft,
            self.shoulderInventoryRight,
            self.shoulderWeaponLeft,
            self.shoulderWeaponRight,
            self.upperAreaLeft,
            self.upperAreaRight,
            self.useLeft,
            self.useRight
        ]
        
    def reset(self):
        for gesture in self._gestures:
            gesture.reset()
                        
    def update(self, currentTime, deltaTime):
        global leftController
        global rightController
        global rollCenter
        
        # update orientation and internal state
        if openVR.isMounted == False:
            return
        
        leftValidation = GestureValidation(openVR.leftTrigger, openVR.leftGrip)
        rightValidation = GestureValidation(openVR.rightTrigger, openVR.rightGrip)
        noneValidation = GestureValidation(1,1)
        
        if self.upperAreaLeft.enabled:
            self.upperAreaLeft.update(currentTime, openVR.headPose.position.y - openVR.leftTouchPose.position.y, leftValidation)
        
        if self.upperAreaRight.enabled:
            self.upperAreaRight.update(currentTime, openVR.headPose.position.y - openVR.rightTouchPose.position.y, leftValidation)
        
        if self.aimPistol.enabled:
            # calculate distance between hands to determine gun pose
            dx = openVR.leftTouchPose.position.x - openVR.rightTouchPose.position.x
            dy = openVR.leftTouchPose.position.y - openVR.rightTouchPose.position.y
            dz = openVR.leftTouchPose.position.z - openVR.rightTouchPose.position.z
            d = dx*dx + dy*dy + dz*dz
            
            self.aimPistol.update(currentTime, d, leftValidation) 
                        
        if self.aimRifleRight.enabled:
            # prioritize pistol aiming
            if self.aimPistol.inGesture or dotProduct(openVR.leftTouchPose.forward, openVR.headPose.forward) < 0.5:
                self.aimRifleRight.update(currentTime, 0, rightValidation)
            else:
                # calculate distance between left hand and head to determine rifle pose
                dx = openVR.rightTouchPose.position.x - openVR.headPose.position.x
                dz = openVR.rightTouchPose.position.z - openVR.headPose.position.z
                d = dx*dx + dz*dz
                
                self.aimRifleRight.update(currentTime, -d, rightValidation)
            
        if self.aimRifleLeft.enabled:
            # prioritize pistol and right rifle aiming
            if self.aimPistol.inGesture or self.aimRifleRight.inGesture or dotProduct(openVR.leftTouchPose.forward, openVR.headPose.forward) < 0.5:
                self.aimRifleLeft.update(currentTime, 0, leftValidation)
            else:
                # calculate distance between left hand and head to determine rifle pose
                dx = openVR.leftTouchPose.position.x - openVR.headPose.position.x
                dz = openVR.leftTouchPose.position.z - openVR.headPose.position.z
                d = dx*dx + dz*dz
                
                self.aimRifleLeft.update(currentTime, -d, leftValidation)
        
        # buttons
        if self.buttonA.enabled:
            self.buttonA.update(currentTime, -openVR.a, rightValidation)
        if self.buttonB.enabled:
            self.buttonB.update(currentTime, -openVR.b, rightValidation)
        if self.buttonRightStick.enabled:
            self.buttonRightStick.update(currentTime, -openVR.rightStick, rightValidation)
            
        if self.buttonX.enabled:
            self.buttonX.update(currentTime, -openVR.x, leftValidation)
        if self.buttonY.enabled:
            self.buttonY.update(currentTime, -openVR.y, leftValidation)
        if self.buttonLeftStick.enabled:
            self.buttonLeftStick.update(currentTime, -openVR.leftStick, leftValidation)
            
        if self.buttonLeftStickUp.enabled:
            self.buttonLeftStickUp.update(currentTime, -openVR.leftStickAxes.y, leftValidation)
        if self.buttonLeftStickDown.enabled:
            self.buttonLeftStickDown.update(currentTime, openVR.leftStickAxes.y, leftValidation)
        if self.buttonLeftStickLeft.enabled:
            self.buttonLeftStickLeft.update(currentTime, openVR.leftStickAxes.x, leftValidation)
        if self.buttonLeftStickRight.enabled:
            self.buttonLeftStickRight.update(currentTime, -openVR.leftStickAxes.x, leftValidation)
                
        leftStick = math.sqrt(openVR.leftStickAxes.x*openVR.leftStickAxes.x + openVR.leftStickAxes.y*openVR.leftStickAxes.y)
        if self.buttonLeftStickInnerRing.enabled:
            self.buttonLeftStickInnerRing.update(currentTime, leftStick, leftValidation)
        if self.buttonLeftStickOuterRing.enabled:
            self.buttonLeftStickOuterRing.update(currentTime, -leftStick, leftValidation)
         
        if self.buttonRightStickUp.enabled:
            self.buttonRightStickUp.update(currentTime, -openVR.rightStickAxes.y, rightValidation)
        if self.buttonRightStickDown.enabled:
            self.buttonRightStickDown.update(currentTime, openVR.rightStickAxes.y, rightValidation)        
        if self.buttonRightStickLeft.enabled:
            self.buttonRightStickLeft.update(currentTime, openVR.rightStickAxes.x, rightValidation)            
        if self.buttonRightStickRight.enabled:
            self.buttonRightStickRight.update(currentTime, -openVR.rightStickAxes.x, rightValidation)
        
        rightStick = math.sqrt(openVR.rightStickAxes.x*openVR.rightStickAxes.x + openVR.rightStickAxes.y*openVR.rightStickAxes.y)
        if self.buttonRightStickInnerRing.enabled:
            self.buttonRightStickInnerRing.update(currentTime, rightStick, rightValidation)
        if self.buttonRightStickOuterRing.enabled:
            self.buttonRightStickOuterRing.update(currentTime, -rightStick, rightValidation)
        
        # head based lean support
        roll = getRoll(openVR.headPose)
        if self.leanLeft.enabled:
            self.leanLeft.update(currentTime, roll - rollCenter, noneValidation)
        
        if self.leanRight.enabled:
            self.leanRight.update(currentTime, rollCenter - roll, noneValidation)

        # left hand based use
        if self.useLeft.enabled:
            self.useLeft.update(currentTime, openVR.leftTouchPose.left.y, leftValidation)            
                            
        # right hand based use
        if self.useRight.enabled:
            self.useRight.update(currentTime, -openVR.rightTouchPose.left.y, rightValidation)

        # calculate distance between left hand and head to determine light pose
        if self.lightLeft.enabled:
            dx = openVR.leftTouchPose.position.x - openVR.headPose.position.x
            dy = openVR.leftTouchPose.position.y - openVR.headPose.position.y
            dz = openVR.leftTouchPose.position.z - openVR.headPose.position.z
            d = dx*dx + dy*dy + dz*dz
            self.lightLeft.update(currentTime, d, leftValidation)
                        
        # calculate distance between right hand and head to determine light pose        
        if self.lightRight.enabled:
            dx = openVR.rightTouchPose.position.x - openVR.headPose.position.x
            dy = openVR.rightTouchPose.position.y - openVR.headPose.position.y
            dz = openVR.rightTouchPose.position.z - openVR.headPose.position.z
            d = dx*dx + dy*dy + dz*dz
            self.lightRight.update(currentTime, d, rightValidation)
                        
        # left melee
        # calculate speed from left controller        
        dx = openVR.leftTouchPose.position.x - leftController.x
        dy = openVR.leftTouchPose.position.y - leftController.y
        dz = openVR.leftTouchPose.position.z - leftController.z
        d = (dx*dx + dy*dy + dz*dz) / (deltaTime * deltaTime)
        leftMeleeAction = -1
        
        # use left melee as fallback if available
        if self.meleeLeft.enabled:
            leftMeleeAction = 0
        # check for alt melee gestures
        if openVR.leftTouchPose.forward.y < self.leftMeleeAltThreshold:
            dot = dotProduct(openVR.leftTouchPose.left, openVR.headPose.forward)
            # check for force push
            if self.meleeLeftAltPush.enabled and dot < -0.5:
                leftMeleeAction = 2
            # check for force pull
            elif self.meleeLeftAltPull.enabled and dot > 0.5:
                leftMeleeAction = 3
            # use left melee alt as fallback
            elif self.meleeLeftAlt.enabled:
                leftMeleeAction = 1
        
        if leftMeleeAction == 0:
            self.meleeLeft.update(currentTime, -d, leftValidation)
        else:
            self.meleeLeft.update(currentTime, 0, leftValidation)
        
        if leftMeleeAction == 1:
            self.meleeLeftAlt.update(currentTime, -d, leftValidation)
        else:
            self.meleeLeftAlt.update(currentTime, 0, leftValidation)
        
        if leftMeleeAction == 2:
            self.meleeLeftAltPush.update(currentTime, -d, leftValidation)
        else:
            self.meleeLeftAltPush.update(currentTime, 0, leftValidation)
        
        if leftMeleeAction == 3:
            self.meleeLeftAltPull.update(currentTime, -d, leftValidation)
        else:
            self.meleeLeftAltPull.update(currentTime, 0, leftValidation)
                
        # right melee
        # calculate speed from right controller
        dx = openVR.rightTouchPose.position.x - rightController.x
        dy = openVR.rightTouchPose.position.y - rightController.y
        dz = openVR.rightTouchPose.position.z - rightController.z
        d = (dx*dx + dy*dy + dz*dz) / (deltaTime * deltaTime)
        rightMeleeAction = -1
        
        # use right melee as fallback if available
        if self.meleeRight.enabled:
            rightMeleeAction = 0
        # check for alt melee gestures
        if openVR.rightTouchPose.forward.y < self.rightMeleeAltThreshold:
            dot = dotProduct(openVR.rightTouchPose.left, openVR.headPose.forward)
            # check for force push
            if self.meleeRightAltPush.enabled and dot < -0.5:
                rightMeleeAction = 2
            # check for force pull
            elif self.meleeRightAltPull.enabled and dot > 0.5:
                rightMeleeAction = 3
            # use left melee alt as fallback
            elif self.meleeRightAlt.enabled:
                rightMeleeAction = 1
        
        if rightMeleeAction == 0:
            self.meleeRight.update(currentTime, -d, rightValidation)
        else:
            self.meleeRight.update(currentTime, 0, rightValidation)
        
        if rightMeleeAction == 1:
            self.meleeRightAlt.update(currentTime, -d, rightValidation)
        else:
            self.meleeRightAlt.update(currentTime, 0, rightValidation)
        
        if rightMeleeAction == 2:
            self.meleeRightAltPush.update(currentTime, -d, rightValidation)
        else:
            self.meleeRightAltPush.update(currentTime, 0, rightValidation)
        
        if rightMeleeAction == 3:
            self.meleeRightAltPull.update(currentTime, -d, rightValidation)
        else:
            self.meleeRightAltPull.update(currentTime, 0, rightValidation)
        
        # shoulder checks        
        holsterY = openVR.headPose.position.y + self.holsterOffset.y
        leftHolsterX = openVR.headPose.position.x - openVR.headPose.left.x * self.holsterOffset.x + openVR.headPose.forward.x * self.holsterOffset.z
        leftHolsterZ = openVR.headPose.position.z - openVR.headPose.left.z * self.holsterOffset.x + openVR.headPose.forward.z * self.holsterOffset.z
        rightHolsterX = openVR.headPose.position.x + openVR.headPose.left.x * self.holsterOffset.x + openVR.headPose.forward.x * self.holsterOffset.z
        rightHolsterZ = openVR.headPose.position.z + openVR.headPose.left.z * self.holsterOffset.x + openVR.headPose.forward.z * self.holsterOffset.z
            
        if self.holsterWeaponLeft.enabled:
            dx = openVR.rightTouchPose.position.x - leftHolsterX
            dy = openVR.rightTouchPose.position.y - holsterY
            dz = openVR.rightTouchPose.position.z - leftHolsterZ
            d = dx*dx + dy*dy + dz*dz    
            self.holsterWeaponLeft.update(currentTime, d, rightValidation)        
                
        if self.holsterWeaponRight.enabled:
            dx = openVR.rightTouchPose.position.x - rightHolsterX
            dy = openVR.rightTouchPose.position.y - holsterY
            dz = openVR.rightTouchPose.position.z - rightHolsterZ
            d = dx*dx + dy*dy + dz*dz
            self.holsterWeaponRight.update(currentTime, d, rightValidation)
                        
        if self.holsterInventoryLeft.enabled:
            dx = openVR.leftTouchPose.position.x - leftHolsterX
            dy = openVR.leftTouchPose.position.y - holsterY
            dz = openVR.leftTouchPose.position.z - leftHolsterZ
            d = dx*dx + dy*dy + dz*dz
            self.holsterInventoryLeft.update(currentTime, d, leftValidation)
            
        if self.holsterInventoryRight.enabled:
            dx = openVR.leftTouchPose.position.x - rightHolsterX
            dy = openVR.leftTouchPose.position.y - holsterY
            dz = openVR.leftTouchPose.position.z - rightHolsterZ
            d = dx*dx + dy*dy + dz*dz
            self.holsterInventoryRight.update(currentTime, d, leftValidation)

        # shoulder checks        
        shoulderY = openVR.headPose.position.y + self.shoulderOffset.y
        leftShoulderX = openVR.headPose.position.x - openVR.headPose.left.x * self.shoulderOffset.x + openVR.headPose.forward.x * self.shoulderOffset.z
        leftShoulderZ = openVR.headPose.position.z - openVR.headPose.left.z * self.shoulderOffset.x + openVR.headPose.forward.z * self.shoulderOffset.z
        rightShoulderX = openVR.headPose.position.x + openVR.headPose.left.x * self.shoulderOffset.x + openVR.headPose.forward.x * self.shoulderOffset.z
        rightShoulderZ = openVR.headPose.position.z + openVR.headPose.left.z * self.shoulderOffset.x + openVR.headPose.forward.z * self.shoulderOffset.z
            
        if self.shoulderWeaponLeft.enabled:
            dx = openVR.rightTouchPose.position.x - leftShoulderX
            dy = openVR.rightTouchPose.position.y - shoulderY
            dz = openVR.rightTouchPose.position.z - leftShoulderZ
            d = dx*dx + dy*dy + dz*dz    
            self.shoulderWeaponLeft.update(currentTime, d, rightValidation)        
                
        if self.shoulderWeaponRight.enabled:
            dx = openVR.rightTouchPose.position.x - rightShoulderX
            dy = openVR.rightTouchPose.position.y - shoulderY
            dz = openVR.rightTouchPose.position.z - rightShoulderZ
            d = dx*dx + dy*dy + dz*dz
            self.shoulderWeaponRight.update(currentTime, d, rightValidation)
                        
        if self.shoulderInventoryLeft.enabled:
            dx = openVR.leftTouchPose.position.x - leftShoulderX
            dy = openVR.leftTouchPose.position.y - shoulderY
            dz = openVR.leftTouchPose.position.z - leftShoulderZ
            d = dx*dx + dy*dy + dz*dz
            self.shoulderInventoryLeft.update(currentTime, d, leftValidation)
            
        if self.shoulderInventoryRight.enabled:
            dx = openVR.leftTouchPose.position.x - rightShoulderX
            dy = openVR.leftTouchPose.position.y - shoulderY
            dz = openVR.leftTouchPose.position.z - rightShoulderZ
            d = dx*dx + dy*dy + dz*dz
            self.shoulderInventoryRight.update(currentTime, d, leftValidation)
            
        # at the end check for trigger and grip, so previous gestures can use these 
        if self.triggerLeft.enabled:
            self.triggerLeft.update(currentTime, -openVR.leftTrigger, leftValidation)
            
        if self.triggerRight.enabled:
            self.triggerRight.update(currentTime, -openVR.rightTrigger, rightValidation)
                        
        if self.gripLeft.enabled:
            self.gripLeft.update(currentTime, -openVR.leftGrip, leftValidation)
            
        if self.gripRight.enabled:
            self.gripRight.update(currentTime, -openVR.rightGrip, rightValidation)

class TouchHaptics:
    def __init__(self, left, samples):
        self.left = left
        self.samples = samples

class TouchHapticsSample:
    def __init__(self, frequency, amplitude):
        self.frequency = frequency
        self.amplitude = amplitude

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
            openVR.triggerHapticPulse(0, deltaTime, left.frequency, left.amplitude)
            
        if len(self._right) > 0:
            right = self._right.pop(0)
            openVR.triggerHapticPulse(1, deltaTime, right.frequency, right.amplitude)

    # some patterns
    def pulse(self, length, intensity):
        global UpdateFrequency
        
        count = (int)(length / (5*UpdateFrequency))
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
        
        count = (int)(length / UpdateFrequency)
        haptics = self.pulse(length, intensity)
        for x in range(count):
            haptics.append(TouchHapticsSample(1, 0))
        
        return haptics

# method for centering  
def reset():
    global leftController
    global rightController
    global rollCenter
    global gestureTracker
    global v2k
    global vrToMouse
    global vrToGamepad

    # recenter the device
    openVR.center()
            
    # set current controller positions
    leftController.x = openVR.leftTouchPose.position.x    
    leftController.y = openVR.leftTouchPose.position.y
    leftController.z = openVR.leftTouchPose.position.z
    
    rightController.x = openVR.rightTouchPose.position.x
    rightController.y = openVR.rightTouchPose.position.y
    rightController.z = openVR.rightTouchPose.position.z

    # recenter roll settings
    rollCenter = 0 #gestureTracker.roll(openVR.headPose)
    
    # unpress all buttons
    gestureTracker.reset()
    v2k.reset()
    vrToMouse.reset()
    vrToGamepad.reset()

# getting new information from device
def update():
    global UpdateFrequency
    global LastUpdate
    global leftController
    global rightController
    global gestureTracker
    global touchHapticsPlayer
    global v2k
    global vrToMouse
    global vrToGamepad
    
    # check interval
    currentTime = time.clock()
    deltaTime = time.clock() - LastUpdate
    if deltaTime < UpdateFrequency:
        return
    
    # check gestures
    gestureTracker.update(currentTime, deltaTime)
        
    # check voice commands
    v2k.update(currentTime) 
    
    # check vr mouse movement
    vrToMouse.update(currentTime, deltaTime)
    
    # check vr gamepad interaction
    vrToGamepad.update(currentTime)
    
    # perform touch haptics
    touchHapticsPlayer.update(deltaTime)
                    
    # set current controller positions
    leftController.x = openVR.leftTouchPose.position.x    
    leftController.y = openVR.leftTouchPose.position.y
    leftController.z = openVR.leftTouchPose.position.z
    
    rightController.x = openVR.rightTouchPose.position.x    
    rightController.y = openVR.rightTouchPose.position.y
    rightController.z = openVR.rightTouchPose.position.z
            
    # reset clock for next update
    LastUpdate = time.clock()


import clr
clr.AddReference('System.Windows.Forms')
from System.Windows.Forms import Application, Form, Label, ComboBox, ComboBoxStyle, DockStyle, Button, FormBorderStyle, FormStartPosition
class SettingsForm(Form):
    def __init__(self):
        self.Text = 'VR Companion Settings'
        self.Name = 'VR Companion Settings'
        
        self.FormBorderStyle = FormBorderStyle.FixedDialog;
        self.MaximizeBox = False;
        self.MinimizeBox = False;
        self.StartPosition = FormStartPosition.CenterScreen;
        self.Height = 128
        
        profileLabel = Label()
        profileLabel.Text = "Profile"
        profileLabel.Dock = DockStyle.Top
        
        self.profileCombo = ComboBox()
        import glob
        for profile in glob.glob("scripts\profiles\*.py"):
        	self.profileCombo.Items.Add(profile.replace("scripts\profiles\\", "").replace(".py", ""))        
        self.profileCombo.Dock = DockStyle.Top
        self.profileCombo.DropDownStyle = ComboBoxStyle.DropDownList        
        
        button = Button()
        button.Text = "Start"
        button.Dock = DockStyle.Top
        button.Click += self.buttonPressed
        
        self.Controls.Add(button)
        self.Controls.Add(self.profileCombo)
        self.Controls.Add(profileLabel)
    
    def buttonPressed(self, sender, args):
    	self.Close()

# a function to predefine settings for different games
def selectProfile():
    global gestureTracker
    global v2k
    global weaponInventory
    global hapticPlayer
    global touchHapticsPlayer
    global vrToMouse
    global vrToGamepad
    global profile

    # gestureTracker handles all controller based gestures (see test profile which has all of them bound to a key and enabled)
    # each gesture
    # - can be "enabled"
    # - can be associated an "action" (optional if only haptic feedback is required)
    # - can have haptic feedback (e.g. when the gesture is entered, maintained and left)
    #    - use HapticsGroup(validating, enter, hold, leave, touchValidating, touchEnter, touchHold, touchLeave) with all parameters being optional
    
    # v2k handles all voice commands
    # simply add all required like this: v2k.addCommand("Save", KeyPress(Key.F5), "Voice Feedback")
    # first parameter is the word to say to activate the command
    # second parameter is the action to perform
    # third parameter is haptic feedback (optional)
    
    # weaponInventory keeps track of available weapons and their haptic feedbacks and the currently selected weapon
    # it basically allows to associated different haptics to the fireWeapon (right trigger) gesture
    
    # hapticPlayer handles bhaptics feedback
    # use it to load additional behaptics presets
    
    # vrToMouse handles mapping of head or controller movements to mouse movements
    # use vrToMouse.mode to toggle between the different modes (use ModeSwitch* actions to toggle them during gameplay):
    # - 0: No mouse output
    # - 1: Headset to mouse
    # - 2: Left controller to mouse
    # - 3: Right controller to mouse
    # - 4: right stick only
    # For Left and right controller, the difference in yaw and pitch to the head is communicated to reshade for the detached aiming shader to do its magic.
    
    # initialize it with vrToGamepad.setController(VigemController.XBoxController) (or VigemController.DualShockController)
    # it contains multiple modes to steer the mapping (use ModeSwitch* actions to toggle them during gameplay):
    #  - vrToGamepad.leftTriggerMode and vrToGamepad.rightTriggerMode handle mapping from
    #    controller to gamepad triggers
    #  - vrToGamepad.leftStickMode and vrToGamepad.rightStickMode handle mapping from 
    #    controller to gamepad sticks
    #  - vrToGamepad.dpadMode handle mapping from controller sticks to dpad
    # For all of those:
    # - 0: No output
    # - 1: Left trigger or stick
    # - 2: Right trigger or stick
    # For the dpad an additional vrToGamepad.dpadThreshold can be defined.
    
    # possible actions for gestures and voice commands
    # - KeyQuickPress(Key.A) or KeyQuickPress([Key.Shift, Key.A]): to press a single button/multiple buttons when entering a gesture
    # - KeyPress(Key.A) or KeyPress([Key.Shift, Key.A]): to hold down a single button/multiple buttons while within a gesture and releasing them when leaving the gesture (voice commands hold for a fixed duration)
    # - KeyRepeat(Key.A, times, interval) or KeyRepeat([Key.Shift, Key.A], times, interval): to repeat pressing a single button/multiple buttons while within a gesture, times says how often to repeat the button for a voice command,
    #        interval is the time between two presses of the button
    # - KeyToggle(Key.A) or KeyToggle([Key.Shift, Key.A]): to press a single button/multiple buttons when entering a gesture and pressing it again when leaving it (voice commands only press it once and are thus equal to KeyQuickPress)
    #
    # - MouseQuickPress(0): to press a single button when entering a gesture
    # - MousePress(0): to hold down a mouse button while within a gesture and releasing it when leaving the gesture (voice commands hold for a fixed duration)
    # - MouseRepeat(0): to repeat pressing a single button while within a gesture, times says how often to repeat the button for a voice command, interval is the time between two presses of the button
    # - MouseToggle(0): to press a single button when entering a gesture and pressing it again when leaving it (voice commands only press it once and are thus equal to MouseQuickPress)
    # as for Key* you can also multiple mouse buttons, 0: left, 1: right, 2: middle mouse button
    #
    # - GamepadQuickPress(VigemButton.A) or GamepadQuickPress([VigemButton.A, VigemButton.X]): to press a single button/multiple buttons when entering a gesture
    # - GamepadPress(VigemButton.A) or GamepadPress([VigemButton.Shift, VigemButton.A]): to hold down a single button/multiple buttons while within a gesture and releasing them when leaving the gesture (voice commands hold for a fixed duration)
    # - GamepadRepeat(VigemButton.A, times, interval) or GamepadRepeat([VigemButton.X, VigemButton.A], times, interval): to repeat pressing a single button/multiple buttons while within a gesture, times says how often to repeat the button for a voice command,
    #        interval is the time between two presses of the button
    # - GamepadToggle(VigemButton.A) or KeyToggle([VigemButton.X, VigemButton.A]): to press a single button/multiple buttons when entering a gesture and pressing it again when leaving it (voice commands only press it once and are thus equal to GamepadQuickPress)
    # To use a gamepad action, you have to first initialize the gamepade controller with vrToGamepad.setController(VigemController.XBoxController).
    #
    # - InventorySelect(inventory, item): activates the given inventory item (numeric index)
    # -    InventoryReplace(inventory, newItem): replaces the current item of inventory with the newItem (used for more dynamic inventories such as DeusEx or L4D)
    #
    # - MultiAction([action1, action2]): if you want to perform multiple actions at the same time (not required to press multiple buttons)
    #
    # - ActionSequence([TimedAction(action1, duration1), TimedAction(action2, duration2)]): if you want to perform actions after each other (use Action() for pauses)
    #
    # - TimeBased([actionShort, actionLong], optionalDuration): if you want to have an action for a short or long press (single shot or auto shot, switch view mode or zoom) 
    #
    # - ModeSwitch(mode, index): activates the index for the given mode (you can define a number of independent modes, just give them unique names), the default index is 0
    # - ModeSwitchWithReset(mode, index, resetIndex): similar to ModeSwitch but resets to the index when entering (resetIndex == -1) or to resetIndex    
    # - ModeBasedAction(mode, [action0, action1, action2, ...]): selects the action with the current active index of the given mode 
    
    # possible validation modes
    GestureValidation_None = 0
    GestureValidation_Delay = 1
    GestureValidation_Trigger = 2
    GestureValidation_Grip = 3
    
    # touch haptics position and prefabs
    Touch_Left = True
    Touch_Right = False
    Touch_Validating_Left = TouchHaptics(Touch_Left, touchHapticsPlayer.pulse(0.1, 0.25))
    Touch_Validating_Right = TouchHaptics(Touch_Right, touchHapticsPlayer.pulse(0.1, 0.25))
    Touch_Enter_Left = TouchHaptics(Touch_Left, touchHapticsPlayer.pulse(0.25, 1))
    Touch_Enter_Right = TouchHaptics(Touch_Right, touchHapticsPlayer.pulse(0.25, 1))
    Touch_Melee_Left = TouchHaptics(Touch_Left, touchHapticsPlayer.pulseWithPause(0.4, 1, 0.7))
    Touch_Melee_Right = TouchHaptics(Touch_Right, touchHapticsPlayer.pulseWithPause(0.4, 1, 0.7))
        
    Haptics_Pistol = HapticsGroup(enter = "MinigunVest_R", touchEnter = TouchHaptics(Touch_Right, touchHapticsPlayer.pulse(0.2, 0.5)))
    Haptics_AutoPistol = HapticsGroup(hold = "MinigunVest_R", touchHold = TouchHaptics(Touch_Right, touchHapticsPlayer.pulse(0.2, 0.5)))
    Haptics_Rifle = HapticsGroup(enter = "MinigunVest_R", touchEnter = TouchHaptics(Touch_Right, touchHapticsPlayer.pulse(0.2, 1.0)))
    Haptics_AutoRifle = HapticsGroup(hold = "MinigunVest_R", touchHold = TouchHaptics(Touch_Right, touchHapticsPlayer.pulse(0.2, 1.0)))
    Haptics_Shotgun = HapticsGroup(enter = "RecoilShotgunVest_R", touchEnter = TouchHaptics(Touch_Right, touchHapticsPlayer.pulseWithPause(0.4, 1.0, 0.7)))
    Haptics_AutoShotgun = HapticsGroup(hold = "RecoilShotgunVest_R", touchHold = TouchHaptics(Touch_Right, touchHapticsPlayer.pulseWithPause(0.4, 1.0, 0.7)))
    
    # some default feedbacks
    gestureTracker.meleeLeft.haptics.enter = "RecoilMeleeVest_L"
    gestureTracker.meleeLeft.haptics.touchEnter = Touch_Melee_Left
    gestureTracker.meleeLeftAlt.haptics.enter = "RecoilMeleeVest_L"
    gestureTracker.meleeLeftAlt.haptics.touchEnter = Touch_Melee_Left
    gestureTracker.meleeLeftAltPull.haptics.enter = "Force Pull_L"
    gestureTracker.meleeLeftAltPull.haptics.touchEnter = Touch_Melee_Left
    gestureTracker.meleeLeftAltPush.haptics.enter = "Force Push_L"
    gestureTracker.meleeLeftAltPush.haptics.touchEnter = Touch_Melee_Left
    gestureTracker.meleeRight.haptics.enter = "RecoilMeleeVest_R"
    gestureTracker.meleeRight.haptics.touchEnter = Touch_Melee_Right
    gestureTracker.meleeRightAlt.haptics.enter = "RecoilMeleeVest_R"
    gestureTracker.meleeRightAlt.haptics.touchEnter = Touch_Melee_Right
    gestureTracker.meleeRightAltPull.haptics.enter = "Force Pull_R"
    gestureTracker.meleeRightAltPull.haptics.touchEnter = Touch_Melee_Left
    gestureTracker.meleeRightAltPush.haptics.enter = "Force Push_R"
    gestureTracker.meleeRightAltPush.haptics.touchEnter = Touch_Melee_Left
        
    gestureTracker.holsterInventoryLeft.validating = "Holster Left"
    gestureTracker.holsterInventoryLeft.touchValidating = Touch_Validating_Left
    gestureTracker.holsterInventoryLeft.haptics.enter =  "Equip From Left to Left"
    gestureTracker.holsterInventoryLeft.haptics.touchEnter =  Touch_Enter_Left
    gestureTracker.holsterInventoryRight.validating = "Holster Right"
    gestureTracker.holsterInventoryRight.touchValidating = Touch_Validating_Left
    gestureTracker.holsterInventoryRight.haptics.enter = "Equip From Right to Left"
    gestureTracker.holsterInventoryRight.haptics.touchEnter =  Touch_Enter_Left
    gestureTracker.holsterWeaponLeft.validating = "Holster Left"
    gestureTracker.holsterWeaponLeft.touchValidating = Touch_Validating_Right
    gestureTracker.holsterWeaponLeft.haptics.enter =  "Equip From Left to Right"
    gestureTracker.holsterWeaponLeft.haptics.touchEnter =  Touch_Enter_Right
    gestureTracker.holsterWeaponRight.validating = "Holster Right"
    gestureTracker.holsterWeaponRight.touchValidating = Touch_Validating_Right
    gestureTracker.holsterWeaponRight.haptics.enter = "Equip From Right to Right"
    gestureTracker.holsterWeaponRight.haptics.touchEnter =  Touch_Enter_Right
    
    gestureTracker.shoulderInventoryLeft.validating = "Shoulder Holster Left"
    gestureTracker.shoulderInventoryLeft.touchValidating = Touch_Validating_Left
    gestureTracker.shoulderInventoryLeft.haptics.enter =  "Equip From Left to Left"
    gestureTracker.shoulderInventoryLeft.haptics.touchEnter =  Touch_Enter_Left
    gestureTracker.shoulderInventoryRight.validating = "Shoulder Holster Right"
    gestureTracker.shoulderInventoryRight.touchValidating = Touch_Validating_Left
    gestureTracker.shoulderInventoryRight.haptics.enter = "Equip From Right to Left"
    gestureTracker.shoulderInventoryRight.haptics.touchEnter =  Touch_Enter_Left
    gestureTracker.shoulderWeaponLeft.validating = "Shoulder Holster Left"
    gestureTracker.shoulderWeaponLeft.touchValidating = Touch_Validating_Right
    gestureTracker.shoulderWeaponLeft.haptics.enter =  "Equip From Left to Right"
    gestureTracker.shoulderWeaponLeft.haptics.touchEnter =  Touch_Enter_Right
    gestureTracker.shoulderWeaponRight.validating = "Shoulder Holster Right"
    gestureTracker.shoulderWeaponRight.touchValidating = Touch_Validating_Right
    gestureTracker.shoulderWeaponRight.haptics.enter = "Equip From Right to Right"
    gestureTracker.shoulderWeaponRight.haptics.touchEnter =  Touch_Enter_Right
    
    gestureTracker.lightLeft.validating = "Light Left"
    gestureTracker.lightLeft.touchValidating = Touch_Validating_Left
    gestureTracker.lightLeft.haptics.touchEnter = Touch_Enter_Left
    gestureTracker.lightRight.validating = "Light Right"
    gestureTracker.lightRight.touchValidating = Touch_Validating_Right
    gestureTracker.lightRight.haptics.touchEnter = Touch_Enter_Right
    
    # some default validation modes (fireWeapon and grab should not be changed)
    gestureTracker.triggerLeft.validationMode = GestureValidation_Trigger
    gestureTracker.triggerRight.validationMode = GestureValidation_Trigger
    gestureTracker.gripLeft.validationMode = GestureValidation_Grip
    gestureTracker.gripRight.validationMode = GestureValidation_Grip
    
    gestureTracker.holsterInventoryLeft.validationMode = GestureValidation_Delay
    gestureTracker.holsterInventoryRight.validationMode = GestureValidation_Delay
    gestureTracker.holsterWeaponLeft.validationMode = GestureValidation_Delay
    gestureTracker.holsterWeaponRight.validationMode = GestureValidation_Delay
    gestureTracker.lightLeft.validationMode = GestureValidation_Delay
    gestureTracker.lightRight.validationMode = GestureValidation_Delay
    gestureTracker.shoulderInventoryLeft.validationMode = GestureValidation_Delay
    gestureTracker.shoulderInventoryRight.validationMode = GestureValidation_Delay
    gestureTracker.shoulderWeaponLeft.validationMode = GestureValidation_Delay
    gestureTracker.shoulderWeaponRight.validationMode = GestureValidation_Delay
    
    # holster and shoulder offset
    gestureTracker.holsterOffset = Vector(0.3, -0.75, 0.45)    # the offset from head to holster
    gestureTracker.shoulderOffset = Vector(0.3, 0, 0.45)    # the offset from head to shoulder
            	
    # settings
    showDialog = (profile == None)
       
    # load settings
    import json
    try:
	    with open('scripts/vr_companion.json') as settingsFile:
	        settings = json.loads(settingsFile.read())
	        if settings != None:
	        	if profile == None:
	        		profile = settings["profile"]
    except:
        if profile == None:
            profile = "WASD_Default"
    
    if showDialog:
        form = SettingsForm()
        
        # set current settings
        form.profileCombo.SelectedItem = profile
        
        # show form
        Application.Run(form)    
    	
    	# get current settings
    	profile = form.profileCombo.SelectedItem
    
        # save settings
        settings = {}
        settings["profile"] = profile
        with open('scripts/vr_companion.json', "w") as settingsFile:
        	settingsFile.write(json.dumps(settings))        
    
    # apply profile    
    diagnostics.watch(profile)
    with open('scripts/profiles/' + profile + '.py') as f:
        exec(f.read())
            
# initialization of state and constants
if starting:
    diagnostics.watch(sys.version)
    
    LastUpdate = time.clock()                # last time an update happened
    UpdateFrequency = 1.0 / 60.0            # interval between updates
    
    global profile
    if "profile" in globals():
        DebugOutput = False
    else:
        DebugOutput = True
        profile = None
            
    # initialize haptics feedback
    if skipBhaptics:
        hapticPlayer = None
    else:
        try:
            hapticPlayer = HapticPlayer()
            hapticPlayer.wait()
            hapticPlayer.submit_dot("backFrame", "VestBack", [{"index": 5, "intensity": 100}], 100)
            time.sleep(0.1)
            hapticPlayer.registerFromScripts("Chainsword_L", 0.24)
            hapticPlayer.registerFromScripts("Equip From Left to Left", 1.8)
            hapticPlayer.registerFromScripts("Equip From Left to Right", 1.8)
            hapticPlayer.registerFromScripts("Equip From Right to Left", 1.8)
            hapticPlayer.registerFromScripts("Equip From Right to Right", 1.8)
            hapticPlayer.registerFromScripts("Holster Left", 0.1)
            hapticPlayer.registerFromScripts("Holster Right", 0.1)
            hapticPlayer.registerFromScripts("Force Pull_L", 1.0)
            hapticPlayer.registerFromScripts("Force Push_L", 1.0)
            hapticPlayer.registerFromScripts("Force Pull_R", 1.0)
            hapticPlayer.registerFromScripts("Force Push_R", 1.0)
            hapticPlayer.registerFromScripts("Laser", 1.2)
            hapticPlayer.registerFromScripts("Light Left", 0.1)
            hapticPlayer.registerFromScripts("Light Right", 0.1)
            hapticPlayer.registerFromScripts("Shoulder Holster Left", 0.1)
            hapticPlayer.registerFromScripts("Shoulder Holster Right", 0.1)
            hapticPlayer.registerFromScripts("Voice Feedback", 0.2)
            
            # the following are from https://www.nexusmods.com/warhammer40000battlesister/mods/1
            hapticPlayer.registerFromScripts("MinigunVest_R", 0.2)
            hapticPlayer.registerFromScripts("RecoilMeleeVest_L", 1.0)
            hapticPlayer.registerFromScripts("RecoilMeleeVest_R", 1.0)
            hapticPlayer.registerFromScripts("RecoilShotgunVest_R", 1.0)
                        
            hapticPlayer.submit_dot("frontFrame", "VestFront", [{"index": 5, "intensity": 100}], 100)
            time.sleep(0.1)
        except:
            hapticPlayer = None
            pass
                
    # initialize controllers
    leftController = type('leftController',(object,),{})()        # all information regarding the left controller
    leftController.x = 0.0                            # the last x position of the controller
    leftController.y = 0.0                            # the last y position of the controller
    leftController.z = 0.0                            # the last z position of the controller
    
    rightController = type('rightController',(object,),{})()    # all information regarding the left controller
    rightController.x = 0.0                            # the last x position of the controller
    rightController.y = 0.0                            # the last y position of the controller
    rightController.z = 0.0                            # the last z position of the controller
                    
    # initialize weapon inventory
    weaponInventory = Inventory()

    # intitialize gesture controller
    gestureTracker = GestureTracker(weaponInventory)
        
    # intialize touch haptics
    touchHapticsPlayer = TouchHapticsPlayer()
        
    # initialize voice commands
    v2k = VoiceToKeyboard()
            
    # initialize vr to mouse and gamepad
    vrToMouse = VRToMouse()
    vrToGamepad = VRToGamepad()
            
    selectProfile()
    
    touchHapticsPlayer.play(TouchHaptics(True, touchHapticsPlayer.pulse(0.25, 0.25)))
    touchHapticsPlayer.play(TouchHaptics(False, touchHapticsPlayer.pulse(0.25, 0.25)))
        
    reset()    # reorient the head set settings
    openVR.update += update    # register to update events of the head set 
    
if DebugOutput:
    # debugging
    diagnostics.watch(openVR.headPose.position.x)
    diagnostics.watch(openVR.headPose.position.y)
    diagnostics.watch(openVR.headPose.position.z)
    
    diagnostics.watch(openVR.headPose.forward.x)
    diagnostics.watch(openVR.headPose.forward.y)
    diagnostics.watch(openVR.headPose.forward.z)
    
    diagnostics.watch(openVR.leftTouchPose.forward.x)
    diagnostics.watch(openVR.leftTouchPose.forward.y)
    diagnostics.watch(openVR.leftTouchPose.forward.z)
    
    diagnostics.watch(openVR.rightTouchPose.forward.x)
    diagnostics.watch(openVR.rightTouchPose.forward.y)
    diagnostics.watch(openVR.rightTouchPose.forward.z)
    
    diagnostics.watch(vrToMouse.mode.current)
    
    diagnostics.watch(time.clock())